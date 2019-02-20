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
    (thresh_change_proxy, thresh_change_proxy_list, is_debug, out_file_name, indexing_to_csv, team, password, season, mysql_password, table, unix_socket, database_name) = ArgumentParser()
    if(is_debug):
        print(f'thresh_change_proxy      = {thresh_change_proxy}')
        print(f'thresh_change_proxy_list = {thresh_change_proxy_list}')
        print(f'out_file_name            = {out_file_name}')
        print(f'indexing_to_csv          = {indexing_to_csv}')
        print(f'team                     = {team}')
        print(f'season                   = {season}')

    #Initialization
    crawler_nba.init(is_debug)

    #Sideband Setting
    current_time = datetime.datetime.now()
    print(f'current_time in Taiwan = {current_time}')
    random.seed(current_time)

    #Scraping NBA stats
    starting_url = "https://stats.nba.com/teams/boxscores"
    (all_data_loop, columns, browser, all_data_item_href) = crawler_nba.GetNBADataRequest(starting_url, thresh_change_proxy, thresh_change_proxy_list, season)

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
    yesterday_time_usa = datetime.datetime.now(time_zone_usa) - datetime.timedelta(days=1)
    current_date_usa   = str(current_time_usa.month).zfill(2)+'/'+str(current_time_usa.day).zfill(2)+'/'+str(current_time_usa.year)
    yesterday_date_usa = str(yesterday_time_usa.month).zfill(2)+'/'+str(yesterday_time_usa.day).zfill(2)+'/'+str(yesterday_time_usa.year)
    print(f'current time in USA(America/New York)       = {current_time_usa}')
    print(f'current date in USA(America/New York)       = {current_date_usa}')
    print(f'Use yesterday date in USA(America/New York) = {yesterday_date_usa}')

    #Check if the data has the interested game.
    (game_set_num, get_wanted_data, selected_data_df, short_selected_data_df, starters_data_dict) = crawler_nba.CheckDateHasSpecifiedTeam(yesterday_date_usa, team, all_data_df, browser, all_data_item_href)

    #Send mails if interested game occurs.
    crawler_nba.CheckSendMails(yesterday_date_usa, game_set_num, selected_data_df, short_selected_data_df, get_wanted_data, password, team, starters_data_dict)

    #Send to I-No if Lakers lose a game.
    crawler_nba.CheckSendMailsToINO(yesterday_date_usa, 'LAL', all_data_df, password, browser, all_data_item_href)

    #Close
    browser.close()

    #Store all the scraped data into MySQL
    crawler_nba.MySQLDBInitializeDataFrame(mysql_password, table, unix_socket, database_name, all_data_df)

    # Close the connection of MySQL Database
    crawler_nba.MySQLDBClose(crawler_nba.cur, crawler_nba.conn)

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
    season                   = '2018-19'
    mysql_password           = ""
    table                    = ""
    database_name            = ""
    unix_socket              = ""

    parser = argparse.ArgumentParser()
    parser.add_argument("--thresh_change_proxy", "-tcp", help="The threshold value of the request number within an IP address to change the proxy.")
    parser.add_argument("--thresh_change_proxy_list", "-tcpl", help="The threshold value of the request number within an IP address to change the proxy list.")
    parser.add_argument("--is_debug", "-isd", help="1: To show the debug messages. 0: Not to show the debug messages. Default is 0.")
    parser.add_argument("--out", "-out", help="The output file name of the scraped NBA data.")
    parser.add_argument("--out_indexing", "-out_idx", help="1: To write out the csv file of scraped NBA data with indexing. 0: To write out the csv file of scraped NBA data without indexing. Default is 1.")
    parser.add_argument("--team", "-team", help="The team specified in this argument will be searched in the statistics of the games played today on stats.nba.com. If the specified team occurs, the statistics will be sent to your mailbox.")
    parser.add_argument("--gmail_password", "-gmail_p", help="The password of your gmail.", required=True)
    parser.add_argument("--season", "-season", help="The NBA season that you want to scrape. For example, '-season 2018-19' will make the script scrape the NBA game data in the 2018-2019 season. The default is 2018-19")
    parser.add_argument("--mysql_password", "-sql_p", help="The password to connect to MySQL server.", required=True)
    parser.add_argument("--mysql_table_name", "-sql_tn", help="The table name that will be used to store data.", required=True)
    parser.add_argument("--unix_socket", "-sql_un_sock", help="The unix_socket that is used to mypysql connection.", required=True)
    parser.add_argument("--database_name", "-database_name", help="The unix_socket that is used to mypysql connection.", required=True)

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
    if args.season:
        season = args.season
    if args.mysql_password:
        mysql_password = args.mysql_password
    if args.mysql_table_name:
        table = args.mysql_table_name
    if args.unix_socket:
        unix_socket = args.unix_socket
    if args.database_name:
        database_name = args.database_name

    return(thresh_change_proxy, thresh_change_proxy_list, is_debug, out_file_name, indexing_to_csv, team, password, season, mysql_password, table, unix_socket, database_name)

#-----------------Execution------------------#
if __name__ == '__main__':
    main()
