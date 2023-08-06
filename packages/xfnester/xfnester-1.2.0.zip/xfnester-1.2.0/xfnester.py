def print_lol(the_list,the_tab=0):
       for each_item in the_list:
                if isinstance(each_item,list):
                         print_lol(each_item,the_tab+1)
                else:
                         for num in range(the_tab):
                             print("\t",end='')
                         print(each_item)
