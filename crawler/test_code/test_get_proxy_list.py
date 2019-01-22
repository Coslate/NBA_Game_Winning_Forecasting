#! /usr/bin/env python3.6

from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.error import HTTPError
import re
import package_crawler_nba.crawler_nba as crawler_nba
import random
import datetime
import sys
import argparse

proxy_list = []
proxy_list = crawler_nba.GetProxyList()


for proxy in proxy_list:
    print(f'proxy = {proxy}')

print(f'proxy num = {len(proxy_list)}')
