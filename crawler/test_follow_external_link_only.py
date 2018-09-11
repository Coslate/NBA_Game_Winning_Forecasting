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
    internal_url_pattern_str = ""
    internal_url_pattern = re.compile(r'.*www.(\S*)\.com.*')
    internal_url_pattern_match = internal_url_pattern.match(starting_url)
    if(internal_url_pattern_match is not None):
        internal_url_pattern_str = internal_url_pattern_match.group(1)
    print(f'internal_url_pattern_str = {internal_url_pattern_str}')

    html = urlopen(starting_url)
    bs_obj = BeautifulSoup(html, 'lxml')

    domain = urlparse(starting_url).scheme+"://"+urlparse(starting_url).netloc
    print(f'domain = {domain}')
    all_internal_links = crawler_nba.GetInternalLinks(bs_obj, internal_url_pattern_str, domain)

    for ele in all_internal_links:
        print(f'ele = {ele}')



#-----------------Execution------------------#
if __name__ == '__main__':
    main()
