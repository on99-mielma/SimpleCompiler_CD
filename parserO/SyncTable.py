# -*- coding:utf-8 -*-
# @Time : 2023/2/4 13:13
# @Author: Reborn
# @Project: SimpleCompilerCD
# @File : SyncTable.py
from parserO import Production
from parserO import SyncTreeNode
from lexerO import Lexer
from utils.exception.parser import ParserError
from utils.exception.parser import GrammarError
from lexerO import Token
from lexerO import TokenType


class Item:
    def __init__(self, p: Production.ProductionAtom, index: int = 0, forward: Production.FirstSetData = None):
        self._index = index
        self._p = p
        self._forward = forward

    @property
    def index(self):
        return self._index

    @property
    def p(self):
        return self._p

    @property
    def forward(self):
        return self._forward

    @forward.setter
    def forward(self, f):
        self._forward = f

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Item):
            return False
        if self._index != o._index:
            return False
        pditem = self._p == o._p or self._p.__eq__(o._p)
        if self._forward == o._forward:
            return pditem
        if self._forward is not None and o._forward is not None:
            return pditem and self._forward.__eq__(o._forward)
        else:
            return False

    def __str__(self) -> str:
        return "Item{index=%s, p=%s, forword=%s}\n" % (self._index, self._p, self._forward)

    def __repr__(self) -> str:
        return "Item{index=%s, p=%s, forword=%s}\n" % (self._index, self._p, self._forward)


class ItemSet:
    __itemSetCnt = 0

    @classmethod
    def getiscnt(cls):
        cls.__itemSetCnt += 1

    @classmethod
    def reduceCnt(cls):
        cls.__itemSetCnt -= 1

    def __init__(self):
        self._id = self.__itemSetCnt
        self.getiscnt()
        self._shiftItem = dict()
        self._itemList = []

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, i):
        self._id = i

    @property
    def shiftItem(self):
        return self._shiftItem

    @property
    def itemList(self):
        return self._itemList

    def add(self, i: Item):
        self._itemList.append(i)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, ItemSet):
            return False
        if self._itemList.__eq__(o._itemList):
            return True
        if len(self._itemList) != len(o._itemList):
            return False
        # w = [True for t in o._itemList if o._itemList.count(t) <= self._itemList.count(t)]
        w = []
        for t in o._itemList:
            if o._itemList.count(t) <= self._itemList.count(t):
                w.append(True)
            else:
                w.append(False)
        # numtest = len(set(self._itemList))
        # return numtest >= len(w)
        # return self._itemList >= o._itemList
        return all(w)

    def __str__(self) -> str:
        return "ItemSet{id=%s, shiftItem=%s, itemList=%s}" % (self._id, self._shiftItem, self._itemList)

    def __repr__(self) -> str:
        return "ItemSet{id=%s, shiftItem=%s, itemList=%s}" % (self._id, self._shiftItem, self._itemList)


class ActionGoto:

    def __init__(self, id):
        self._id = id
        self._op = dict()

    @property
    def id(self):
        return self._id

    def get(self, key):
        return self._op.get(key, None)

    def getKeys(self):
        return set(self._op.keys())

    def put(self, keky, a):
        if isinstance(a, int) or isinstance(a, Production.ProductionAtom):
            self._op[keky] = a

    def putKeys(self, keys, a):
        if isinstance(a, int) or isinstance(a, Production.ProductionAtom):
            for key in keys:
                self._op[key] = a

    def remove(self, key):
        del self._op[key]

    def putAll(self, shiftItem):
        """
        将shiftItem放入op中 采用更新策略而非替换策略
        :param shiftItem:
        :return:
        """
        self._op.update(shiftItem)

    def __str__(self) -> str:
        return "ActionGoto{id=%s, op=%s}" % (self._id, self._op)

    def __repr__(self) -> str:
        return "ActionGoto{id=%s, op=%s}" % (self._id, self._op)


class SyncTable:
    def __init__(self, production: Production.Production, START_OF_GRAMMAR: str = "START"):
        """

        :param production:传递的产生式类
        :param START_OF_GRAMMAR: 文法产生式的开始符号 必须在文法中定义 START_OF_GRAMMAR 的增广文法
        """
        self._START_OF_GRAMMAR = START_OF_GRAMMAR
        """
        生成的项目集族 ItemSet相关
        """
        self._itemSetList = []
        """
        生成的项目集族 ActionGoto相关
        """
        self._agList = []
        """
        传递的产生式类
        """
        self._production = production
        """
        符号栈 / 状态栈 分析表
        """
        self._analysisTable = []
        """
        生成抽象语法树  
        """
        self._syncTreeNode: SyncTreeNode.SyncTreeNode = None
        """
        生成 DFA 项目集族
        """
        self.genItemSetList()
        """
        利用 项目集族 生成 action goto表
        """
        self.genActionGotoList()

    @property
    def START_OF_GRAMMAR(self):
        return self._START_OF_GRAMMAR

    @property
    def syncTreeNode(self):
        return self._syncTreeNode

    @property
    def itemSetList(self):
        strisl = ''
        for i in self._itemSetList:
            strisl += str(i)
            strisl += '\n'
        return strisl

    @property
    def agList(self):
        stragl = ''
        for iag in self._agList:
            stragl += str(iag)
            stragl += '\n'
        return stragl

    @property
    def analysisTable(self):
        return self._analysisTable

    def syncTokenList(self, lexer: Lexer.Lexer, parserError: ParserError.ParserError) -> bool:
        state = []
        symbol = []
        syncTreeNodes = []
        tokens = lexer.getTokens()
        state.append(0)
        tokenInd = 0
        while tokenInd >= 0 and tokenInd < len(tokens):
            t: Token.Token = tokens[tokenInd]
            if len(state) == 0:
                parserError.checkGrammar(None, t)
                return False
            index = state[-1]
            actionGoto = self._agList[index]
            val = ""
            if t.kind == TokenType.TokenType.ID.name:
                val = "ID"
            elif t.kind == TokenType.TokenType.CONST.name:
                val = "CONSTANT"
            else:
                val = t.val
            self.addStateAndSymbol(state, symbol, val)
            o = actionGoto.get(val)
            if o is None:
                o = actionGoto.get(None)
            if isinstance(o, int):
                state.append(int(o))
                symbol.append(val)
                syncTreeNodes.append(SyncTreeNode.SyncTreeNode(val=val, token=t))
            elif isinstance(o, Production.ProductionAtom):
                state, symbol, syncTreeNodes = self.reduceToken(state, symbol, syncTreeNodes, o)
                tokenInd -= 1
            else:
                parserError.checkGrammar(actionGoto.getKeys(), t)
                return False
            tokenInd += 1

        while not len(symbol) == 1 or not self._START_OF_GRAMMAR == symbol[-1]:
            self.addStateAndSymbol(state, symbol, None)
            if len(state) == 0:
                parserError.checkGrammar(None, None)
                return False
            index2 = state[-1]
            actionGoto2 = self._agList[index2]
            o2 = actionGoto2.get(None)
            if o2 is None or isinstance(o2, int):
                parserError.checkGrammar(actionGoto2.getKeys(), None)
                return False
            else:
                state, symbol, syncTreeNodes = self.reduceToken(state, symbol, syncTreeNodes, o2)
        self.addStateAndSymbol(state, symbol, None)
        if len(symbol) == 1 and self._START_OF_GRAMMAR == symbol[-1]:
            if len(syncTreeNodes) > 0:
                self._syncTreeNode = syncTreeNodes[-1]
            else:
                self._syncTreeNode = None
            return True
        parserError.checkGrammar(self._agList[state[-1]].getKeys(), None)
        return False

    def addStateAndSymbol(self, state, symbol, val):
        self._analysisTable.append("%-100s\t%-100s\t%s" % (state, symbol, val))

    def reduceToken(self, state: list, symbol: list, syncTreeNodes: list, pAtom: Production.ProductionAtom):
        tempList = []
        lenpar = len(pAtom.right)
        token = Token.Token()
        if lenpar == 1:
            token = syncTreeNodes[-1].token
        for i in range(lenpar):
            if len(state) > 0:
                state.pop()
            if len(symbol) > 0:
                symbol.pop()
            if len(syncTreeNodes) > 0:
                tempList.append(syncTreeNodes.pop())
        tempList.reverse()
        endStr = pAtom.left
        tindex = self._agList[state[-1]].get(endStr)
        if tindex is None:
            index = None
        else:
            index = int(tindex)
        state.append(index)
        symbol.append(endStr)
        tempSyncTreeNode = SyncTreeNode.SyncTreeNode(endStr, tempList, token)
        for t in tempList:
            t.father = tempSyncTreeNode
        syncTreeNodes.append(tempSyncTreeNode)
        return state, symbol, syncTreeNodes

    def genActionGotoList(self):
        for ist in self._itemSetList:
            actiongoto = ActionGoto(ist.id)
            actiongoto.putAll(ist.shiftItem)
            for ite in ist.itemList:
                if ite.index == len(ite.p.right):
                    if ite.forward is None:
                        actiongoto.put(None, ite.p)
                    else:
                        if ite.forward.endToken:
                            actiongoto.put(None, ite.p)
                        actiongoto.putKeys(ite.forward.data, ite.p)
            self._agList.append(actiongoto)

    def genItemSetList(self):
        startProduction: Production.ProductionAtom
        for ipa in self._production.productionList:  # 找到第一条产生式
            if self._START_OF_GRAMMAR == ipa.left:
                startProduction = ipa
                break
        startItem: ItemSet = ItemSet()  # 初始化项目集族
        self._itemSetList.append(startItem)
        startItem.add(Item(p=startProduction))
        i = 0
        istlen = len(self._itemSetList)
        while i < istlen:
            self._itemSetList[i] = self.closure(self._itemSetList[i])  # 算闭包
            self._itemSetList[i] = self.searchForward(self._itemSetList[i])  # 向前搜索
            i += 1
            istlen = len(self._itemSetList)

    def closure(self, itemSet: ItemSet):
        iteml = itemSet.itemList
        initi = 0
        thelen = len(iteml)
        while initi < thelen:
            temp: Item = iteml[initi]
            if temp.index == len(temp.p.right) - 1:
                mayLeft = temp.p.right[temp.index]
                liftMpList = self._production.specmpList(mayLeft)
                if liftMpList is not None:
                    for pa in liftMpList:
                        item2: Item = Item(p=pa, index=0, forward=temp.forward)
                        if iteml.count(item2) == 0:
                            iteml.append(item2)
            elif temp.index < len(temp.p.right) - 1:
                mayLeft2 = temp.p.right[temp.index]
                leftMplist = self._production.specmpList(mayLeft2)
                if leftMplist is not None:
                    secondStr = temp.p.right[temp.index + 1]
                    for pa2 in leftMplist:
                        item3: Item = Item(p=pa2)
                        item3.forward = self._production.firstSet.get(secondStr, None)
                        if iteml.count(item3) == 0:
                            iteml.append(item3)
            initi += 1
            thelen = len(iteml)
        return itemSet

    def searchForward(self, itemSet: ItemSet):
        itemList = itemSet.itemList
        sMap = dict()
        keys = []
        for temp in itemList:
            if temp.index < len(temp.p.right):
                tempStr = temp.p.right[temp.index]
                itemSet2: ItemSet
                if sMap.get(tempStr, None) is not None:
                    itemSet2 = sMap.get(tempStr)
                    itemSet2.itemList.append(Item(temp.p, temp.index + 1, temp.forward))
                else:
                    itemSet2 = ItemSet()
                    itemSet2.itemList.append(Item(temp.p, temp.index + 1, temp.forward))
                    sMap[tempStr] = itemSet2
                    keys.append(tempStr)
        index = len(self._itemSetList)
        for key1 in keys:
            itemSet3: ItemSet = sMap.get(key1)
            itemSet3 = self.closure(itemSet3)
            ind = self.isConflict(itemSet3)
            if ind != -1:
                itemSet._shiftItem[key1] = ind
                itemSet.reduceCnt()
            else:
                itemSet3.id = index
                index += 1
                itemSet._shiftItem[key1] = itemSet3.id
                self._itemSetList.append(itemSet3)
        return itemSet

    def isConflict(self, ist: ItemSet) -> int:
        for i in range(len(self._itemSetList)):
            if ist.__eq__(self._itemSetList[i]):
                return i
        return -1
