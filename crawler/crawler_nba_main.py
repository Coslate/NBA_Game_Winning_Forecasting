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
    print(f'> Parse the argument...')
    (thresh_change_proxy, thresh_change_proxy_list, is_debug, out_file_name, indexing_to_csv, team, password, season, mysql_password, table, unix_socket, database_name, scrape_all_season, write_csv_use_sql) = ArgumentParser()
    if(is_debug):
        print(f'thresh_change_proxy      = {thresh_change_proxy}')
        print(f'thresh_change_proxy_list = {thresh_change_proxy_list}')
        print(f'out_file_name            = {out_file_name}')
        print(f'indexing_to_csv          = {indexing_to_csv}')
        print(f'team                     = {team}')
        print(f'season                   = {season}')
        print(f'scrape_all_season        = {scrape_all_season}')
        print(f'write_csv_use_sql        = {write_csv_use_sql}')

#Initialization
    print(f'> Proxy initialization...')
    crawler_nba.init(is_debug)

#Sideband Setting
    print(f'> Sideband setting...')
    current_time = datetime.datetime.now()
    print(f'current_time in Taiwan = {current_time}')
    random.seed(current_time)

    #Get current date at the time zone of America/New York
    time_zone_usa      = pytz.timezone('America/New_York')
    current_time_usa   = datetime.datetime.now(time_zone_usa)
    yesterday_time_usa = datetime.datetime.now(time_zone_usa) - datetime.timedelta(days=1)
    current_date_usa   = str(current_time_usa.month).zfill(2)+'/'+str(current_time_usa.day).zfill(2)+'/'+str(current_time_usa.year)
    yesterday_date_usa = str(yesterday_time_usa.month).zfill(2)+'/'+str(yesterday_time_usa.day).zfill(2)+'/'+str(yesterday_time_usa.year)
    print(f'current time in USA(America/New York)       = {current_time_usa}')
    print(f'current date in USA(America/New York)       = {current_date_usa}')
    print(f'Use yesterday date in USA(America/New York) = {yesterday_date_usa}')

#Scraping NBA stats
    print(f'> Crawling/Scraping...')
    starting_url = "https://stats.nba.com/teams/boxscores"
    (all_data_loop, columns, browser, all_data_item_href) = crawler_nba.GetNBADataRequest(starting_url, thresh_change_proxy, thresh_change_proxy_list, season, scrape_all_season)

#Constructing the dataframe and write out as a csv file
    print(f'> Constructing the dataframe...')
    all_data_df = crawler_nba.ConstructDFFROMListOFList(all_data_loop, columns)

#Check if the data has the interested game.
    print(f'> Check whether specific teams have games...')
    (game_set_num, get_wanted_data, selected_data_df, short_selected_data_df, starters_data_dict) = crawler_nba.CheckDataHasSpecifiedTeam(yesterday_date_usa, team, all_data_df, browser, all_data_item_href)

#Send mails if interested game occurs.
    print(f'> Send mails if specific team has games...')
    crawler_nba.CheckSendMails(yesterday_date_usa, game_set_num, selected_data_df, short_selected_data_df, get_wanted_data, password, team, starters_data_dict)

#Send to I-No if Lakers lose a game.
    print(f'> Send mails if LAL lost games...')
    crawler_nba.CheckSendMailsToINO(yesterday_date_usa, 'LAL', all_data_df, password, browser, all_data_item_href)

#Close
    print(f'> Close the browser...')
    browser.close()

#Store all the scraped data into MySQL
    print(f'> Database Initialization(MySQL)...')
    crawler_nba.MySQLDBInitializeNBATable(mysql_password, table, unix_socket, database_name)

#Store data list to MySQL one by one.
    print(f'> Store scraped data into database(MySQL)...')
    crawler_nba.MySQLDBStoreNBADataAll(table, all_data_df, yesterday_date_usa, scrape_all_season)

#Get scraped data from MySQL.
    print(f'> Get scraped data from database(MySQL)...')
    all_data_df_sql = crawler_nba.GetAllDataFromDatabase(table)

#Check whether to write out scraped data to a CSV file.
    print(f'> Check whether to write scraped data to a CSV file(MySQL)...')
    crawler_nba.CheckIfWriteToCSV(all_data_df, all_data_df_sql, out_file_name, indexing_to_csv, write_csv_use_sql)

#Close the connection of MySQL Database
    print(f'> Store done and close the database connection(MySQL)...')
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
    scrape_all_season        = 0
    write_csv_use_sql        = 0
    gmail_user               = ""
    gmail_to_list            = ""

    parser = argparse.ArgumentParser()
    parser.add_argument("--thresh_change_proxy", "-tcp", help="The threshold value of the request number within an IP address to change the proxy.")
    parser.add_argument("--thresh_change_proxy_list", "-tcpl", help="The threshold value of the request number within an IP address to change the proxy list.")
    parser.add_argument("--is_debug", "-isd", help="1: To show the debug messages. 0: Not to show the debug messages. Default is 0.")
    parser.add_argument("--out", "-out", help="The output file name of the scraped NBA data.")
    parser.add_argument("--out_indexing", "-out_idx", help="1: To write out the csv file of scraped NBA data with indexing. 0: To write out the csv file of scraped NBA data without indexing. Default is 1.")
    parser.add_argument("--team", "-team", help="The team specified in this argument will be searched in the statistics of the games played today on stats.nba.com. If the specified team occurs, the statistics will be sent to your mailbox.")
    parser.add_argument("--gmail_password", "-gmail_p", help="The password of your gmail.")
    parser.add_argument("--gmail_user", "-gmail_user", help="The 'From' user to send the notify mails.")
    parser.add_argument("--gmail_to_list", "-gmail_to_list", help="The 'To' users that receive the sending notified mails from -gmail_user. It can be specified as a file that includes one email address of a receiver each line or just specified as '-gmail_to_list [receiver_email_address_1, receiver_email_address_2, ..., receiver_email_address_n]")
    parser.add_argument("--season", "-season", help="The NBA season that you want to scrape. For example, '-season 2018-19' will make the script scrape the NBA game data in the 2018-2019 season. The default is 2018-19")
    parser.add_argument("--mysql_password", "-sql_p", help="The password to connect to MySQL server.", required=True)
    parser.add_argument("--mysql_table_name", "-sql_tn", help="The table name that will be used to store data.", required=True)
    parser.add_argument("--unix_socket", "-sql_un_sock", help="The unix_socket that is used to mypysql connection.", required=True)
    parser.add_argument("--database_name", "-database_name", help="The unix_socket that is used to mypysql connection.", required=True)
    parser.add_argument("--scrape_all_season", "-scrape_all_season", help="Set 1 to scrape all the pages of a season. Set 0 to only scrape the first page of a season.")
    parser.add_argument("--write_csv_use_sql", "-wus", help="Set 1 to write out the scraped data to CSV file through output from MySQL database. Set 0 to write out the scraped data to CSV file through output from NBA.stats.")

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
    if args.scrape_all_season:
        scrape_all_season = int(args.scrape_all_season)
    if args.write_csv_use_sql:
        write_csv_use_sql = int(args.write_csv_use_sql)

    return(thresh_change_proxy, thresh_change_proxy_list, is_debug, out_file_name, indexing_to_csv, team, password, season, mysql_password, table, unix_socket, database_name, scrape_all_season, write_csv_use_sql)

#-----------------Execution------------------#
if __name__ == '__main__':
    main()
