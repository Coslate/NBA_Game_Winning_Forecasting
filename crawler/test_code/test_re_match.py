#! /usr/bin/env python3.6

import re
str_test = '/mail_to:orielly.com'

'''
if((re.match(r'^(/|#)', str_test) is not None)) :
    if(re.match(r'.*:.*', str_test) is not None):
        print('match :')
    else:
        print('not match :')

    print('match')
else:
    print('not match')
'''
'''
a_var = 'SAS'
a_str = 'NOddadwadaefef    vs. SAS'
if(re.match(r'.*{}.*'.format(a_var), a_str)):
    print('yes')
else:
    print('no')

print(re.findall('\b', 't\bst'))
print(re.findall('\\b', 't\bst'))
print(re.findall(r'\b', 't\bst'))
'''



a = '22\/22\/32'
if(re.match(r'.*/.*', a)):
    print('yes')
else:
    print('no')
