# -*- coding: utf-8 -*-
"""
Created on Mon Dec 05 15:44:30 2016

@author: Administrator
"""

"""
模板应该全部都是函数才好。
"""

def print_lol(the_list,level = 0):
    for item_in in the_list:
        if isinstance(item_in,list):
            print_lol(item_in,level+1)
        else:
            for tab_stop in range(level):
                print "\t",
            print item_in