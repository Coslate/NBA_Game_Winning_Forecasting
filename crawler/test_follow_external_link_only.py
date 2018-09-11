#! /usr/bin/env python3.6

from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
import package_crawler_nba.crawler_nba as crawler_nba
import random
import datetime

def main():
    starting_url = "https://www.oreilly.com"
    html = urlopen(starting_url)
    bs_obj = BeautifulSoup(html, 'lxml')

    domain = urlparse(starting_url).scheme+"://"+urlparse(starting_url).netloc
    print(f'domain = {domain}')
    all_internal_links = crawler_nba.GetInternalLinks(bs_obj, 'https://oreilly.com')

    for ele in all_internal_links:
        print(f'ele = {ele}')



#-----------------Execution------------------#
if __name__ == '__main__':
    main()
