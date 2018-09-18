#! /usr/bin/env python3.6

from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
import package_crawler_nba.crawler_nba as crawler_nba
import random
import datetime
import sys
from urllib.error import HTTPError

def main():
    current_time = datetime.datetime.now()
    print(f'current_time = {current_time}')
    random.seed(datetime.datetime.now())

    starting_url = "https://www.oreilly.com"
    print(f'starting_url = {starting_url}')

    all_internal_links = []
    all_external_links = []
    external_link_str_list = []
    (all_external_links, all_internal_links, recursive_err) = crawler_nba.GetAllExternalLinksThrInternalLinks(starting_url, all_external_links, all_internal_links, external_link_str_list)

    print('---------------------All External Links : ---------------------')
    for external_link in all_external_links:
        print(f'{external_link}')

    print('---------------------All Internal Links : ---------------------')
    for internal_link in all_internal_links:
        print(f'{internal_link}')

    print('---------------------All exclude link str : ---------------------')
    for exclude_str in external_link_str_list:
        print(f'{exclude_str}')

#-----------------Execution------------------#
if __name__ == '__main__':
    main()
