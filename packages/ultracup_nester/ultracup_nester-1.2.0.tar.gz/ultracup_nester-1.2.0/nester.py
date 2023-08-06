""" This is the nested.py module that allows to print any level
of nested lists, if you have a list within a list within a list
this is your module
"""
def print_lol (the_list,level=0):
    """ This function takes a positional argument called "the_list", which
    is any Python list (of - possibly - nested lists). Each data item in the
    provided list is (recursively) printed to the screen on it's own line.
    And a level argument to indent the nested elements level times"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item,level+1)
        else:
            for tab_stop in range(level):
                print("\t", end='')
            print(each_item)
