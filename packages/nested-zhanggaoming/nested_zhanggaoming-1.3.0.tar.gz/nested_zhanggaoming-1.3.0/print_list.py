""" 一个简单的打印list数据到console的模块 """
import sys

def print_lol(the_list, indent=False, level=0, out=sys.stdout):
    """第一个参数是list, 第二个参数是 缩进, 第三个参数是 准备输出的地方"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level+1, out)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t", end='', file=out)
            print(each_item, file=out)
