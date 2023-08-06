"""这是nester.py模块，提供了一个名为print_lol的涵数，这个涵数的作用是打印列表，
其中有可能包含嵌套列表。"""
def print_lol(the_list,level=0):
	"""这个函数有一个位置参数，名为“the_list”,这可以是任何Python列表，
	也可以是包含嵌套列表的列表。所指定的列表中的每个数据项会递归地输出
	到屏幕上，各数据项各占一行。
	第二个参数，名为“level”，用于遇到嵌套列表时插入制表符"""
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item,level+1)
		else:
			for i in range(level):
				print('\t',end='')
			print(each_item)