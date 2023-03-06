from lexer import Tokenizer


class Lexer(object):
    def __init__(self, configPath, filename):
        """

        :param configPath: 'KEY_WORD' and 'OP' and 'SYMBOL' and 'ID' and 'CONSTANT' config setup json path
        :param filename: test file path
        """
        self._filename = filename
        self._ti = Tokenizer.Tokenizer(configPath=configPath, filename=filename)

    @property
    def ti(self):
        """
        生成时间！
        :return: Check Tokenizer
        """
        return self._ti

    def getTokens(self):
        return self.ti.tokens

    @property
    def filename(self):
        return self._filename

    def printTokens(self):
        for t in self.getTokens():
            print(t)


if __name__ == '__main__':
    l = Lexer("../lexer/config.json", "../lexer/test.txt")
    l.printTokens()
