#! /usr/bin/env python3.6

from pathlib import Path

my_file = Path('./bb.log')
if my_file.exists():
    print('exist!')
else:
    print('no')
