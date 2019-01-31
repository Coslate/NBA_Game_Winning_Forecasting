#! /usr/bin/env python3.6

from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.error import HTTPError
from selenium import webdriver
from tabulate import tabulate
import re
import pandas as pd
import package_crawler_nba.crawler_nba as crawler_nba
import package_email.email as email
import random
import datetime
import sys
import argparse
import pytz

#########################
#     Main-Routine      #
#########################
def main():
    #Argument Parser
    (thresh_change_proxy, thresh_change_proxy_list, is_debug, out_file_name, indexing_to_csv, team, password) = ArgumentParser()
    print(f'thresh_change_proxy      = {thresh_change_proxy}')
    print(f'thresh_change_proxy_list = {thresh_change_proxy_list}')

    #Initialization
    crawler_nba.init(is_debug)

    #Sideband Setting
    current_time = datetime.datetime.now()
    print(f'current_time in Taiwan = {current_time}')
    random.seed(current_time)

    #Scraping NBA stats
    starting_url = "https://stats.nba.com/teams/boxscores"
    (all_data_loop, columns) = crawler_nba.GetNBADataRequest(starting_url, thresh_change_proxy, thresh_change_proxy_list)

    #Constructing the dataframe and write out as a csv file
    all_data_df     = pd.DataFrame(data = all_data_loop, columns = columns)
    all_data_df.dropna(axis=1, how='all', inplace=True) #Delete the empty columns
    all_data_df_tab = tabulate(all_data_df, headers='keys', tablefmt='psql')
    print(f'org columns = {columns}')
    print(f'new columns = {list(all_data_df.columns.values)}')
    print(f'all_data_df_tab = ')
    print(all_data_df_tab)
    if(out_file_name != ""):
        all_data_df.to_csv(out_file_name, sep=',', index=indexing_to_csv)

    #Get current date at the time zone of America/New York
    time_zone_usa      = pytz.timezone('America/New_York')
    current_time_usa   = datetime.datetime.now(time_zone_usa)
    yesterday_time_usa = datetime.datetime.now(time_zone_usa) - timedelta(days=1)
    current_date_usa   = str(current_time_usa.month).zfill(2)+'/'+str(current_time_usa.day).zfill(2)+'/'+str(current_time_usa.year)
    yesterday_date_usa = str(yesterday_time_usa.month).zfill(2)+'/'+str(yesterday_time_usa.day).zfill(2)+'/'+str(yesterday_time_usa.year)
    print(f'current time in USA(America/New York)       = {current_time_usa}')
    print(f'current date in USA(America/New York)       = {current_date_usa}')
    print(f'Use yesterday date in USA(America/New York) = {yesterday_date_usa}')

    #Send email if has interested team
    (get_wanted_data, selected_data_df, short_selected_df) = crawler_nba.CheckDateHasSpecifiedTeam(yesterday_date_usa, team, all_data_df)
    if(get_wanted_data):
        gmail_user     = 'coslate@media.ee.ntu.edu.tw'
        gmail_password = password # your gmail password
#        content = selected_data_df.to_string(index=indexing_to_csv)
        content  = tabulate(short_selected_df, headers='keys', tablefmt='psql')
        content += '\n'+'detailed : '+'\n'
        content += tabulate(selected_data_df, headers='keys', tablefmt='psql')
        title    = 'NBA game statistics for {x}'.format(x = team)
        to_addr  = gmail_user
        cc_addr  = gmail_user+', '+'vickiehsu828@gmail.com'
        email.SendMail(gmail_user, gmail_password, content, title, to_addr, cc_addr)
        print(f'There are NBA games for {team} at {yesterday_date_usa}. Email sent!')
    else:
        print(f'No NBA games for {team} at {yesterday_date_usa}.')

#########################
#     Sub-Routine       #
#########################
def ArgumentParser():
    is_debug                 = 0
    thresh_change_proxy      = 10
    thresh_change_proxy_list = 50
    out_file_name            = ""
    indexing_to_csv          = True
    team                     = 'GSW'
    password                 = ''

    parser = argparse.ArgumentParser()
    parser.add_argument("--thresh_change_proxy", "-tcp", help="The threshold value of the request number within an IP address to change the proxy.")
    parser.add_argument("--thresh_change_proxy_list", "-tcpl", help="The threshold value of the request number within an IP address to change the proxy list.")
    parser.add_argument("--is_debug", "-isd", help="1: To show the debug messages. 0: Not to show the debug messages. Default is 0.")
    parser.add_argument("--out", "-out", help="The output file name of the scraped NBA data.")
    parser.add_argument("--out_indexing", "-out_idx", help="1: To write out the csv file of scraped NBA data with indexing. 0: To write out the csv file of scraped NBA data without indexing. Default is 1.")
    parser.add_argument("--team", "-team", help="The team specified in this argument will be searched in the statistics of the games played today on stats.nba.com. If the specified team occurs, the statistics will be sent to your mailbox.")
    parser.add_argument("--gmail_password", "-gmail_p", help="The password of your gmail.", required=True)




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
    if args.team:
        team = args.team
    if args.gmail_password:
        password = args.gmail_password

    return(thresh_change_proxy, thresh_change_proxy_list, is_debug, out_file_name, indexing_to_csv, team, password)

#-----------------Execution------------------#
if __name__ == '__main__':
    main()
