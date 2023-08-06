#coding:utf-8

"""
迭代for循环
"""
def print_lol(print_list,indent=False,level=0):
	for str in print_list:
		if isinstance(str,list):
			print_lol(str,indent,level+1)
		else:
			if indent:
				for tab_stop in range(level):
					print "\t"
			print str
