''' 这里是python模块的描述注解'''
def print_lol(the_list,indent=False,level=0):
	''' 这里是函数的注释'''
	for each_item in the_list:
		if isinstance(each_item,list):
			print_lol(each_item,indent,level+1);
		else :
			if indent :
				for each_i in range(level):
					print("\t",end='');
			print(each_item);