from lexer import TokenType

class Token(object):

    def __init__(self, row=-1, col=-1, kind="ERROR", val="NULL"):
        """

        :param row: 行号
        :param col: 列号
        :param kind: 'KEY_WORD' and 'OP' and 'SYMBOL' and 'ID' and 'CONSTANT'
        :param val: 具体的内容
        """
        self._row = row
        self._col = col
        self._kind = kind
        self._val = val
        # self.say()

    @property
    def row(self):
        return self._row

    @row.setter
    def row(self, row):
        self._row = row

    @property
    def col(self):
        return self._col

    @col.setter
    def col(self, col):
        self._col = col

    @property
    def kind(self):
        return self._kind

    @kind.setter
    def kind(self, kind):
        self._kind = kind

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, val):
        self._val = val

    def say(self):
        print("I am Token!")
        self.row = 8

    # toString
    def __str__(self) -> str:
        return "Token {row=%s, col=%s, kind=%s, val='%s'}" % (self._row, self._col, self._kind, self._val)

    # toString
    def __repr__(self) -> str:
        return "Token {row=%s, col=%s, kind=%s, val='%s'}" % (self._row, self._col, self._kind, self._val)


if __name__ == '__main__':
    t1 = Token()
    print(t1.row)
    print(t1.col)
    print(t1.val)
    print(t1.kind)
    t1.row = 9
    t1.col = 5
    t1.kind = "CONST"
    t1.val = "1.1"
    print(t1.__str__())
    t2 = Token(1, 2, "ID", "fucku")
    tlist = []
    tlist.append(t1)
    tlist.append(t2)
    tlist.append(Token(10, 0, TokenType.TokenType.KEY_WORD.name, "for"))
