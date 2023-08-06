# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 20:55:12 2016

@author: zhongjian
"""


"""从嵌套多层的列表中打印出单个数据"""
def diedai_list(the_list,tab):
    """用递归函数解决"""
    for i in the_list:
        if isinstance(i,list):
            print(diedai_list(i,tab+1))
        else:
            for add_tab in range(tab):
                print('\t',end='')
            print(i)