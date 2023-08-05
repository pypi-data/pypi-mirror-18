#coding=utf-8
from distutils.core import setup

setup(
    name='liuxiaohui_nester',
    version='1.0.4',
    py_modules=['liuxiaohui_nester'],
    author='heart4u',
    author_email='heart4u@163.com',
    url='http://www.2018studio.cn',
    description='''这是pester.py模块，提供了一个名为print_lol()的函数
用来打印列表，其中包含或不包含嵌套列表。并且会以缩
进的方式进行打印。增加参数indent决定是否使用缩进功
能，默认为关闭缩进。增加fn参数对输出进行重定向。'''
)
