#! /usr/bin/env python3.6

from   urllib.error import HTTPError
from   bs4 import BeautifulSoup
import requests
import re



#########################
#     Main-Routine      #
#########################
def main():
    url = "http://stats.nba.com/teams/boxscores/"
    GetThePageAndUpdateURL(url)


#########################
#     Sub-Routine       #
#########################
def GetThePageAndUpdateURL(url):
    #--------------------------------------------------------------
    #Step1. Issue Request.
    #--------------------------------------------------------------
    response = None
    while(response is None):
        try:
            response = requests.get(url, cookies = {'over18':"1"}, verify = False)
        except HTTPError as e:
            print(e)
            sys.exit()
        except:
            print("Connection refused by the server..")
            print("Reconnected after 5 seconds")
            print("...")
            time.sleep(5)
            print("Continuing...")
            continue

    #--------------------------------------------------------------
    #Step2. Interpret Response with Beautifulsoup.
    #--------------------------------------------------------------

    soup        = BeautifulSoup(response.text, 'lxml')
    print(soup.prettify())
    data        = soup.find_all('a', {"ng-href" : "/game/0021701226", "href" : "\/game\/0021701226"})
    for x in data:
        print(f'data = {x}')

#---------------Execution---------------#
if __name__ == '__main__':
    main()
