import sys
def print_lol(the_list,level=-1,out=sys.stdout):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,level+1,out)
        else:
            for n in range(level):
                print("\t",end='',file=out)
            print(each_item,file=out)

