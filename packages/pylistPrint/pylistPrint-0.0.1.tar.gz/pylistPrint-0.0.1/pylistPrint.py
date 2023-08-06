
"""This module is to print the list from head first python. This is a test."""

def pylistPrint(items):
    for item in items:
        if isinstance(item, list):
            pylistPrint(item)
        else:
            print(item)