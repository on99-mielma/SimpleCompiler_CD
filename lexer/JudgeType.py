import json
from lexer import TokenType
import regex as re


class JudgeType(object):
    def __init__(self, tjson):
        self._tjson = tjson
        self._KEY_WORD = tjson['KEY_WORD']
        self._OP = tjson['OP']
        self._SYMBOL = tjson['SYMBOL']
        self._CONSTANT = "^" + tjson['CONSTANT']
        self._ID = "^" + tjson['ID']

    @property
    def getKEY_WORD(self):
        return self._KEY_WORD

    @property
    def getOP(self):
        return self._OP

    @property
    def getSYMBOL(self):
        return self._SYMBOL

    @property
    def getCONSTNAT(self):
        return self._CONSTANT

    @property
    def getID(self):
        return self._ID

    def getTokenType(self, wordstr):
        if self._KEY_WORD.count(wordstr):
            return TokenType.TokenType.KEY_WORD
        if self._OP.count(wordstr):
            return TokenType.TokenType.OP
        if self._SYMBOL.count(wordstr):
            return TokenType.TokenType.SYMBOL
        constantans = re.match(self._CONSTANT, wordstr)
        if constantans is not None and wordstr == constantans.group():
            return TokenType.TokenType.CONST
        idans = re.match(self._ID, wordstr)
        if idans is not None and wordstr == idans.group():
            return TokenType.TokenType.ID
        return TokenType.TokenType.ERROR

    def getAllType(self):
        print(type(self._KEY_WORD))
        print(type(self._OP))
        print(type(self._SYMBOL))
        print(type(self._CONSTANT))
        print(type(self._ID))

    def testReMatch(self, wordstr):
        ans = re.match(self._CONSTANT, wordstr)
        print(ans)
        # print(type(ans.span())) #tuple
        print(ans.span()[0])
        print(ans.span()[1])
        # print(len(ans.group()))
        # print(wordstr==ans.group())
        print("*" * 64)
        ans2 = re.match(self._ID, wordstr)
        print(ans2)
        print(ans2.span()[0])
        print(ans2.span()[1])


def main():
    with open('../lexer/config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    jt = JudgeType(config)
    print('*' * 64)
    print(jt.getKEY_WORD)
    print(jt.getOP)
    print(jt.getSYMBOL)
    print(jt.getCONSTNAT)
    print(jt.getID)
    print('*' * 64)
    print(jt.getTokenType('public').name)
    print('*' * 64)
    # jt.testReMatch("= a + b * 2.4 + 1.2 - 1.2E+12;")
    # jt.testReMatch("")
    # jt.testReMatch("ccc3")
    # jt.testReMatch("1.1E+3.1")
    # jt.testReMatch("589.89123101+20.59453i")
    print("-"*64)
    print(jt.getOP.count("= "))


if __name__ == '__main__':
    main()
