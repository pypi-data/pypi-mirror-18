"""This is the "nester.py" module and it provides one function called print_lol()
   which prints lists that may or may not include nested lists."""

import sys

def print_lol(the_list, indent=False, level=0, write=sys.stdout):
	"""
	Prints a list of (possibly) nested lists with indentation.
	                                                       """
	for each_item in the_list:
		if isinstance(each_item, list):
			print_lol(each_item, indent, level+1, write)
		else:
			if indent:
				for x in range(level):
					print("\t", end='', file=write)
			print (each_item, file=write)
