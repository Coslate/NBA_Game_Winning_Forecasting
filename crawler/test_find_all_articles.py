#! /usr/bin/env python3.6

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

html = urlopen("https://en.wikipedia.org/wiki/Kevin_Bacon")
response = BeautifulSoup(html, 'lxml')
#print(response.prettify())
for link in response.findAll("div", {"id":"bodyContent"}):
    url_extrac = link.findAll("a", href = re.compile("^(\/wiki\/)((?!:).)*$"))
    #print(f"link = {link}")
    #print(f'link.attrs = {link.attrs}')
    for ele in url_extrac:
        print("------------------")
        print(f"ele = {ele}")
        print(f"attrs = {ele.attrs}")
        print(f"attrs[href] = {ele.attrs['href']}")
        print("------------------")
