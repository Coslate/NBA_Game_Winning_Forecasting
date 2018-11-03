#! /usr/bin/env python3.6
import re

test_str = 'glxkaaa adago-1'

if(re.match(r'^(((?!(empty)).)*$)', test_str) is not None):
    print('match!')
else:
    print('not match')



if(re.match(r'.*aaa.*', test_str) is not None):
    print('----match---')
else:
    print('----no----')

