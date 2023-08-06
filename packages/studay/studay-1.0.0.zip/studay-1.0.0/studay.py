''' 这里是python模块的描述注解'''
def print_lol(the_list):
	''' 这里是python函数的注解'''
	for item in the_list:
		if isinstance(item,list):
			print_lol(item);
		else :
			print(item);