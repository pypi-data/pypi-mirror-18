#! /usr/bin/python3

"""
This is module about headfirst practice dmeo
"""
def print_lol(the_list, level = 0):
    """
    the function is that print each item in the_list
    """
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, level + 1)
        else:
            for x in range(level):
                print('\t', end='')
            print(each_item)
