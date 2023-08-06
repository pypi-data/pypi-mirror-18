""" 这是一个用来展开打印列表的模块 """


# 用来展开所有的列表并且每行打印一个其中的内容，另一个参数the_list用来遇到嵌套列表的时候会打印一个制表符
def read_list(the_list, indent=False, the_level=0):
    for each_item in the_list:
        if isinstance(each_item, list):
            read_list(each_item, indent, the_level + 1)
        else:
            if indent:
                for tab_stop in range(the_level):
                    print("\t", end='')
            print(each_item)
