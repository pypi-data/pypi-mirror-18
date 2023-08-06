"""This is the "nester.py" module and it provides one function called print_lol()
    which prints lists that may or not include nested lists."""
def print_lol(the_list, indent=False, level=0):
        """ Bug Fix1 """
        """This function takes positional argument called "the_list", which
              is any Python list (or - possibly - nested list). Each data item in the
              provided list is (recursively) printed to the screen on it's own line.
              A second argument called "indent"(True or False) is used to when indent or not,
              A third argument called "level" is used to tab-step when a nested list is encountered."""
        for each_item in the_list:
                if isinstance(each_item,list):
                        print_lol(each_item,indent,level + 1)
                else:
                        if indent:
                                for tab_step in range(level):
                                        print("\t", end=' ')
                        print(each_item)
