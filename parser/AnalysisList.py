# -*- coding:utf-8 -*-
# @Time : 2023/2/5 13:09
# @Author: Reborn
# @Project: SimpleCompilerCD
# @File : AnalysisList.py
import json

import Production
import SyncTable
from utils.file import FileReader
from lexer import Lexer
from utils.exception.parser import GrammarError
from utils.exception.parser import ParserError


class AnalysisList:
    def __init__(self, configPath):
        self._fileReader = None
        self._configPath = configPath
        try:
            with open(configPath, 'r', encoding='utf-8') as ff:
                fconfig = json.load(ff)
            self._production = Production.Production(fconfig)
        except FileNotFoundError:
            print('无法打开指定的文件!AL')
        except LookupError:
            print(LookupError.with_traceback())
            print('指定了未知的编码!AL')
        except UnicodeDecodeError:
            print('读取文件时解码错误!AL')
        finally:
            ff.close()
        self._syncTable = SyncTable.SyncTable(production=self._production)

    @property
    def production(self):
        return self._production

    def printItemSetList(self):
        print(self._syncTable.itemSetList)

    def printActionGotoTable(self):
        print(self._syncTable.agList)

    def printAnalysisTable(self):
        print(self._syncTable.analysisTable)

    def getTreeNode(self):
        return self._syncTable.syncTreeNode

    @property
    def production(self):
        return self._production

    def analyse(self, lexer: Lexer) -> bool:
        try:
            self._fileReader = FileReader.FileReader(lexer.filename)
        except GrammarError.GrammarError:
            raise GrammarError.GrammarError
        return self._syncTable.syncTokenList(lexer, ParserError.ParserError(self._fileReader))


if __name__ == '__main__':
    l = Lexer.Lexer("../lexer/config.json", "../lexer/test.txt")
    l.printTokens()
    a = AnalysisList("../parser/config.json")
    print(a.production)
    a.printItemSetList()
    a.printActionGotoTable()
    analyseOk = a.analyse(l)
    a.printAnalysisTable()

    """
    ItemSet (45-56) disappear  去解析为什么46不同即可 fix!: __eq__错误
    """
