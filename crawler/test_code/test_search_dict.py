#! /usr/bin/env python3.6

a_dict_list = [{'main_color' : 'red', 'sec_color' : 'blue'},
               {'main_color' : 'yellow', 'sec_color' : 'green'},
               {'main_color' : 'yellow', 'sec_color' : 'blue'}]

sel_dict = a_dict_list[0]
for x in a_dict_list:
    print('main_color = {x}, sec_color = {y}'.format(x = x['main_color'], y = x['sec_color']))

if(any(((d['main_color'] == sel_dict['main_color']) and (d['sec_color'] == sel_dict['sec_color'])) for d in a_dict_list)):
   print('yes')
   a_dict_list.remove(sel_dict)
else:
   print('no')

for x in a_dict_list:
    print('main_color = {x}, sec_color = {y}'.format(x = x['main_color'], y = x['sec_color']))
