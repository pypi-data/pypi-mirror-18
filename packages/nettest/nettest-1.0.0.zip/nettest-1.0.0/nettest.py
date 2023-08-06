'''这个函数用于打印嵌套列表。，。。
。。。。
。。。。。。。'''
def my_print (the_list) :
    '''这就是用于实现的函数方法？
呵呵我累撒谎积分卡机
萨回到家萨芬'''
    for each_i in the_list :
        if isinstance(each_i,list) :
            my_print(each_i)
        else :
            print(each_i)
