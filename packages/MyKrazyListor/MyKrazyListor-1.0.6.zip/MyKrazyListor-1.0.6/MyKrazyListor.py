""" This is my first python module to iterate a list of items.
Going good so far.
"""


def list_recursion(inputList, indent=False, level=0):
    for listItem in inputList:
        if isinstance(listItem, list):
            list_recursion(listItem, indent, level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t", end='')
            print(listItem)
