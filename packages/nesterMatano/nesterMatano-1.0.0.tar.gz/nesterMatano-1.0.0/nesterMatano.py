"""This is the 'nester.py' module, and it provides one function called
printLol() which prints lists that may or may not include nested lists."""


def printLol(theList):


    """This function takes a positional argument calles 'theList' which is
any Python list (of, possibly, nested list). Each data item in the provided
list (recursively) printed to the screen on its own line."""
    for item in theList:
        if isinstance(item, list):
            printLol(item)
        else:
            print(item)
