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

#########################
#     Main-Routine      #
#########################
def main():
    #Initialization
    crawler_nba.init()

    #Argument Parser
    thresh_change_proxy = ArgumentParser()
    print(f'thresh_change_proxy = {thresh_change_proxy}')

    #Sideband Setting
    current_time = datetime.datetime.now()
    print(f'current_time = {current_time}')
    random.seed(datetime.datetime.now())

    starting_url = "https://www.oreilly.com"
    print(f'starting_url = {starting_url}')

    all_internal_links = []
    all_external_links = []
    external_link_str_list = []
    (all_external_links, all_internal_links, recursive_err) = crawler_nba.GetAllExternalLinksThrInternalLinks(starting_url, all_external_links, all_internal_links, external_link_str_list, thresh_change_proxy)

    print('---------------------All External Links : ---------------------')
    for external_link in all_external_links:
        print(f'{external_link}')

    print('---------------------All Internal Links : ---------------------')
    for internal_link in all_internal_links:
        print(f'{internal_link}')

    print('---------------------All exclude link str : ---------------------')
    for exclude_str in external_link_str_list:
        print(f'{exclude_str}')

#########################
#     Sub-Routine       #
#########################
def ArgumentParser():
    thresh_change_proxy = 10

    parser = argparse.ArgumentParser()
    parser.add_argument("--thresh_change_proxy", "-tcp", help="The threshold value of the request number within an IP address. If the request number is larger, then the program will change the proxy.")


    args = parser.parse_args()

    if args.thresh_change_proxy:
        thresh_change_proxy = int(args.thresh_change_proxy)

    return(thresh_change_proxy)

#-----------------Execution------------------#
if __name__ == '__main__':
    main()
