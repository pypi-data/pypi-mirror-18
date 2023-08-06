"""这是一个统计列表嵌套数量的函数"""
def listnum(count,listname):
	for listnode in listname:
		if isinstance(listnode,list):
			count=count+listnum(count,listnode)
	return count
