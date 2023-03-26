# -*- coding:utf-8 -*-
# @Time : 2023/2/2 13:31
# @Author: Reborn
# @Project: SimpleCompilerCD
# @File : Production.py
import json


class Production(object):
    def __init__(self, pjson):
        """
        产生式的非终结符
        """
        self._nonTerminal = set()
        """
        产生式的终结符
        """
        self._terminal = set()
        """
        产生式 列表
        """
        self._productionList = []
        """
        所有终结符/非终结符 first集合
        """
        self._firstSet = dict()
        """
        产生式 快速拿到产生式
        """
        self._mpList = dict()

        for p in pjson["production"]:
            # print(p)
            self._productionList.append(ProductionAtom(p['left'], p['right']))  # left:str /// right:list
        self.genNonTerminalTerminal()
        self.genFirstSet()

    @property
    def nonTerminal(self):
        return self._nonTerminal

    @property
    def terminal(self):
        return self._terminal

    @property
    def productionList(self):
        return self._productionList

    @property
    def firstSet(self):
        return self._firstSet

    @property
    def mpList(self):
        return self._mpList

    def specmpList(self, wordstr):
        return self._mpList.get(wordstr, None)

    def genNonTerminalTerminal(self):
        """

        :return: 生成终结符和非终结符的相关列表并构造索引
        """
        for pagtt in self._productionList:
            self._nonTerminal.add(pagtt.left)
            self._terminal = self._terminal | set(pagtt.right)
        self._terminal = self._terminal - self._nonTerminal  # 除去终结符列表中的非终结符
        for strnt in self._nonTerminal:
            tempList = []
            for pagtt1 in self._productionList:
                if pagtt1.left == strnt:
                    tempList.append(pagtt1)
            self._mpList[strnt] = tempList

    def genFirstSet(self):
        for wordgfs in self._terminal:
            self.getFirstData(wordgfs)
        for wordgfs0 in self._nonTerminal:
            self.getFirstData(wordgfs0)

    def getFirstData(self, word: str):
        """
        对某一个 (非)终结符 生成first集合
        :param word:
        :return:
        """
        d = FirstSetData()
        if self._firstSet.get(word, None) is not None:
            return self._firstSet[word]
        # if word in self._firstSet:
        #     return self._firstSet[word]
        self._firstSet[word] = d
        if word in self._terminal:  # 终结符处理
            d.add(word)
            d.endToken = False
        else:  # 非终结符处理
            canGetEnd = False
            for pagfd in self._mpList[word]:
                tempRight = pagfd.right
                if len(tempRight) == 0:
                    canGetEnd = True
                else:
                    for tempStrR in tempRight:
                        if tempStrR in self._terminal:  # 如果是终结符则添加并结束
                            d.add(tempStrR)
                            break
                        else:
                            firstData = self.getFirstData(tempStrR)
                            d.add(firstData.data)
                            if not firstData.endToken:
                                break
                        if tempStrR == tempRight[-1]:
                            canGetEnd = True
            d.endToken = canGetEnd
        return d

    def __str__(self) -> str:
        return "Produciton{productionList = %s }" % self._productionList

    def __repr__(self) -> str:
        return "Produciton{productionList = %s }" % self._productionList


class ProductionAtom(object):

    def __init__(self, left, right: list):
        self._left = left
        self._right = right

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    def __str__(self) -> str:
        return "ProductionAtom{left='%s', right='%s'}" % (self._left, self._right)

    def __repr__(self) -> str:
        return "ProductionAtom{left='%s', right='%s'}" % (self._left, self._right)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, ProductionAtom):
            return False
        return o._right == self._right and o._left == self._left


class FirstSetData(object):

    def __init__(self, data=None, endToken=False):
        """

        :param data: first集合
        :param endToken: 标识是否可以接收 结束字符
        """
        if data is None:
            data = set()
        self._data = data
        self._endToken = endToken

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, d):
        self._data = d

    @property
    def endToken(self):
        return self._endToken

    @endToken.setter
    def endToken(self, t):
        self._endToken = t

    # def add(self, word: str):
    #     self._data.add(word)
    #
    # def add(self, setData: set):
    #     self._data = setData | self._data

    def add(self, thing):
        if isinstance(thing, str):
            self._data.add(thing)
        elif isinstance(thing, set):
            self._data.update(thing)

    def remove(self, word):
        self._data.discard(word)

    def __str__(self) -> str:
        return "FirstSetData{data=<< %s >>, endToken='%s'}" % (self._data, self._endToken)

    def __repr__(self) -> str:
        return "FirstSetData{data=<< %s >>, endToken='%s'}" % (self._data, self._endToken)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, FirstSetData):
            return False
        if self._endToken == o._endToken and self._data == o._data:
            return True
        if len(self._data) != len(o._data):
            return False
        # tmpIneq = self._data & o._data
        # return self._endToken == o._endToken and tmpIneq.__eq__(self._data) and len(self._data - tmpIneq) >= 0 and len(o._data - tmpIneq) == 0
        return self._endToken == o._endToken and self._data.issuperset(o._data)


if __name__ == '__main__':
    with open("/config.json", "r", encoding='utf-8') as f:
        config = json.load(f)
    pp = Production(config)
    # print(type(pp.productionList[2].left))
    print(pp.nonTerminal)
    print('-*' * 50)
    print(pp.terminal)
    print('-*' * 50)
    print(pp.productionList)
    print('-*' * 50)
    print(pp.firstSet)
    print('-*' * 50)
    print(pp.mpList)
