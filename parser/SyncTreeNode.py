# -*- coding:utf-8 -*-
# @Time : 2023/2/4 12:33
# @Author: Reborn
# @Project: SimpleCompilerCD
# @File : SyncTreeNode.py
from lexer import Token


class SyncTreeNode:
    __cnt = 1 # default 0 -> 1

    def __init__(self, val: str = None, child: list = None, token: Token.Token = None):
        self._val = val
        self._child = child
        self._id = self.__cnt
        # self.__cnt += 1
        self.get_cnt()
        self._token = token
        self._father: SyncTreeNode = None

    @classmethod
    def get_cnt(cls):
        cls.__cnt += 1
        # return cls.__cnt

    @property
    def id(self):
        return self._id

    @property
    def val(self):
        return self._val

    @property
    def child(self):
        return self._child

    @property
    def father(self):
        return self._father

    @property
    def child(self):
        return self._child

    @property
    def token(self):
        return self._token

    @father.setter
    def father(self, f):
        self._father = f

    def __str__(self) -> str:
        if self._father is None:
            return "SyncTreeNode{id=%s, val=~%s~, father=%s, token=%s, child=%s}" % (self._id, self._val, self._father, self._token, self._child)
        return "SyncTreeNode{id=%s, val=~%s~, father=%s, token=%s, child=%s}" % (self._id, self._val, self._father.val, self._token, self._child)

    def __repr__(self) -> str:
        if self._father is None:
            return "SyncTreeNode{id=%s, val=~%s~, father=%s, token=%s, child=%s}" % (self._id, self._val, self._father, self._token, self._child)
        return "SyncTreeNode{id=%s, val=~%s~, father=%s, token=%s, child=%s}" % (self._id, self._val, self._father.val, self._token, self._child)


if __name__ == '__main__':
    stn = SyncTreeNode()
    # print(stn.get_cnt())
    print(stn.id)
    print()
    stn2 = SyncTreeNode()
    stn3 = SyncTreeNode()
    # print(stn.get_cnt())
    # print(stn2.get_cnt())
    print(stn.id)
    print(stn2.id)
    stn3.father = stn2
    print(stn3.father.val)
    print(stn)
    print(stn2)
    print(stn3)
