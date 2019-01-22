#! /usr/bin/env python3.6

list_test = [1, 3, 4]

def TestListAdd(input_list):
#    for x in range(len(input_list)):
#        input_list[x] += 1
#    input_list = [x+1 for x in input_list]
    input_list.append(100)

TestListAdd(list_test)

print('-'.join(str(x) for x in list_test))
