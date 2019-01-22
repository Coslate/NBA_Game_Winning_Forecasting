#! /usr/bin/env python3.6


my_list = [1, 2, 3, 4]

def DelElement(val, my_list):
    my_list.remove(val)


for x in my_list:
    print(f'x = {x}')

print('-----------')
DelElement(3, my_list)

for x in my_list:
    print(f'x = {x}')

