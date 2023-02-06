import regex as re
import json
from lexer import JudgeType
from utils.file import FileReader
from lexer import Token
from lexer import TokenType


class Tokenizer(object):
    def __init__(self, configPath, filename, tokens=None):
        """

        :param configPath: 'KEY_WORD' and 'OP' and 'SYMBOL' and 'ID' and 'CONSTANT' config setup json path
        :param filename: test file path
        :param tokens: 保存Token的list
        """
        if tokens is None:
            self._tokens = []
        self._configPath = configPath
        try:
            with open(configPath, 'r', encoding='utf-8') as f:
                config = json.load(f)
            self._judgetype = JudgeType.JudgeType(config)
        except FileNotFoundError:
            print('无法打开指定的文件!')
        except LookupError:
            print('指定了未知的编码!')
        except UnicodeDecodeError:
            print('读取文件时解码错误!')
        finally:
            f.close()

        self._codeRow = FileReader.FileReader(filename=filename)
        self.genTokens()
        self.checkTokens()

    @property
    def configPath(self):
        return self._configPath

    @configPath.setter
    def configPath(self, c):
        self._configPath = c

    @property
    def judgetype(self):
        return self._judgetype

    @judgetype.setter
    def judgetype(self, j):
        self._judgetype = j

    @property
    def codeRow(self):
        return self._codeRow

    @codeRow.setter
    def codeRow(self, c):
        self._codeRow = c

    @property
    def tokens(self):
        return self._tokens

    @tokens.setter
    def tokens(self, t):
        self._tokens = t

    def genTokens(self):
        """

        :return: 生成Token并且加入到tokens中
        """
        global code
        code = self._codeRow.nextRow()
        isNoteState = False
        while code is not None:
            if len(code) == 0:
                code = self._codeRow.nextRow()
                continue
            word = ""
            # for ii in range(len(code)):
            ii = 0
            while ii < len(code):
                c = code[ii]
                while self.isBlank(c):
                    ii += 1
                    c = code[ii]
                if isNoteState == False and ii < len(code) - 1 and c == '/' and code[ii + 1] == '*':
                    isNoteState = True
                    ii += 1
                    if len(word) != 0:
                        self._tokens.append(Token.Token(self._codeRow.rowInd, ii, self.judgetype.getTokenType(word).name, word))
                        word = ""
                    ii += 1
                    continue
                if isNoteState == True:
                    if ii < len(code) - 1 and c == '*' and code[ii + 1] == '/':
                        isNoteState = False
                        break
                    ii += 1
                    continue
                if ii < len(code) - 1 and c == '/' and code[ii + 1] == '/':
                    if len(word) != 0:
                        self._tokens.append(Token.Token(self._codeRow.rowInd, ii, self.judgetype.getTokenType(word).name, word))
                    break
                flag = True
                patternList = [self.judgetype.getCONSTNAT, self.judgetype.getID]
                for pattern in patternList:
                    matchans = re.match(pattern, code[ii:])
                    if matchans is not None and matchans.span()[1] != 0:
                        flag = False
                        tempString = code[ii:ii + matchans.span()[1]]
                        self._tokens.append(Token.Token(self._codeRow.rowInd, ii + 1, self.judgetype.getTokenType(tempString).name, tempString))
                        ii = ii + matchans.span()[1] - 1
                        if len(word) != 0:
                            self._tokens.append(Token.Token(self._codeRow.rowInd, ii + 1, self.judgetype.getTokenType(word).name, word))
                            word = ""
                        break
                if flag == True:
                    word += c
                    if ii < len(code) - 1 and self.judgetype.getOP.count(word + code[ii + 1]) != 0:
                        self._tokens.append(Token.Token(self._codeRow.rowInd, ii + 1, self.judgetype.getTokenType(word + code[ii + 1]).name, word + code[ii + 1]))
                        ii += 1
                    else:
                        self._tokens.append(Token.Token(self._codeRow.rowInd, ii + 1, self.judgetype.getTokenType(word).name, word))
                    word = ""
                ii += 1
            code = self._codeRow.nextRow()

    def checkTokens(self):
        """

        :return: 如果TokenType是ERROR则打印错误日志
        """
        for t in self._tokens:
            if t.kind == TokenType.TokenType.ERROR.name:
                print("ERROROROROROROR!")

    def isBlank(self, c):
        """

        :param c: 传入长度只能为1的字符串
        :return: True or False
        """
        return c == ' ' or c == '\t' or c == '\n'


if __name__ == '__main__':
    tn = Tokenizer("../lexer/config.json", "../lexer/test.txt")
    print(len(tn.tokens))
    for i in tn.tokens:
        print(i)
