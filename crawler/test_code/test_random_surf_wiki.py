#! /usr/bin/env python3.6

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import package_crawler_nba.crawler_nba as crawler_nba
import random
import datetime

print(f"time = {datetime.datetime.now()}")

first_link = "/wiki/Kevin_Bacon"
print(f"first_link = {first_link}")
random.seed(datetime.datetime.now())
links = crawler_nba.GetAllWikiAtricleLinks(first_link, 0)
len_links = len(links)

while(len_links > 0):
    rand_int = random.randint(0, len_links-1)
    random_selected_links = links[rand_int].attrs['href']
    print("-----------------------------------")
    print(f"get from {len_links} links :")
    print(f"random_selected_links = {random_selected_links}")

    #Update new links through random selected links
    links = crawler_nba.GetAllWikiAtricleLinks(random_selected_links, 0)
    len_links = len(links)

