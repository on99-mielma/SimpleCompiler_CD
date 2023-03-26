import sys

if __name__ == '__main__':

    print('当前PYTHON版本为 {} '.format(sys.version))
    if sys.version_info.minor < 10:
        print("您使用的python版本似乎并不符合要求 (要求python >= 3.10)")
        exit(1)
    from lexerO import Lexer
    from parserO import AnalysisList

    lexer = Lexer.Lexer("lexerO/config.json", "test.txt")
    lexer.printTokens()
    print()
    print('=*' * 100)
    print()
    ana = AnalysisList.AnalysisList("parserO/config.json")
    print(ana.production)
    # print('[*]-' * 100)
    # print(ana.production.nonTerminal)
    # print(ana.production.terminal)
    # print('[*]-' * 100)
    ana.printItemSetList()
    ana.printActionGotoTable()
    anaCheck = ana.analyse(lexer=lexer)
    ana.printAnalysisTable()
