""" 这是一个headfirst例子，学习如何建立一个迭代函数"""
def print_lol(the_list,the_tab=false,level=0):
        for each_item in the_list:      #这是循环主体
                if isinstance(each_item,list):
                        print_lol(each_item,the_tab,level+1)
                else:
                        if the_tab:
                                for tab_stop in range(level):
                                        print("\t",end='')
                                print(each_item)
                        
