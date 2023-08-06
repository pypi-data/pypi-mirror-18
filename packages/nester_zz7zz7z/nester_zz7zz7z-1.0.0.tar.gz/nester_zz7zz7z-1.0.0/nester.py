"""This is the module for print the item"""
def print_lol(the_list):
    """that is the module"""
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item)
        else:
            print(each_item)
