'''这是“nster.py”模块，提供了一个名为print_lol()的函数，这个函数的作用是
   打印列表，其中有可能包含（也可能不包含）嵌套列表。'''
def print_lol(the_list, indent=False, level=0):
    '''这个函数有一个位置参数，名为the_list，这可以是任何python列表（可以嵌套列表）。
       所指定的列表中的每个数据项都会（递归地）输出到屏幕上，各数据项各占一行。'''
    
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level+1)
        else:
            if indent:
                print('\t'*level, end='')
            print(each_item)
