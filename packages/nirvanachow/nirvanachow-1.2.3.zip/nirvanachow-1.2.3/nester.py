'''这是“nster.py”模块，提供了一个名为print_lol()的函数，这个函数的作用是
   打印列表，其中有可能包含（也可能不包含）嵌套列表。'''
import sys
def print_lol(the_list, indent=False, level=0, fh=sys.stdout):
    '''
        the_list，这可以是任何python列表（可以嵌套列表），各数据项各占一行。
        indent,是否缩进
        level，缩进多少
        file，指定数据写入位置
    '''
    
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level+1, fh)
        else:
            if indent:
                print('\t'*level, end='', file=fh)
            print(each_item, file=fh)
