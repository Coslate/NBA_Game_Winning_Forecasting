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

def GetAllInternalLinks(starting_url):
    print('---------------GetAllInternalLinks begins-------------------')
    internal_url_pattern_str = ""
    internal_url_pattern = re.compile(r'.*www.(\S*)\.com.*')
    internal_url_pattern_match = internal_url_pattern.match(starting_url)
    if(internal_url_pattern_match is not None):
        internal_url_pattern_str = internal_url_pattern_match.group(1)
    else:
        internal_url_pattern = re.compile(r'(\S*)\..*')
        internal_url_pattern_match = internal_url_pattern.match(urlparse(starting_url).netloc)
        internal_url_pattern_str = internal_url_pattern_match.group(1)

    print(f'internal_url_pattern_str = {internal_url_pattern_str}')

    try:
        html = urlopen(starting_url)
    except HTTPError:
        print(f'Cannot access {starting_url}')
        print(f'Program terminated')
        sys.exit(1)

    bs_obj = BeautifulSoup(html, 'lxml')

    domain = urlparse(starting_url).scheme+"://"+urlparse(starting_url).netloc
    print(f'domain = {domain}')
    all_internal_links = crawler_nba.GetInternalLinks(bs_obj, internal_url_pattern_str, domain)

    for ele in all_internal_links:
        print(f'internal link = {ele}')
    print('---------------GetAllInternalLinks ends-------------------')

    return all_internal_links

def GetRandomExternalLinks(starting_url):
    print('---------------GetRandomExternalLinks begins----------------')
    external_url_pattern_str = ""
    external_url_pattern = re.compile(r'.*www.(\S*)\.com.*')
    external_url_pattern_match = external_url_pattern.match(starting_url)
    if(external_url_pattern_match is not None):
        external_url_pattern_str = external_url_pattern_match.group(1)
    else:
        external_url_pattern = re.compile(r'(\S*)\..*')
        external_url_pattern_match = external_url_pattern.match(urlparse(starting_url).netloc)
        external_url_pattern_str = external_url_pattern_match.group(1)

    print(f'external_url_pattern_str = {external_url_pattern_str}')

    try:
        html = urlopen(starting_url)
    except HTTPError:
        print(f'Cannot access {starting_url}')
        print(f'Program terminated')
        sys.exit(1)

    bs_obj = BeautifulSoup(html, 'lxml')

    all_external_links = crawler_nba.GetExternalLinks(bs_obj, external_url_pattern_str)

    for ele in all_external_links:
        print(f'external link = {ele}')

    print('---------------GetRandomExternalLinks ends----------------')
    if(len(all_external_links) == 0):
        # If there is no external link, get one from one of the internal link
        print('No external links, looking around the internal link for one.')
        all_internal_links = GetAllInternalLinks(starting_url)
        if(len(all_internal_links) == 0):
            print('No internal links found. Progran terminated.')
            sys.exit(1)
        else:
            random_internal_link = all_internal_links[random.randint(0, len(all_internal_links)-1)]
            print(f'Random internal link is {random_internal_link}')
            return GetRandomExternalLinks(random_internal_link)
    else:
        return all_external_links[random.randint(0, len(all_external_links)-1)]

def FollowExternalOnly(starting_url):
    external_link = GetRandomExternalLinks(starting_url)
    print(f'Random external link is {external_link}')
    FollowExternalOnly(external_link)

def main():
    current_time = datetime.datetime.now()
    print(f'current_time = {current_time}')
    random.seed(datetime.datetime.now())

    starting_url = "https://www.oreilly.com"
    print(f'starting_url = {starting_url}')

    #GetAllInternalLinks(starting_url)
    FollowExternalOnly(starting_url)



#-----------------Execution------------------#
if __name__ == '__main__':
    main()
