#! /usr/bin/python3
import sys
"""
This is module about headfirst practice dmeo
"""
def print_lol(the_list, indent = False, level = 0, file = sys.stdout):
    """
    the function is that print each item in the_list
    """
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level + 1, file)
        else:
            if indent:
                for x in range(level):
                    print('\t', end='', file=file)
            print(each_item, file=file)
