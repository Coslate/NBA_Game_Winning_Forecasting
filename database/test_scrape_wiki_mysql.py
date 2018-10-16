#! /usr/bin/env python3.6
import pymysql
import re
import random
import datetime
import sys
import argparse
import os
#import package_crawler_nba.crawler_nba as crawler_nba

#########################
#     Main-Routine      #
#########################
def main():
    #Initialization
    crawler_nba.init()

    #Argument Parser
    (password, table) = ArgumentParser()

    #DB Initialization
    crawler_nba.MySQLDBInitialize(password, table)

    #Sideband Setting
    current_time = datetime.datetime.now()
    print(f'current_time = {current_time}')
    random.seed(datetime.datetime.now())

    starting_url = "https://en.wikipedia.org/wiki/Kevin_Bacon"
    print(f'starting_url = {starting_url}')

    print('Get Wiki Links and store the content to MySQL...')
    all_internal_links_loop = crawler_nba.GetWikiLinksContent(starting_url,cur, table)
    for internal_link in all_internal_links_loop:
        print(f'internal_link = {internal_link}')

#########################
#     Sub-Routine       #
#########################
def ArgumentParser():
    password = ""
    table    = ""

    parser = argparse.ArgumentParser()
    parser.add_argument("--mysql_password", "-sql_p", help="The password to connect to MySQL server.", required=True)
    parser.add_argument("--mysql_table_name", "-sql_tn", help="The table name that will be used to store data.", required=True)

    args = parser.parse_args()

    if args.password:
        password = args.password
    if args.table:
        table = args.table

    return(password, table)

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
