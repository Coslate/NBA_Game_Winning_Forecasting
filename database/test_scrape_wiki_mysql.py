#! /usr/bin/env python3.6
import pymysql
import re
import random
import datetime
import sys
import argparse
import os

#########################
#     Main-Routine      #
#########################
def main():
    #Initialization
    iter_num = 0
    crawler_nba.init()

    #Argument Parser
    (password, table, max_sql_store_num) = ArgumentParser()

    #DB Initialization
    crawler_nba.MySQLDBInitialize(password, table)

    #Sideband Setting
    current_time = datetime.datetime.now()
    print(f'current_time = {current_time}')
    random.seed(datetime.datetime.now())

    starting_url = "https://en.wikipedia.org/wiki/Kevin_Bacon"
    print(f'starting_url = {starting_url}')

    choose_link = starting_url
    while(iter_num < max_sql_store_num):
        print('iter_num = {}. Get Wiki Links and store the content to MySQL...'.format(iter_num))
        print(f'choose_link = {choose_link}')
        all_internal_links_loop = crawler_nba.GetWikiLinksContent(choose_link, crawler_nba.cur, table)
        total_num_internal_links_loop = len(all_internal_links_loop)

        if(total_num_internal_links_loop > 0):
            choose_link = "http://en.wikipedia.org"+all_internal_links_loop[random.randint(0, total_num_internal_links_loop-1)].attrs['href']
        iter_num += 1

    crawler_nba.MySQLDBClose(crawler_nba.cur, crawler_nba.conn)
#########################
#     Sub-Routine       #
#########################
def ArgumentParser():
    password = ""
    table    = ""
    max_sql_store_num = 10

    parser = argparse.ArgumentParser()
    parser.add_argument("--mysql_password", "-sql_p", help="The password to connect to MySQL server.", required=True)
    parser.add_argument("--mysql_table_name", "-sql_tn", help="The table name that will be used to store data.", required=True)
    parser.add_argument("--max_sql_store_num", "-sql_mx_sn", help="The maximum number that stores in MySQL table.", required=True)

    args = parser.parse_args()

    if args.mysql_password:
        password = args.mysql_password
    if args.mysql_table_name:
        table = args.mysql_table_name
    if args.max_sql_store_num:
        max_sql_store_num = int(args.max_sql_store_num)

    return(password, table, max_sql_store_num)

#-----------------Execution------------------#
if __name__ == '__main__':
    import sys
    this_script_path = os.path.realpath(__file__)
    this_script_folder = os.path.dirname(this_script_path)
    crawler_nba_pkg_path = this_script_folder+'/../crawler'
    print('Add to sys.path : {x}'.format(x=crawler_nba_pkg_path))
    sys.path.append(crawler_nba_pkg_path)
    import package_crawler_nba.crawler_nba as crawler_nba
    print('Import package_crawler_nba successfully.')

    main()
