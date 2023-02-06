# -*- coding:utf-8 -*-
# @Time : 2023/2/5 13:09
# @Author: Reborn
# @Project: SimpleCompilerCD
# @File : AnalysisList.py
import json

from parser import Production
from parser import SyncTable
from utils.file import FileReader
from lexer import Lexer
from utils.exception.parser import GrammarError
from utils.exception.parser import ParserError


class AnalysisList:
    def __init__(self, configPath):
        self._fileReader = None
        self._configPath = configPath
        try:
            with open(configPath, 'r', encoding='utf-8') as f:
                config = json.load(f)
            self._production = Production.Production(config)
        except FileNotFoundError:
            print('无法打开指定的文件!')
        except LookupError:
            print('指定了未知的编码!')
        except UnicodeDecodeError:
            print('读取文件时解码错误!')
        finally:
            f.close()
        self._syncTable = SyncTable.SyncTable(production=self._production)

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
            print("文法分析错误")
        return self._syncTable.syncTokenList(lexer, ParserError.ParserError(self._fileReader))


if __name__ == '__main__':
    l = Lexer.Lexer("../lexer/config.json", "../parser/test.txt")
    l.printTokens()
    a = AnalysisList("../parser/config.json")
    print(a.production)
    a.printItemSetList()
    a.printActionGotoTable()
    analyseOk = a.analyse(l)
    a.printAnalysisTable()