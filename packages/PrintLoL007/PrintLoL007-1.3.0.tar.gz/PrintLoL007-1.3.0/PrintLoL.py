""" What's New ???  """
"""In this latest version of PrintLoL module I have included the facility to write the list into a file in a formmated way, make sure if you want to simply print it on the screen then import the "sys" module and you must provide all the argument values before coming to the data object pointing to the file !!! """

"""This is the "PrintLoL.py" module and it provides one function called print_lol() 
   which prints lists that may or may not include nested lists."""

def print_lol(the_list,indent =False ,level=0,fh=sys.stdout):
	"""This function takes one positional argument called "the_list", which 
	is any Python list (of - possibly - nested lists). Each data item in the
	provided list is (recursively) printed to the screen on it’s own line.
	You may also specify if you want any indentation by stating True or False, and you may also give the number of tab stops you want !!!
	Finally provide the data object of the file you wanna print this list to !
	Thank You for your patience !!!"""
	for each_item in the_list:
		if isinstance(each_item, list):
			print_lol(each_item,indent,level+1,fh)
		else:
			if indent :
				for tab_stop in range(level):
					print("\t",end='',file=fh)
			print(each_item,file=fh)



