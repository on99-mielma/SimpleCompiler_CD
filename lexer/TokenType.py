from enum import Enum


class TokenType(Enum):
    KEY_WORD = 1
    ID = 2
    CONST = 3
    SYMBOL = 4
    OP = 5
    ERROR = 6
