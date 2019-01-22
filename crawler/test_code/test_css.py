#! /usr/bin/env python3.6

from bs4 import BeautifulSoup

css_soup = BeautifulSoup('<p class="boy strikeout"></p>', 'lxml')
p_tag = css_soup.find_all("p", class_="strikeout")
print(p_tag)
