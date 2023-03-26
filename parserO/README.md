# 语法分析

LR(1)

将配置文件中的语法设置抽象出来形成相应的终结符列表，非终结符列表，ItemSet项目集族，ActionGoto表项目集族并配合上部分词法分析生成的Token总序列来配合生成抽象语法树并且配合上部分进行词法分析的错误发生位置的判断。

对配置文件解析如下(未加入终结符与终结符标识):

![Start](..\parserO\Start.png)



那么通过此构建预测分析表

示例如下:

配置文件:

```json
{
  "production": [
    { "left": "START", "right": ["S"] },
    { "left": "S", "right": ["CLASS_S","S"] },
    { "left": "S", "right": ["FUNC_S","S"] },
    { "left": "S", "right": [] },

    { "left": "CLASS_S", "right": ["FIELD_TYPE","class","ID","{","CLASS_BODY","}"] },
    { "left": "FUNC_S", "right": ["function","TYPEDEF","ID","(","ARGS",")","{","BLOCK_STMT","}"] },

    { "left": "FIELD_TYPE", "right": [] },
    { "left": "FIELD_TYPE", "right": ["public"] },
    { "left": "FIELD_TYPE", "right": ["private"] },
    { "left": "FIELD_TYPE", "right": ["protected"] },
    { "left": "OPTIONAL_FIELD_TYPE", "right": [] },
    { "left": "OPTIONAL_FIELD_TYPE", "right": ["static"] },
    { "left": "OPTIONAL_FIELD_TYPE", "right": ["final"] },

    { "left": "TYPEDEF", "right": ["ID"] },
    { "left": "TYPEDEF", "right": ["CONST_TYPE"] },

    { "left": "CONST_TYPE", "right": ["void"] },
    { "left": "CONST_TYPE", "right": ["char"] },
    { "left": "CONST_TYPE", "right": ["bool"] },
    { "left": "CONST_TYPE", "right": ["short"] },
    { "left": "CONST_TYPE", "right": ["int"] },
    { "left": "CONST_TYPE", "right": ["long"] },
    { "left": "CONST_TYPE", "right": ["double"] },
    { "left": "CONST_TYPE", "right": ["float"] },
    { "left": "CONST_TYPE", "right": ["var"] },

    { "left": "DECLARE_INTER", "right": ["TYPEDEF","ID","DECLARE_INIT","DECLARE_VARS",";"] },
    { "left": "DECLARE_CLASS", "right": ["FIELD_TYPE","OPTIONAL_FIELD_TYPE","TYPEDEF","ID","DECLARE_INIT","DECLARE_VARS",";"] },
    { "left": "METHOD_CLASS", "right": ["FIELD_TYPE","OPTIONAL_FIELD_TYPE","TYPEDEF","ID","(","ARGS",")","{","BLOCK_STMT","}"] },
    { "left": "METHOD_CLASS", "right": ["FIELD_TYPE","OPTIONAL_FIELD_TYPE","TYPEDEF","main","(","ARGS",")","{","BLOCK_STMT","}"] },


    { "left": "DECLARE_INIT", "right": [] },
    { "left": "DECLARE_INIT", "right": ["=","EXPRESSION"] },
    { "left": "DECLARE_VARS", "right": [] },
    { "left": "DECLARE_VARS", "right": [",","ID","DECLARE_INIT","DECLARE_VARS"] },

    { "left": "ARGS", "right": [] },
    { "left": "ARGS", "right": ["TYPEDEF","ID","ARG"] },
    { "left": "ARG", "right": [] },
    { "left": "ARG", "right": [",","TYPEDEF","ID","ARG"] },

    { "left": "EXPRESSION", "right": ["VALUE"] },
    { "left": "EXPRESSION", "right": ["(","EXPRESSION",")"] },
    { "left": "EXPRESSION", "right": ["EXPRESSION","OPERATION","EXPRESSION"] },

    { "left": "VALUE", "right": ["CONSTANT"] },
    { "left": "VALUE", "right": ["OPERATION_SPECIAL","ID","OPERATION_SPECIAL"] },

    { "left": "OPERATION_SPECIAL", "right": [] },
    { "left": "OPERATION_SPECIAL", "right": ["++"] },
    { "left": "OPERATION_SPECIAL", "right": ["--"] },

    { "left": "OPERATION", "right": ["OPERATION_CAL"] },
    { "left": "OPERATION", "right": ["OPERATION_CMP"] },
    { "left": "OPERATION", "right": ["OPERATION_EQ"] },
    { "left": "OPERATION", "right": ["OPERATION_LOG"] },
    { "left": "OPERATION_CAL", "right": [","] },
    { "left": "OPERATION_CAL", "right": ["+"] },
    { "left": "OPERATION_CAL", "right": ["-"] },
    { "left": "OPERATION_CAL", "right": ["*"] },
    { "left": "OPERATION_CAL", "right": ["/"] },
    { "left": "OPERATION_CAL", "right": ["%"] },
    { "left": "OPERATION_CAL", "right": ["|"] },
    { "left": "OPERATION_CAL", "right": ["&"] },
    { "left": "OPERATION_CAL", "right": ["~"] },
    { "left": "OPERATION_CAL", "right": ["^"] },
    { "left": "OPERATION_EQ", "right": ["="] },
    { "left": "OPERATION_EQ", "right": ["+="] },
    { "left": "OPERATION_EQ", "right": ["-="] },
    { "left": "OPERATION_EQ", "right": ["*="] },
    { "left": "OPERATION_EQ", "right": ["/="] },
    { "left": "OPERATION_EQ", "right": ["%="] },
    { "left": "OPERATION_CMP", "right": ["<"] },
    { "left": "OPERATION_CMP", "right": [">"] },
    { "left": "OPERATION_CMP", "right": ["=="] },
    { "left": "OPERATION_CMP", "right": ["!="] },
    { "left": "OPERATION_CMP", "right": ["<="] },
    { "left": "OPERATION_CMP", "right": [">="] },
    { "left": "OPERATION_LOG", "right": ["!"] },
    { "left": "OPERATION_LOG", "right": ["&&"] },
    { "left": "OPERATION_LOG", "right": ["||"] },

    { "left": "IF_STMT", "right": ["if","(","EXPRESSION",")","{","BLOCK_STMT","}","ELSE_IF_STMT"] },
    { "left": "ELSE_IF_STMT", "right": [] },
    { "left": "ELSE_IF_STMT", "right": ["else","IF_STMT"] },
    { "left": "ELSE_IF_STMT", "right": ["else","{","BLOCK_STMT","}"] },

    { "left": "FOR_STMT", "right": ["for","(","FOR_EXPRESSION",";","EXPRESSION",";","EXPRESSION",")","{","BLOCK_STMT","}"] },
    { "left": "FOR_EXPRESSION", "right": ["EXPRESSION"] },
    { "left": "FOR_EXPRESSION", "right": ["TYPEDEF","ID","DECLARE_INIT","DECLARE_VARS"] },

    { "left": "WHILE_STMT", "right": ["while","(","EXPRESSION",")","{","BLOCK_STMT","}"] },

    { "left": "DO_WHILE_STMT", "right": ["do","{","BLOCK_STMT","}","while","(","EXPRESSION",")",";"] },

    { "left": "PRINT_STMT", "right": ["print","(","EXPRESSION",")",";"] },
    { "left": "RETURN_STMT", "right": ["return","EXPRESSION",";"] },


    { "left": "CLASS_BODY", "right": [] },
    { "left": "CLASS_BODY", "right": ["CLASS_BODY_TMP","CLASS_BODY"] },
    { "left": "CLASS_BODY_TMP", "right": ["DECLARE_CLASS"] },
    { "left": "CLASS_BODY_TMP", "right": ["METHOD_CLASS"] },

    { "left": "BLOCK_STMT", "right": [] },
    { "left": "BLOCK_STMT", "right": ["BLOCK_STMT_TMP","BLOCK_STMT"] },
    { "left": "BLOCK_STMT_TMP", "right": ["DECLARE_INTER"] },
    { "left": "BLOCK_STMT_TMP", "right": ["EXPRESSION",";"] },
    { "left": "BLOCK_STMT_TMP", "right": ["IF_STMT"] },
    { "left": "BLOCK_STMT_TMP", "right": ["FOR_STMT"] },
    { "left": "BLOCK_STMT_TMP", "right": ["WHILE_STMT"] },
    { "left": "BLOCK_STMT_TMP", "right": ["DO_WHILE_STMT"] },
    { "left": "BLOCK_STMT_TMP", "right": ["PRINT_STMT"] },
    { "left": "BLOCK_STMT_TMP", "right": ["RETURN_STMT"] }

  ]
}
```

生成ItemSet如下（截取部分):

```
ItemSet{id=0, shiftItem={'S': 1, 'CLASS_S': 2, 'FUNC_S': 3, 'FIELD_TYPE': 4, 'function': 5, 'public': 6, 'private': 7, 'protected': 8}, itemList=[Item{index=0, p=ProductionAtom{left='START', right='['S']'}, forword=None}
, Item{index=0, p=ProductionAtom{left='S', right='['CLASS_S', 'S']'}, forword=None}
, Item{index=0, p=ProductionAtom{left='S', right='['FUNC_S', 'S']'}, forword=None}
, Item{index=0, p=ProductionAtom{left='S', right='[]'}, forword=None}
, Item{index=0, p=ProductionAtom{left='CLASS_S', right='['FIELD_TYPE', 'class', 'ID', '{', 'CLASS_BODY', '}']'}, forword=FirstSetData{data=<< {'public', 'protected', 'class', 'private', 'function'} >>, endToken='True'}}
, Item{index=0, p=ProductionAtom{left='FUNC_S', right='['function', 'TYPEDEF', 'ID', '(', 'ARGS', ')', '{', 'BLOCK_STMT', '}']'}, forword=FirstSetData{data=<< {'public', 'protected', 'class', 'private', 'function'} >>, endToken='True'}}
, Item{index=0, p=ProductionAtom{left='FIELD_TYPE', right='[]'}, forword=FirstSetData{data=<< {'class'} >>, endToken='False'}}
, Item{index=0, p=ProductionAtom{left='FIELD_TYPE', right='['public']'}, forword=FirstSetData{data=<< {'class'} >>, endToken='False'}}
, Item{index=0, p=ProductionAtom{left='FIELD_TYPE', right='['private']'}, forword=FirstSetData{data=<< {'class'} >>, endToken='False'}}
, Item{index=0, p=ProductionAtom{left='FIELD_TYPE', right='['protected']'}, forword=FirstSetData{data=<< {'class'} >>, endToken='False'}}
]}


ItemSet{id=1, shiftItem={}, itemList=[Item{index=1, p=ProductionAtom{left='START', right='['S']'}, forword=None}
]}


ItemSet{id=2, shiftItem={'S': 9, 'CLASS_S': 2, 'FUNC_S': 3, 'FIELD_TYPE': 4, 'function': 5, 'public': 6, 'private': 7, 'protected': 8}, itemList=[Item{index=1, p=ProductionAtom{left='S', right='['CLASS_S', 'S']'}, forword=None}
, Item{index=0, p=ProductionAtom{left='S', right='['CLASS_S', 'S']'}, forword=None}
, Item{index=0, p=ProductionAtom{left='S', right='['FUNC_S', 'S']'}, forword=None}
, Item{index=0, p=ProductionAtom{left='S', right='[]'}, forword=None}
, Item{index=0, p=ProductionAtom{left='CLASS_S', right='['FIELD_TYPE', 'class', 'ID', '{', 'CLASS_BODY', '}']'}, forword=FirstSetData{data=<< {'public', 'protected', 'class', 'private', 'function'} >>, endToken='True'}}
, Item{index=0, p=ProductionAtom{left='FUNC_S', right='['function', 'TYPEDEF', 'ID', '(', 'ARGS', ')', '{', 'BLOCK_STMT', '}']'}, forword=FirstSetData{data=<< {'public', 'protected', 'class', 'private', 'function'} >>, endToken='True'}}
, Item{index=0, p=ProductionAtom{left='FIELD_TYPE', right='[]'}, forword=FirstSetData{data=<< {'class'} >>, endToken='False'}}
, Item{index=0, p=ProductionAtom{left='FIELD_TYPE', right='['public']'}, forword=FirstSetData{data=<< {'class'} >>, endToken='False'}}
, Item{index=0, p=ProductionAtom{left='FIELD_TYPE', right='['private']'}, forword=FirstSetData{data=<< {'class'} >>, endToken='False'}}
, Item{index=0, p=ProductionAtom{left='FIELD_TYPE', right='['protected']'}, forword=FirstSetData{data=<< {'class'} >>, endToken='False'}}
]}


ItemSet{id=3, shiftItem={'S': 10, 'CLASS_S': 2, 'FUNC_S': 3, 'FIELD_TYPE': 4, 'function': 5, 'public': 6, 'private': 7, 'protected': 8}, itemList=[Item{index=1, p=ProductionAtom{left='S', right='['FUNC_S', 'S']'}, forword=None}
, Item{index=0, p=ProductionAtom{left='S', right='['CLASS_S', 'S']'}, forword=None}
, Item{index=0, p=ProductionAtom{left='S', right='['FUNC_S', 'S']'}, forword=None}
, Item{index=0, p=ProductionAtom{left='S', right='[]'}, forword=None}
, Item{index=0, p=ProductionAtom{left='CLASS_S', right='['FIELD_TYPE', 'class', 'ID', '{', 'CLASS_BODY', '}']'}, forword=FirstSetData{data=<< {'public', 'protected', 'class', 'private', 'function'} >>, endToken='True'}}
, Item{index=0, p=ProductionAtom{left='FUNC_S', right='['function', 'TYPEDEF', 'ID', '(', 'ARGS', ')', '{', 'BLOCK_STMT', '}']'}, forword=FirstSetData{data=<< {'public', 'protected', 'class', 'private', 'function'} >>, endToken='True'}}
, Item{index=0, p=ProductionAtom{left='FIELD_TYPE', right='[]'}, forword=FirstSetData{data=<< {'class'} >>, endToken='False'}}
, Item{index=0, p=ProductionAtom{left='FIELD_TYPE', right='['public']'}, forword=FirstSetData{data=<< {'class'} >>, endToken='False'}}
, Item{index=0, p=ProductionAtom{left='FIELD_TYPE', right='['private']'}, forword=FirstSetData{data=<< {'class'} >>, endToken='False'}}
, Item{index=0, p=ProductionAtom{left='FIELD_TYPE', right='['protected']'}, forword=FirstSetData{data=<< {'class'} >>, endToken='False'}}
]}

```

生成的ActionGoto表如下（部分):

```
ActionGoto{id=0, op={'S': 1, 'CLASS_S': 2, 'FUNC_S': 3, 'FIELD_TYPE': 4, 'function': 5, 'public': 6, 'private': 7, 'protected': 8, None: ProductionAtom{left='S', right='[]'}, 'class': ProductionAtom{left='FIELD_TYPE', right='[]'}}}

ActionGoto{id=1, op={None: ProductionAtom{left='START', right='['S']'}}}

ActionGoto{id=2, op={'S': 9, 'CLASS_S': 2, 'FUNC_S': 3, 'FIELD_TYPE': 4, 'function': 5, 'public': 6, 'private': 7, 'protected': 8, None: ProductionAtom{left='S', right='[]'}, 'class': ProductionAtom{left='FIELD_TYPE', right='[]'}}}

ActionGoto{id=3, op={'S': 10, 'CLASS_S': 2, 'FUNC_S': 3, 'FIELD_TYPE': 4, 'function': 5, 'public': 6, 'private': 7, 'protected': 8, None: ProductionAtom{left='S', right='[]'}, 'class': ProductionAtom{left='FIELD_TYPE', right='[]'}}}

ActionGoto{id=4, op={'class': 11}}

ActionGoto{id=5, op={'TYPEDEF': 12, 'ID': 13, 'CONST_TYPE': 14, 'void': 15, 'char': 16, 'bool': 17, 'short': 18, 'int': 19, 'long': 20, 'double': 21, 'float': 22, 'var': 23}}

ActionGoto{id=6, op={'class': ProductionAtom{left='FIELD_TYPE', right='['public']'}}}

ActionGoto{id=7, op={'class': ProductionAtom{left='FIELD_TYPE', right='['private']'}}}

ActionGoto{id=8, op={'class': ProductionAtom{left='FIELD_TYPE', right='['protected']'}}}

ActionGoto{id=9, op={None: ProductionAtom{left='S', right='['CLASS_S', 'S']'}}}

ActionGoto{id=10, op={None: ProductionAtom{left='S', right='['FUNC_S', 'S']'}}}

ActionGoto{id=11, op={'ID': 24}}

ActionGoto{id=12, op={'ID': 25}}
```

部分LR（1）分析过程如下：

```
[0]                                                                                                 	[]                                                                                                  	class
[0, 4]                                                                                              	['FIELD_TYPE']                                                                                      	class
[0, 4, 11]                                                                                          	['FIELD_TYPE', 'class']                                                                             	ID
[0, 4, 11, 24]                                                                                      	['FIELD_TYPE', 'class', 'ID']                                                                       	{
[0, 4, 11, 24, 26]                                                                                  	['FIELD_TYPE', 'class', 'ID', '{']                                                                  	public
[0, 4, 11, 24, 26, 33]                                                                              	['FIELD_TYPE', 'class', 'ID', '{', 'public']                                                        	int
[0, 4, 11, 24, 26, 32]                                                                              	['FIELD_TYPE', 'class', 'ID', '{', 'FIELD_TYPE']                                                    	int
[0, 4, 11, 24, 26, 32, 40]                                                                          	['FIELD_TYPE', 'class', 'ID', '{', 'FIELD_TYPE', 'OPTIONAL_FIELD_TYPE']                             	int
[0, 4, 11, 24, 26, 32, 40, 52]                                                                      	['FIELD_TYPE', 'class', 'ID', '{', 'FIELD_TYPE', 'OPTIONAL_FIELD_TYPE', 'int']                      	ID
[0, 4, 11, 24, 26, 32, 40, 47]                                                                      	['FIELD_TYPE', 'class', 'ID', '{', 'FIELD_TYPE', 'OPTIONAL_FIELD_TYPE', 'CONST_TYPE']               	ID
[0, 4, 11, 24, 26, 32, 40, 45]                                                                      	['FIELD_TYPE', 'class', 'ID', '{', 'FIELD_TYPE', 'OPTIONAL_FIELD_TYPE', 'TYPEDEF']                  	ID
[0, 4, 11, 24, 26, 32, 40, 45, 60]                                                                  	['FIELD_TYPE', 'class', 'ID', '{', 'FIELD_TYPE', 'OPTIONAL_FIELD_TYPE', 'TYPEDEF', 'ID']            	=
[0, 4, 11, 24, 26, 32, 40, 45, 60, 88]                                                              	['FIELD_TYPE', 'class', 'ID', '{', 'FIELD_TYPE', 'OPTIONAL_FIELD_TYPE', 'TYPEDEF', 'ID', '=']       	CONSTANT
[0, 4, 11, 24, 26, 32, 40, 45, 60, 88, 143]                                                         	['FIELD_TYPE', 'class', 'ID', '{', 'FIELD_TYPE', 'OPTIONAL_FIELD_TYPE', 'TYPEDEF', 'ID', '=', 'CONSTANT']	;
[0, 4, 11, 24, 26, 32, 40, 45, 60, 88, 141]                                                         	['FIELD_TYPE', 'class', 'ID', '{', 'FIELD_TYPE', 'OPTIONAL_FIELD_TYPE', 'TYPEDEF', 'ID', '=', 'VALUE']	;
[0, 4, 11, 24, 26, 32, 40, 45, 60, 88, 140]                                                         	['FIELD_TYPE', 'class', 'ID', '{', 'FIELD_TYPE', 'OPTIONAL_FIELD_TYPE', 'TYPEDEF', 'ID', '=', 'EXPRESSION']	;
[0, 4, 11, 24, 26, 32, 40, 45, 60, 86]                                                              	['FIELD_TYPE', 'class', 'ID', '{', 'FIELD_TYPE', 'OPTIONAL_FIELD_TYPE', 'TYPEDEF', 'ID', 'DECLARE_INIT']	;
[0, 4, 11, 24, 26, 32, 40, 45, 60, 86, 137]                                                         	['FIELD_TYPE', 'class', 'ID', '{', 'FIELD_TYPE', 'OPTIONAL_FIELD_TYPE', 'TYPEDEF', 'ID', 'DECLARE_INIT', 'DECLARE_VARS']	;
[0, 4, 11, 24, 26, 32, 40, 45, 60, 86, 137, 164]                                                    	['FIELD_TYPE', 'class', 'ID', '{', 'FIELD_TYPE', 'OPTIONAL_FIELD_TYPE', 'TYPEDEF', 'ID', 'DECLARE_INIT', 'DECLARE_VARS', ';']	private
[0, 4, 11, 24, 26, 30]                                                                              	['FIELD_TYPE', 'class', 'ID', '{', 'DECLARE_CLASS']                                                 	private
[0, 4, 11, 24, 26, 29]                                                                              	['FIELD_TYPE', 'class', 'ID', '{', 'CLASS_BODY_TMP']                                                	private
[0, 4, 11, 24, 26, 29, 34]                                                                          	['FIELD_TYPE', 'class', 'ID', '{', 'CLASS_BODY_TMP', 'private']                                     	double
[0, 4, 11, 24, 26, 29, 32]                                                                          	['FIELD_TYPE', 'class', 'ID', '{', 'CLASS_BODY_TMP', 'FIELD_TYPE']                                  	double
[0, 4, 11, 24, 26, 29, 32, 40]                                                                      	['FIELD_TYPE', 'class', 'ID', '{', 'CLASS_BODY_TMP', 'FIELD_TYPE', 'OPTIONAL_FIELD_TYPE']           	double
[0, 4, 11, 24, 26, 29, 32, 40, 54]                                                                  	['FIELD_TYPE', 'class', 'ID', '{', 'CLASS_BODY_TMP', 'FIELD_TYPE', 'OPTIONAL_FIELD_TYPE', 'double'] 	ID
[0, 4, 11, 24, 26, 29, 32, 40, 47]                                                                  	['FIELD_TYPE', 'class', 'ID', '{', 'CLASS_BODY_TMP', 'FIELD_TYPE', 'OPTIONAL_FIELD_TYPE', 'CONST_TYPE']	ID
[0, 4, 11, 24, 26, 29, 32, 40, 45]                                                                  	['FIELD_TYPE', 'class', 'ID', '{', 'CLASS_BODY_TMP', 'FIELD_TYPE', 'OPTIONAL_FIELD_TYPE', 'TYPEDEF']	ID
[0, 4, 11, 24, 26, 29, 32, 40, 45, 60]                                                              	['FIELD_TYPE', 'class', 'ID', '{', 'CLASS_BODY_TMP', 'FIELD_TYPE', 'OPTIONAL_FIELD_TYPE', 'TYPEDEF', 'ID']	=
[0, 4, 11, 24, 26, 29, 32, 40, 45, 60, 88]                                                          	['FIELD_TYPE', 'class', 'ID', '{', 'CLASS_BODY_TMP', 'FIELD_TYPE', 'OPTIONAL_FIELD_TYPE', 'TYPEDEF', 'ID', '=']	CONSTANT
[0, 4, 11, 24, 26, 29, 32, 40, 45, 60, 88, 143]                                                     	['FIELD_TYPE', 'class', 'ID', '{', 'CLASS_BODY_TMP', 'FIELD_TYPE', 'OPTIONAL_FIELD_TYPE', 'TYPEDEF', 'ID', '=', 'CONSTANT']	;
[0, 4, 11, 24, 26, 29, 32, 40, 45, 60, 88, 141]                                                     	['FIELD_TYPE', 'class', 'ID', '{', 'CLASS_BODY_TMP', 'FIELD_TYPE', 'OPTIONAL_FIELD_TYPE', 'TYPEDEF', 'ID', '=', 'VALUE']	;
[0, 4, 11, 24, 26, 29, 32, 40, 45, 60, 88, 140]                                                     	['FIELD_TYPE', 'class', 'ID', '{', 'CLASS_BODY_TMP', 'FIELD_TYPE', 'OPTIONAL_FIELD_TYPE', 'TYPEDEF', 'ID', '=', 'EXPRESSION']	;
[0, 4, 11, 24, 26, 29, 32, 40, 45, 60, 86]                                                          	['FIELD_TYPE', 'class', 'ID', '{', 'CLASS_BODY_TMP', 'FIELD_TYPE', 'OPTIONAL_FIELD_TYPE', 'TYPEDEF', 'ID', 'DECLARE_INIT']	;
[0, 4, 11, 24, 26, 29, 32, 40, 45, 60, 86, 137]                                                     	['FIELD_TYPE', 'class', 'ID', '{', 'CLASS_BODY_TMP', 'FIELD_TYPE', 'OPTIONAL_FIELD_TYPE', 'TYPEDEF', 'ID', 'DECLARE_INIT', 'DECLARE_VARS']	;
[0, 4, 11, 24, 26, 29, 32, 40, 45, 60, 86, 137, 164]                                                	['FIELD_TYPE', 'class', 'ID', '{', 'CLASS_BODY_TMP', 'FIELD_TYPE', 'OPTIONAL_FIELD_TYPE', 'TYPEDEF', 'ID', 'DECLARE_INIT', 'DECLARE_VARS', ';']	protected
[0, 4, 11, 24, 26, 29, 30]                                                                          	['FIELD_TYPE', 'class', 'ID', '{', 'CLASS_BODY_TMP', 'DECLARE_CLASS']                               	protected
[0, 4, 11, 24, 26, 29, 29]                                                                          	['FIELD_TYPE', 'class', 'ID', '{', 'CLASS_BODY_TMP', 'CLASS_BODY_TMP']                              	protected
[0, 4, 11, 24, 26, 29, 29, 35]                                                                      	['FIELD_TYPE', 'class', 'ID', '{', 'CLASS_BODY_TMP', 'CLASS_BODY_TMP', 'protected']                 	bool
[0, 4, 11, 24, 26, 29, 29, 32]                                                                      	['FIELD_TYPE', 'class', 'ID', '{', 'CLASS_BODY_TMP', 'CLASS_BODY_TMP', 'FIELD_TYPE']                	bool
[0, 4, 11, 24, 26, 29, 29, 32, 40]                                                                  	['FIELD_TYPE', 'class', 'ID', '{', 'CLASS_BODY_TMP', 'CLASS_BODY_TMP', 'FIELD_TYPE', 'OPTIONAL_FIELD_TYPE']	bool
[0, 4, 11, 24, 26, 29, 29, 32, 40, 50]                                                              	['FIELD_TYPE', 'class', 'ID', '{', 'CLASS_BODY_TMP', 'CLASS_BODY_TMP', 'FIELD_TYPE', 'OPTIONAL_FIELD_TYPE', 'bool']	ID
[0, 4, 11, 24, 26, 29, 29, 32, 40, 47]                                                              	['FIELD_TYPE', 'class', 'ID', '{', 'CLASS_BODY_TMP', 'CLASS_BODY_TMP', 'FIELD_TYPE', 'OPTIONAL_FIELD_TYPE', 'CONST_TYPE']	ID
[0, 4, 11, 24, 26, 29, 29, 32, 40, 45]                                                              	['FIELD_TYPE', 'class', 'ID', '{', 'CLASS_BODY_TMP', 'CLASS_BODY_TMP', 'FIELD_TYPE', 'OPTIONAL_FIELD_TYPE', 'TYPEDEF']	ID
[0, 4, 11, 24, 26, 29, 29, 32, 40, 45, 60]                                                          	['FIELD_TYPE', 'class', 'ID', '{', 'CLASS_BODY_TMP', 'CLASS_BODY_TMP', 'FIELD_TYPE', 'OPTIONAL_FIELD_TYPE', 'TYPEDEF', 'ID']	=
[0, 4, 11, 24, 26, 29, 29, 32, 40, 45, 60, 88]                                                      	['FIELD_TYPE', 'class', 'ID', '{', 'CLASS_BODY_TMP', 'CLASS_BODY_TMP', 'FIELD_TYPE', 'OPTIONAL_FIELD_TYPE', 'TYPEDEF', 'ID', '=']	ID
[0, 4, 11, 24, 26, 29, 29, 32, 40, 45, 60, 88, 144]                                                 	['FIELD_TYPE', 'class', 'ID', '{', 'CLASS_BODY_TMP', 'CLASS_BODY_TMP', 'FIELD_TYPE', 'OPTIONAL_FIELD_TYPE', 'TYPEDEF', 'ID', '=', 'OPERATION_SPECIAL']	ID
[0, 4, 11, 24, 26, 29, 29, 32, 40, 45, 60, 88, 144, 169]                                            	['FIELD_TYPE', 'class', 'ID', '{', 'CLASS_BODY_TMP', 'CLASS_BODY_TMP', 'FIELD_TYPE', 'OPTIONAL_FIELD_TYPE', 'TYPEDEF', 'ID', '=', 'OPERATION_SPECIAL', 'ID']	;
[0, 4, 11, 24, 26, 29, 29, 32, 40, 45, 60, 88, 144, 169, 187]                                       	['FIELD_TYPE', 'class', 'ID', '{', 'CLASS_BODY_TMP', 'CLASS_BODY_TMP', 'FIELD_TYPE', 'OPTIONAL_FIELD_TYPE', 'TYPEDEF', 'ID', '=', 'OPERATION_SPECIAL', 'ID', 'OPERATION_SPECIAL']	;
[0, 4, 11, 24, 26, 29, 29, 32, 40, 45, 60, 88, 141]                                                 	['FIELD_TYPE', 'class', 'ID', '{', 'CLASS_BODY_TMP', 'CLASS_BODY_TMP', 'FIELD_TYPE', 'OPTIONAL_FIELD_TYPE', 'TYPEDEF', 'ID', '=', 'VALUE']	;
[0, 4, 11, 24, 26, 29, 29, 32, 40, 45, 60, 88, 140]                                                 	['FIELD_TYPE', 'class', 'ID', '{', 'CLASS_BODY_TMP', 'CLASS_BODY_TMP', 'FIELD_TYPE', 'OPTIONAL_FIELD_TYPE', 'TYPEDEF', 'ID', '=', 'EXPRESSION']	;
[0, 4, 11, 24, 26, 29, 29, 32, 40, 45, 60, 86]                                                      	['FIELD_TYPE', 'class', 'ID', '{', 'CLASS_BODY_TMP', 'CLASS_BODY_TMP', 'FIELD_TYPE', 'OPTIONAL_FIELD_TYPE', 'TYPEDEF', 'ID', 'DECLARE_INIT']	;
[0, 4, 11, 24, 26, 29, 29, 32, 40, 45, 60, 86, 137]                                                 	['FIELD_TYPE', 'class', 'ID', '{', 'CLASS_BODY_TMP', 'CLASS_BODY_TMP', 'FIELD_TYPE', 'OPTIONAL_FIELD_TYPE', 'TYPEDEF', 'ID', 'DECLARE_INIT', 'DECLARE_VARS']	;
[0, 4, 11, 24, 26, 29, 29, 32, 40, 45, 60, 86, 137, 164]                                            	['FIELD_TYPE', 'class', 'ID', '{', 'CLASS_BODY_TMP', 'CLASS_BODY_TMP', 'FIELD_TYPE', 'OPTIONAL_FIELD_TYPE', 'TYPEDEF', 'ID', 'DECLARE_INIT', 'DECLARE_VARS', ';']	void
[0, 4, 11, 24, 26, 29, 29, 30]                                                                      	['FIELD_TYPE', 'class', 'ID', '{', 'CLASS_BODY_TMP', 'CLASS_BODY_TMP', 'DECLARE_CLASS']             	void

```

