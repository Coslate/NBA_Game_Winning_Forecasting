#! /usr/bin/env python3.6

from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("https://en.wikipedia.org/wiki/Kevin_Bacon")
response = BeautifulSoup(html, 'lxml')
#print(response.prettify())
for link in response.findAll("a"):
    print(f"link = {link}")
    print(f'link.attrs = {link.attrs}')
    if('href' in link.attrs):
        href_link = link.attrs['href']
        print(f'link.attrs[\'href\'] = {href_link}')
