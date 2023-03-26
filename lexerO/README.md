# 词法分析

传入配置文件与代码文件，对代码文件逐行写入数组，并构造好相应的数据结构方便读取行内容以及行号

逐行逐字符读 满足条件就配置好相应的Token配置然后放入Token 序列  以此生成文法的全部Token序列

生成完毕后放入DFA进行检查

配置文件如下(JSON)

```json
{
  "KEY_WORD": ["class", "void", "function", "static",
    "private","public","protected",
    "char", "int", "boolean", "double", "bool","var",
    "val","if", "else", "while", "do", "for",
    "this", "return", "null", "print"],
  "OP": ["+", "-", "*", "/", "+=", "-=", "*=", "/=",
          "++", "--", "&", "|", "~", "&&", "||",
          "<", ">", "=", "<=", ">=", "==", "!="],
  "SYMBOL": [".", ",", ";", "(", ")", "[", "]", "{", "}"],
  "ID": "[_A-Za-z][_A-Za-z0-9]*",
  "CONSTANT": "((\"(.*)\")|('(\\\\)?[\\p{ASCII}]')|(\\d+(\\.\\d*)?i)|(\\d*(\\.)?\\d*(E([+\\-])\\d*(\\.)?\\d*)?)|false|true)"
}
```

DFA设计如下

![DFA](..\lexerO\DFA.png)

那么实例代码如下:

```
class TestClass{
    public int a = 1;
    private double d = 2.0;
    protected bool pd = false;//?
    /*
    ???
    */

    void main(){
    print(123);
    print("gogogogogogo");
    double u = 1.2E+12;
    double t = u + 2 * a / d;
    var testI = 5.64+2.3i;
    for( int i = 0 ; i < 99 ; i++){
           print(i);
    }
    if( u == t){
        print("IMPROSIABLE");
    }
    else{
        print("GOOD");
    }
    return a;

    }
}

function int test2(){
    char c = 1;
    while(c <= 125){
        c += 1;
    }
    return c;
}
```

生成Token序列如下:

```
Token {row=1, col=1, kind=KEY_WORD, val='class'}
Token {row=1, col=7, kind=ID, val='TestClass'}
Token {row=1, col=16, kind=SYMBOL, val='{'}
Token {row=2, col=5, kind=KEY_WORD, val='public'}
Token {row=2, col=12, kind=KEY_WORD, val='int'}
Token {row=2, col=16, kind=ID, val='a'}
Token {row=2, col=18, kind=OP, val='='}
Token {row=2, col=20, kind=CONST, val='1'}
Token {row=2, col=21, kind=SYMBOL, val=';'}
Token {row=3, col=5, kind=KEY_WORD, val='private'}
Token {row=3, col=13, kind=KEY_WORD, val='double'}
Token {row=3, col=20, kind=ID, val='d'}
Token {row=3, col=22, kind=OP, val='='}
Token {row=3, col=24, kind=CONST, val='2.0'}
Token {row=3, col=27, kind=SYMBOL, val=';'}
Token {row=4, col=5, kind=KEY_WORD, val='protected'}
Token {row=4, col=15, kind=KEY_WORD, val='bool'}
Token {row=4, col=20, kind=ID, val='pd'}
Token {row=4, col=23, kind=OP, val='='}
Token {row=4, col=25, kind=ID, val='false'}
Token {row=4, col=30, kind=SYMBOL, val=';'}
Token {row=9, col=5, kind=KEY_WORD, val='void'}
Token {row=9, col=10, kind=ID, val='main'}
Token {row=9, col=14, kind=SYMBOL, val='('}
Token {row=9, col=15, kind=SYMBOL, val=')'}
Token {row=9, col=16, kind=SYMBOL, val='{'}
Token {row=10, col=5, kind=KEY_WORD, val='print'}
Token {row=10, col=10, kind=SYMBOL, val='('}
Token {row=10, col=11, kind=CONST, val='123'}
Token {row=10, col=14, kind=SYMBOL, val=')'}
Token {row=10, col=15, kind=SYMBOL, val=';'}
Token {row=11, col=5, kind=KEY_WORD, val='print'}
Token {row=11, col=10, kind=SYMBOL, val='('}
Token {row=11, col=11, kind=CONST, val='"gogogogogogo"'}
Token {row=11, col=25, kind=SYMBOL, val=')'}
Token {row=11, col=26, kind=SYMBOL, val=';'}
Token {row=12, col=5, kind=KEY_WORD, val='double'}
Token {row=12, col=12, kind=ID, val='u'}
Token {row=12, col=14, kind=OP, val='='}
Token {row=12, col=16, kind=CONST, val='1.2E+12'}
Token {row=12, col=23, kind=SYMBOL, val=';'}
Token {row=13, col=5, kind=KEY_WORD, val='double'}
Token {row=13, col=12, kind=ID, val='t'}
Token {row=13, col=14, kind=OP, val='='}
Token {row=13, col=16, kind=ID, val='u'}
Token {row=13, col=18, kind=OP, val='+'}
Token {row=13, col=20, kind=CONST, val='2'}
Token {row=13, col=22, kind=OP, val='*'}
Token {row=13, col=24, kind=ID, val='a'}
Token {row=13, col=26, kind=OP, val='/'}
Token {row=13, col=28, kind=ID, val='d'}
Token {row=13, col=29, kind=SYMBOL, val=';'}
Token {row=14, col=5, kind=KEY_WORD, val='var'}
Token {row=14, col=9, kind=ID, val='testI'}
Token {row=14, col=15, kind=OP, val='='}
Token {row=14, col=17, kind=CONST, val='5.64'}
Token {row=14, col=21, kind=OP, val='+'}
Token {row=14, col=22, kind=CONST, val='2.3i'}
Token {row=14, col=26, kind=SYMBOL, val=';'}
Token {row=15, col=5, kind=KEY_WORD, val='for'}
Token {row=15, col=8, kind=SYMBOL, val='('}
Token {row=15, col=10, kind=KEY_WORD, val='int'}
Token {row=15, col=14, kind=ID, val='i'}
Token {row=15, col=16, kind=OP, val='='}
Token {row=15, col=18, kind=CONST, val='0'}
Token {row=15, col=20, kind=SYMBOL, val=';'}
Token {row=15, col=22, kind=ID, val='i'}
Token {row=15, col=24, kind=OP, val='<'}
Token {row=15, col=26, kind=CONST, val='99'}
Token {row=15, col=29, kind=SYMBOL, val=';'}
Token {row=15, col=31, kind=ID, val='i'}
Token {row=15, col=32, kind=OP, val='++'}
Token {row=15, col=34, kind=SYMBOL, val=')'}
Token {row=15, col=35, kind=SYMBOL, val='{'}
Token {row=16, col=12, kind=KEY_WORD, val='print'}
Token {row=16, col=17, kind=SYMBOL, val='('}
Token {row=16, col=18, kind=ID, val='i'}
Token {row=16, col=19, kind=SYMBOL, val=')'}
Token {row=16, col=20, kind=SYMBOL, val=';'}
Token {row=17, col=5, kind=SYMBOL, val='}'}
Token {row=18, col=5, kind=KEY_WORD, val='if'}
Token {row=18, col=7, kind=SYMBOL, val='('}
Token {row=18, col=9, kind=ID, val='u'}
Token {row=18, col=11, kind=OP, val='=='}
Token {row=18, col=14, kind=ID, val='t'}
Token {row=18, col=15, kind=SYMBOL, val=')'}
Token {row=18, col=16, kind=SYMBOL, val='{'}
Token {row=19, col=9, kind=KEY_WORD, val='print'}
Token {row=19, col=14, kind=SYMBOL, val='('}
Token {row=19, col=15, kind=CONST, val='"IMPROSIABLE"'}
Token {row=19, col=28, kind=SYMBOL, val=')'}
Token {row=19, col=29, kind=SYMBOL, val=';'}
Token {row=20, col=5, kind=SYMBOL, val='}'}
Token {row=21, col=5, kind=KEY_WORD, val='else'}
Token {row=21, col=9, kind=SYMBOL, val='{'}
Token {row=22, col=9, kind=KEY_WORD, val='print'}
Token {row=22, col=14, kind=SYMBOL, val='('}
Token {row=22, col=15, kind=CONST, val='"GOOD"'}
Token {row=22, col=21, kind=SYMBOL, val=')'}
Token {row=22, col=22, kind=SYMBOL, val=';'}
Token {row=23, col=5, kind=SYMBOL, val='}'}
Token {row=24, col=5, kind=KEY_WORD, val='return'}
Token {row=24, col=12, kind=ID, val='a'}
Token {row=24, col=13, kind=SYMBOL, val=';'}
Token {row=26, col=5, kind=SYMBOL, val='}'}
Token {row=27, col=1, kind=SYMBOL, val='}'}
Token {row=29, col=1, kind=KEY_WORD, val='function'}
Token {row=29, col=10, kind=KEY_WORD, val='int'}
Token {row=29, col=14, kind=ID, val='test2'}
Token {row=29, col=19, kind=SYMBOL, val='('}
Token {row=29, col=20, kind=SYMBOL, val=')'}
Token {row=29, col=21, kind=SYMBOL, val='{'}
Token {row=30, col=5, kind=KEY_WORD, val='char'}
Token {row=30, col=10, kind=ID, val='c'}
Token {row=30, col=12, kind=OP, val='='}
Token {row=30, col=14, kind=CONST, val='1'}
Token {row=30, col=15, kind=SYMBOL, val=';'}
Token {row=31, col=5, kind=KEY_WORD, val='while'}
Token {row=31, col=10, kind=SYMBOL, val='('}
Token {row=31, col=11, kind=ID, val='c'}
Token {row=31, col=13, kind=OP, val='<='}
Token {row=31, col=16, kind=CONST, val='125'}
Token {row=31, col=19, kind=SYMBOL, val=')'}
Token {row=31, col=20, kind=SYMBOL, val='{'}
Token {row=32, col=9, kind=ID, val='c'}
Token {row=32, col=11, kind=OP, val='+='}
Token {row=32, col=14, kind=CONST, val='1'}
Token {row=32, col=15, kind=SYMBOL, val=';'}
Token {row=33, col=5, kind=SYMBOL, val='}'}
Token {row=34, col=5, kind=KEY_WORD, val='return'}
Token {row=34, col=12, kind=ID, val='c'}
Token {row=34, col=13, kind=SYMBOL, val=';'}
Token {row=35, col=1, kind=SYMBOL, val='}'}
```

