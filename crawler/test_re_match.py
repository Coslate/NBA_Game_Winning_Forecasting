#! /usr/bin/env python3.6

import re
str_test = '/mail_to:orielly.com'

if((re.match(r'^(/|#)', str_test) is not None)) :
    if(re.match(r'.*:.*', str_test) is not None):
        print('match :')
    else:
        print('not match :')

    print('match')
else:
    print('not match')
