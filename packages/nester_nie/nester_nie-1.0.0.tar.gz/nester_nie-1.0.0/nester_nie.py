#!/usr/local/bin/python3

def print_lol(the_list):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item)
        else:
            print(each_item)

if __name__ == "__main__":
    mylist = ['Hello',["apple","banner",["1","2","3"]]]
    print_lol(mylist)
