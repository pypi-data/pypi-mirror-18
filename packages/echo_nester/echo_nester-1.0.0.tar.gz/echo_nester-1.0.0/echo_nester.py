""" echo_nester.py 模块提供了一个函数 echo_print_list() ，这个函数可以用于打印包含嵌套列表的列表 """
def echo_print_list(thelist):
    for each_item in thelist: 
        if isinstance(each_item,list):
            echo_print_list(each_item)
        else:
            print(each_item)
   
