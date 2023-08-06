'''这个函数用于打印嵌套列表。，。。
。。。。
。。。。。。。'''
def my_print (the_list,is_sp = False,p_level = 0) :
    '''这就是用于实现的函数方法？
呵呵我累撒谎积分卡机，level用来表示制表符数量
萨回到家萨芬'''
    for each_i in the_list :
        if isinstance(each_i,list) :
            my_print(each_i,p_level+1)
        else :
            if is_sp :
                for tab_print in range(p_level):
                    print("\t",end = "")
            print(each_i)
