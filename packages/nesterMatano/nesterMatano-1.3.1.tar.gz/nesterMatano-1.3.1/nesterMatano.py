"""This is the 'nester.py' module, and it provides one function called
printLol() which prints lists that may or may not include nested lists."""


def printLol(theList, indent = False, level=0):


    """This function takes a positional argument calles 'theList' which is
any Python list (of, possibly, nested list). Each data item in the provided
list (recursively) printed to the screen on its own line.
A second argument called 'indent' is used to turn on or off indent
A third argument called 'level' is used to insert tap-stops when a nested list
is encountered """
    for item in theList:
        if isinstance(item, list):
            printLol(item, indent , level+1)
        else:
            if indent:
                for tabStop in range(level):
                    print("\t",end="")

            print(item)
