from lexer import Token


class TokenException(Exception):
    _REMINDEXCEPTION = "词法分析 TOKEN出错"

    def __init__(self, t: Token.Token = None, error: str = None):
        if t is None and error is None:
            Exception.__init__(self, self._REMINDEXCEPTION)
        elif error is None:
            Exception.__init__(self, "TokenException{row=%s, col=%s, val=%s, error=%s}" % (
                t.row, t.col, t.val, self._REMINDEXCEPTION))
        else:
            Exception.__init__(self, "TokenException{row=%s, col=%s, val=%s, error=%s : %s }" % (
            t.row, t.col, t.val, self._REMINDEXCEPTION, error))
