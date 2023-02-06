# -*- coding:utf-8 -*-
# @Time : 2023/2/4 14:14
# @Author: Reborn
# @Project: SimpleCompilerCD
# @File : ParserError.py
from utils.file import FileReader
from lexer import Token
from utils.exception.parser import GrammarError


class ParserError:
    def __init__(self, fileReader: FileReader.FileReader = None):
        self._fileReader = fileReader

    def checkGrammar(self, keys: set = None, t: Token.Token = None):
        if self._fileReader is None:
            if t is None:
                raise GrammarError.GrammarError(keys, 0)
            else:
                raise GrammarError.GrammarError(keys, t=t)
        else:
            codeSize = len(self._fileReader.readRow)
            if t is None:
                for i in max(codeSize - 2, 0):
                    print(self._fileReader.userowInd(i))
                print("ˇ")
                print()
                raise GrammarError.GrammarError(keys, codeSize)
            else:
                codeRow = t.row
                codeCol = t.col
                if codeRow == 1:
                    strfr = self._fileReader.userowInd(0)
                    print(strfr + "ˇ")
                else:
                    print("err: %s" % self._fileReader.userowInd(codeRow - 2))
                    strn1 = self._fileReader.userowInd(codeRow - 1)
                    print(strn1 + "ˇ")
                print()
                if codeRow < codeSize:
                    print("err: %s" % self._fileReader.userowInd(codeRow))
                raise GrammarError.GrammarError(keys, t)
