#! /usr/bin/env python3.6

import random
import datetime
import package_crawler_nba.crawler_nba as crawler_nba

random.seed(datetime.datetime.now())

initial_page = '/wiki/Python_(programming_language)'
print(f'initial_page = {initial_page}')
all_article_links = crawler_nba.GetAllWikiAtricleLinks(initial_page)
all_article_links_len = len(all_article_links)
while(all_article_links_len > 0):
    for link in all_article_links:
        print('--------------')
        link_url = link.attrs['href']
        print(f'link_url = {link_url}')
        history_ip_address_list = crawler_nba.GetEditHistoryIPList(link.attrs['href'])
        for history_ip in history_ip_address_list:
            country = crawler_nba.GetCountry(history_ip)
            print(f'{history_ip} is from {country}')

    new_article_link = all_article_links[random.randint(0, all_article_links_len-1)].attrs['href']
    print(f'new_article_page = {new_article_link}')
    all_article_links = crawler_nba.GetAllWikiAtricleLinks(new_article_link)
    all_article_links_len = len(all_article_links)


