""" This is my first python module to iterate a list of items.
Going good so far.
"""

def list_recursion(inputList, level):
# This iterates the inputList collection.
	for listItem in inputList:
		if isinstance(listItem, list):
			list_recursion(listItem, level+1)
		else :
			for tab_stop in range(level):
				print("\t", end='')
			print(listItem)
