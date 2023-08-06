"""movies = ["the holy grail",1975,"terry jones & terry gilliam",91,["grahas chapman",["michael palin","john cleese","terry gilliam","eric idle","terry jones"]]]
print(movies)"""

"""这是nester_lxw.py模块，提供了一个名为print_lol_lxw的函数，这个函数的作用是打印列表
其中有可能包嵌套列表"""
def print_lol_lxw(the_list):
    """这个函数取一个位置参数，可以是任何列表
    所制定的列表中的每个数据项会输出到屏幕上
    各数据项各占一行。"""
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol_lxw(each_item)
        else:
            print(each_item)

