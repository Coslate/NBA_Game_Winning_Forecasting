#! /usr/bin/env python3.6

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import package_crawler_nba.crawler_nba as crawler_nba
import random
import datetime

print(f"time = {datetime.datetime.now()}")

pages_links = set()
recursive_num = 0
crawler_nba.GetAllURLLinks("", 1, pages_links, recursive_num)
