#! /usr/bin/env python3.6
import re

a = '123.22'

if(re.match(r'\d+\.\d+', a)):
    print('yes')
else:
    print('no')
