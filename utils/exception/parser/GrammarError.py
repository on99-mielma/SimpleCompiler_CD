# -*- coding:utf-8 -*-
# @Time : 2023/2/4 13:40
# @Author: Reborn
# @Project: SimpleCompilerCD
# @File : GrammarError.py
from lexer import Token


class GrammarError(Exception):
    _REMINDEXCEPTION = "语法分析出错"

    def __init__(self, keys: set, t: int | Token.Token):
        if isinstance(t, int):
            Exception.__init__(self, "GrammarException{row=%s, error=%s, expectr=%s, get=null}" % (t, self._REMINDEXCEPTION, keys))
        elif isinstance(t, Token.Token):
            Exception.__init__(self, "GrammarException{row=%s, col=%s, error=%s, expectr=%s, get=%s}" % (t.row, t.col, self._REMINDEXCEPTION, keys, t.val))
        else:
            Exception.__init__(self, self._REMINDEXCEPTION)


if __name__ == '__main__':
    raise GrammarError(keys=set(), t=678)
