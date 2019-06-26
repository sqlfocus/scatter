#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
模块总体注释，说明
 1. 模块引用按字典排序，整体引用在前，部分引用在后
 2. 变量采用linux内核命名方式，以"_"拼接的小写单词组
 3. 行前填充以4空格为单位，不能使用TAB
 4. 单行长度尽量控制在80字符
'''

#整体引用
import math
import os
import sys
#部分引用
from os import system as _system
from os import *               #<TK!!!>尽量避免使用此类型引用



def arg_func():
    def test(kind, *args, **keywords):
        for arg in args:
            pass
        for kw in keywords:
            pass       #<NOTE>print(keywords[kw])
    #示例
    test("hi", 1, 2, arg1="w", arg2="d")

def arg_set_type_func():
    '''
    可以通过元信息指定函数参数类型，并约定返回值类型
    参数，':'后跟指定类型
    返回值，'->'后跟指定类型
    '''
    def test(ham: str, eggs: str = 'eggs') -> str:
        return test.__annotations__  #此dict包含参数信息
    #示例
    #{'ham': <class 'str'>, 'eggs': <class 'str'>, 'return': <class 'str'>}
    test('spam')

def else_func():
    '''简单介绍else的使用场景'''
    for i in range(5):
        for j in range(5):
            if j == 3:
                break          #breaks out of innermost enclosing
        else:
            print("NO PRINT")  #因此<TK!!!>当j=3，break后不会执行至此

    try:
        result = 1 / 1
    except ZeroDivisionError:
        print("division by zero!")
    else:                      #必须位于所有except后，当无异常时执行
        pass                   #<TK!!!>如果发生除0异常，则不进入此代码块
    finally:                   #无论异常与否，都执行
        pass

def for_func():
    #借助slice copy，可以在循环内修改数组
    #words will be ["hello", "hi", "hi", "hello"]
    words = ["hi", "hello"]
    for word in words[:]:
        words.insert(0, word)

    #依赖数字的遍历
    #i will be 0,1,2,3,4
    for i in range(0, 5, 1):   #起始值，终值，步长
        pass

    
def if_func():
    if True:
        pass
    elif False:
        pass
    else:        #<TK!!!>如果有elif，则此关键词不可少
        pass
    
def lamda_func():
    '''
    小匿名函数可以利用lamda创建，且被限制为单个表达式;
    lamda表达式具有闭包特性，可索引局部变量
    '''
    def make_incrementor(n):
        return lambda x: x + n
    #示例
    f = make_incrementor(42)
    f(0)     #42
    f(1)     #43
    
def ret_func():
    #pass        #无返回值，<NOTE>默认返回值为None
    #return 1    #单返回值
    #return 1,2  #多返回值，<NOTE>等价于return (1,2)
    return [1,2] #返回list
    
def main():
    '''
    函数注释：展示python的使用方法，并列举推荐方式
    '''
    #推荐几种字符串格式化方法
    say_hi = 'hello, "jack"'       #use ' if have " in string
    say_hi_r = r'C:\some\name'     #add "r" before string when "\" as normal character
    f'Results of the {say_hi} {math.pi:.3f}'   #结果: Results of the hello, "jack" 3.142
    'Results of the {} {:.3}'.format(say_hi, math.pi)
    'Results of the {0} {1:.3}'.format(say_hi, math.pi)
    'Results of the {word} {value:.3}'.format(word=say_hi, value=math.pi)
    tb = {'word': say_hi, 'value': math.pi}
    'Results of the {0[word]} {0[value]:.3}'.format(tb)

    #模块
    os.__name__                #打印模块名，os
    dir(os)                    #函数dir()，罗列模块定义的变量、函数等
    _system("ls > /dev/null")  #执行系统命令

    #小知识点
    arg_func()
    arg_set_type_func()
    else_func()
    for_func()
    if_func()
    lamda_func()
    ret_func()
    
if __name__ == "__main__":
    '''
    模块单独执行入口，或非正式单元测试用例
    '''
    sys.exit(main())
