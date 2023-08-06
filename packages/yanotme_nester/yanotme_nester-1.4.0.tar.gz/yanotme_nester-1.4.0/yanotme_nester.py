"""this is the standard way to include a mutilple-line comment in your code. add indent param"""
def print_lol(the_list,indent,level=0):
    """this is a locale param ,called "the_list" ,this can be any python list."""
    for item_list in the_list:
        if isinstance(item_list,list):
            print_lol(item_list,indent,level+1)
        else:
            if indent == True:
                for num in range(level):
                    print("\t",end='')
            print(item_list);
