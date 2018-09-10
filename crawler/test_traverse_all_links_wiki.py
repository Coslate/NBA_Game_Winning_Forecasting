#! /usr/bin/env python3.6

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import package_crawler_nba.crawler_nba as crawler_nba
import random
import datetime
import sys

print(f"time = {datetime.datetime.now()}")
sys.setrecursionlimit(1500)
print(f'python recursion limit = {sys.getrecursionlimit()}')

pages_links = set()
recursive_num = 0
(recursive_num, pages_links) = crawler_nba.GetAllURLLinks("", pages_links, recursive_num, 1)

print('--Final--')
print(f'recursive_num = {recursive_num}')
for pages in pages_links:
    print(f'pages = {pages}')
