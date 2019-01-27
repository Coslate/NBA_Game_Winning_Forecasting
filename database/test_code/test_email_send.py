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
    #Argument Parser
    (password) = ArgumentParser()

    gmail_user = 'coslate@media.ee.ntu.edu.tw'
    gmail_password = password # your gmail password
    content = 'Excel File Test2'
    title = 'Test2'
    to_addr = 'vickiehsu828@gmail.com'

    email.SendMail(gmail_user, gmail_password, content, title, to_addr)

'''
    msg = MIMEText('Excel File')
    msg['Subject'] = 'Test'
    msg['From'] = gmail_user
    msg['To'] = 'vickiehsu828@gmail.com'

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.send_message(msg)
    server.quit()

    print('Email sent!')
'''

#########################
#     Sub-Routine       #
#########################
def ArgumentParser():
    password = ""

    parser = argparse.ArgumentParser()
    parser.add_argument("--gmail_password", "-gmail_p", help="The password of your gmail.", required=True)

    args = parser.parse_args()

    if args.gmail_password:
        password = args.gmail_password

    return(password)

#-----------------Execution------------------#
if __name__ == '__main__':
    import sys
    this_script_path = os.path.realpath(__file__)
    this_script_folder = os.path.dirname(this_script_path)
    crawler_nba_pkg_path = this_script_folder+'/../crawler'
    print('Add to sys.path : {x}'.format(x=crawler_nba_pkg_path))
    sys.path.append(crawler_nba_pkg_path)
    import package_email.email as email
    print('Import package_email successfully.')

    main()
