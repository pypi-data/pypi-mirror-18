def printlol(the_list,level):
    for each_item in the_list:
        if isinstance(each_item,list):
            printlol(each_item,level+1)
        else:
             for tap_stop in range(level):
                print("\t",end='')
             print(each_item)
            
                
