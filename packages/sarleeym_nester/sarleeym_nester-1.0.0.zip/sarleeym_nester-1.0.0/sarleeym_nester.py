""" this is the nester module"""

def print_lol(the_list):
    """this function takes an argument called the_list"""

    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print(each_item)
