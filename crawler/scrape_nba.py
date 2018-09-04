#! /usr/bin/env python3.6

from   bs4 import BeautifulSoup
import requests



#########################
#     Main-Routine      #
#########################
def main():
    url = "https://stats.nba.com/players/advanced-leaders"
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
    data        = soup.find_all('div', {"class":"r-ent"})
    print(f'data = {data}')

#---------------Execution---------------#
if __name__ == '__main__':
    main()
