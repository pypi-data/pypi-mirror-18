
""" 把输入的 list(嵌套或者不嵌套 list) 递归打印到控制台 """ 
def print_lol(the_list):
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print(each_item)

""" 生成输出数组"""
movies = ['a', 'b', 'c', 'd', [1, ['aaa', 'bbb']]]
print_lol(movies)
