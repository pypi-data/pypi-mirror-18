"""this is the standard way to include a mutilple-line comment in your code."""
def print_lol(the_list):
    """this is a locale param ,called "the_list" ,this can be any python list."""
    for item_list in the_list:
        if isinstance(item_list,list):
            print_lol(item_list)
        else:
            print(item_list);
