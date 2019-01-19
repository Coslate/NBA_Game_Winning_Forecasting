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
    #Argument Parser
    (thresh_change_proxy, thresh_change_proxy_list, is_debug) = ArgumentParser()
    print(f'thresh_change_proxy      = {thresh_change_proxy}')
    print(f'thresh_change_proxy_list = {thresh_change_proxy_list}')

    #Initialization
    crawler_nba.init(is_debug)

    #Sideband Setting
    current_time = datetime.datetime.now()
    print(f'current_time = {current_time}')
    random.seed(current_time)

    starting_url = "https://stats.nba.com/teams/boxscores"
    print(f'starting_url = {starting_url}')


#########################
#     Sub-Routine       #
#########################
def ArgumentParser():
    is_debug = 0
    thresh_change_proxy = 10
    thresh_change_proxy_list = 50

    parser = argparse.ArgumentParser()
    parser.add_argument("--thresh_change_proxy", "-tcp", help="The threshold value of the request number within an IP address to change the proxy.")
    parser.add_argument("--thresh_change_proxy_list", "-tcpl", help="The threshold value of the request number within an IP address to change the proxy list.")
    parser.add_argument("--is_debug", "-isd", help="1: To show the debug messages. 0: Not to show the debug messages.")


    args = parser.parse_args()

    if args.thresh_change_proxy:
        thresh_change_proxy = int(args.thresh_change_proxy)
    if args.thresh_change_proxy_list:
        thresh_change_proxy_list = int(args.thresh_change_proxy_list)
    if args.is_debug:
        is_debug = int(args.is_debug)

    return(thresh_change_proxy, thresh_change_proxy_list, is_debug)

#-----------------Execution------------------#
if __name__ == '__main__':
    main()
