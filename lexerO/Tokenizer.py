import regex as re
import json
from lexerO import JudgeType
from utils.file import FileReader
from lexerO import Token
from lexerO import TokenType
from utils.exception.lexer import TokenException


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
        """

        :return:获得读取配置文件中的具体配置返回的类
        """
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
        code = self._codeRow.nextRow()  # 读取代码行
        isNoteState = False  # 初始化注释状态检测
        while code is not None:  # 到最后一行超出下标会返回None 即是停止
            if len(code) == 0:  # 跳过空行
                code = self._codeRow.nextRow()
                continue
            word = ""
            # for ii in range(len(code)):
            ii = 0
            while ii < len(code):  # 读取行的每个字符
                c = code[ii]
                while self.isBlank(c):  # 跳过空字符
                    ii += 1
                    c = code[ii]
                if isNoteState == False and ii < len(code) - 1 and c == '/' and code[ii + 1] == '*':  # 检查进入注释状态
                    isNoteState = True
                    ii += 1
                    if len(word) != 0:  # 如果此时word里有东西而非空串 则进入生成Token阶段
                        self._tokens.append(
                            Token.Token(self._codeRow.rowInd, ii, self.judgetype.getTokenType(word).name, word))
                        word = ""  # 清空word串
                    ii += 1
                    continue
                if isNoteState == True:
                    if ii < len(code) - 1 and c == '*' and code[ii + 1] == '/':
                        isNoteState = False  # 跳出注释状态 直接终止此行检测 没有对后面再进行处理 即当*/后面仍然有事物则不会报错 如果后面有语句则会错失语句
                        break
                    ii += 1
                    continue
                if ii < len(code) - 1 and c == '/' and code[ii + 1] == '/':  # 另一种注释状态检查
                    if len(word) != 0:
                        self._tokens.append(
                            Token.Token(self._codeRow.rowInd, ii, self.judgetype.getTokenType(word).name, word))
                    break
                flag = True
                patternList = [self.judgetype.getCONSTNAT, self.judgetype.getID]  # 存放常量或id处理
                for pattern in patternList:
                    matchans = re.match(pattern, code[ii:])
                    if matchans is not None and matchans.span()[1] != 0:  # 匹配成功
                        flag = False  # 非标识符
                        tempString = code[ii:ii + matchans.span()[1]]  # 截取语句
                        self._tokens.append(
                            Token.Token(self._codeRow.rowInd, ii + 1, self.judgetype.getTokenType(tempString).name,
                                        tempString))
                        ii = ii + matchans.span()[1] - 1
                        if len(word) != 0:  # 要是word还有符号 那么写入token
                            self._tokens.append(
                                Token.Token(self._codeRow.rowInd, ii + 1, self.judgetype.getTokenType(word).name, word))
                            word = ""
                        break
                if flag == True:
                    word += c
                    if ii < len(code) - 1 and self.judgetype.getOP.count(word + code[ii + 1]) != 0:  # ++ --等两字符运算符 特判
                        self._tokens.append(Token.Token(self._codeRow.rowInd, ii + 1,
                                                        self.judgetype.getTokenType(word + code[ii + 1]).name,
                                                        word + code[ii + 1]))
                        ii += 1
                    else:
                        self._tokens.append(
                            Token.Token(self._codeRow.rowInd, ii + 1, self.judgetype.getTokenType(word).name, word))
                    word = ""
                ii += 1
            code = self._codeRow.nextRow()

    def checkTokens(self):
        """

        :return: 如果TokenType是ERROR则打印错误日志
        """
        for t in self._tokens:
            if t.kind == TokenType.TokenType.ERROR.name:
                raise TokenException.TokenException(t=t)

    def isBlank(self, c):
        """

        :param c: 传入长度只能为1的字符串
        :return: True or False
        """
        return c == ' ' or c == '\t' or c == '\n'


if __name__ == '__main__':
    tn = Tokenizer("../lexerO/config.json", "/test.txt")
    print(len(tn.tokens))
    for i in tn.tokens:
        print(i)
