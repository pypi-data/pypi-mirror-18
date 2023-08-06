#! /usr/bin/python3

"""
This is module about headfirst practice dmeo
"""
def print_lol(the_list):
    """
    the function is that print each item in the_list
    """
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print(each_item)
