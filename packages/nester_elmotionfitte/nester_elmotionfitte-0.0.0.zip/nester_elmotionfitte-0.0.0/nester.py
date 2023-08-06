'''
this module is a function which can print the nested list
'''
def print_lol(the_list, indent=False, level=0):
	'''this function receive list as an input and print it
	   it also receive another argument to handle indentation
	   now this function is able to select wheter or not indentation is needed'''
	for each_item in the_list:
		if isinstance(each_item, list):
			print_lol(each_item, indent, level+1)
		else:
			if indent:
				for x in range(level):
					print("\t", end='')
			print (each_item)
				
