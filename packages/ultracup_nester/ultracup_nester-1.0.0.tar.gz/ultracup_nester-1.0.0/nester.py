""" This is the nested.py module that allows to print any level
of nested lists, if you have a list within a list within a list
this is your module
"""
def print_lol (the_list):
    """ This functino accepts an item, if the item is a list
    it iterates over the item an prints it's elements, if isn't
    prints its content right away!
    """
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print(each_item)
