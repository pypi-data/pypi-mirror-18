"""
This is the "nester.py" module and it's provide anoe function called print_lol()
which prints lists that may or may not include nested lists.
"""
def print_lol(the_list,level):
    """ This function has one positinal argument called "the_list" which is any python
        list. Each data item in the list is printed to the screen on
        it's own line."""
    for item in the_list:
        if isinstance(item,list):
            print_lol(item,level+1)
        else:
            for i in range(level):
                print("\t",end='')
            print(item)
