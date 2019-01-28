#! /usr/bin/env python3.6

from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.error import HTTPError
from selenium import webdriver
import re
import pandas as pd
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
    (thresh_change_proxy, thresh_change_proxy_list, is_debug, out_file_name, indexing_to_csv) = ArgumentParser()
    print(f'thresh_change_proxy      = {thresh_change_proxy}')
    print(f'thresh_change_proxy_list = {thresh_change_proxy_list}')

    #Initialization
    crawler_nba.init(is_debug)

    #Sideband Setting
    current_time = datetime.datetime.now()
    print(f'current_time = {current_time}')
    random.seed(current_time)

    #Scraping NBA stats
    starting_url = "https://stats.nba.com/teams/boxscores"
    (all_data_loop, columns) = crawler_nba.GetNBADataRequest(starting_url, thresh_change_proxy, thresh_change_proxy_list)

    #Constructing the dataframe and write out as a csv file
    all_data_df = pd.DataFrame(data = all_data_loop, columns = columns)
    all_data_df.dropna(axis=1, how='all', inplace=True) #Delete the empty columns
    print(f'org columns = {columns}')
    print(f'new columns = {list(all_data_df.columns.values)}')
    print(f'all_data_loop_df = ')
    print(all_data_df.to_string(index=indexing_to_csv))
    if(out_file_name != ""):
        all_data_df.to_csv(out_file_name, sep=',', index=indexing_to_csv)


#########################
#     Sub-Routine       #
#########################
def ArgumentParser():
    is_debug = 0
    thresh_change_proxy = 10
    thresh_change_proxy_list = 50
    out_file_name = ""
    indexing_to_csv = True

    parser = argparse.ArgumentParser()
    parser.add_argument("--thresh_change_proxy", "-tcp", help="The threshold value of the request number within an IP address to change the proxy.")
    parser.add_argument("--thresh_change_proxy_list", "-tcpl", help="The threshold value of the request number within an IP address to change the proxy list.")
    parser.add_argument("--is_debug", "-isd", help="1: To show the debug messages. 0: Not to show the debug messages. Default is 0.")
    parser.add_argument("--out", "-out", help="The output file name of the scraped NBA data.")
    parser.add_argument("--out_indexing", "-out_idx", help="1: To write out the csv file of scraped NBA data with indexing. 0: To write out the csv file of scraped NBA data without indexing. Default is 1.")


    args = parser.parse_args()

    if args.thresh_change_proxy:
        thresh_change_proxy = int(args.thresh_change_proxy)
    if args.thresh_change_proxy_list:
        thresh_change_proxy_list = int(args.thresh_change_proxy_list)
    if args.is_debug:
        is_debug = int(args.is_debug)
    if args.out:
        out_file_name = args.out
    if args.out_indexing:
        indexing_to_csv = True if(int(args.out_indexing) == 1) else False

    return(thresh_change_proxy, thresh_change_proxy_list, is_debug, out_file_name, indexing_to_csv)

#-----------------Execution------------------#
if __name__ == '__main__':
    main()
