#! /usr/bin/env python3

import re

a = "yes" if(re.match(r'.*world.*', 'hello world!')) else "no"
print('a = {}'.format(a))
