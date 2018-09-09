from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

def GetAllWikiAtricleLinks(url, is_debug):
    html = urlopen("http://en.wikipedia.org"+url)
    response = BeautifulSoup(html, 'lxml')
    ret_all_article_links = []
    all_div_tags = response.findAll('div', {"id":"bodyContent"})

    for ele_tags in all_div_tags:
        ret_all_article_links += ele_tags.findAll('a', href=re.compile("^(\/wiki\/)((?!:).)*$"))

    if(is_debug):
        for ele in ret_all_article_links:
            print("------------------")
            print(f"ele = {ele}")
            print(f"attrs = {ele.attrs}")
            print(f"attrs[href] = {ele.attrs['href']}")
            print("------------------")

    return ret_all_article_links

def GetAllURLLinks(url, is_debug, pages_links, recursive_num):
    recursive_num += 1
    html = urlopen("http://en.wikipedia.org"+url)
    response = BeautifulSoup(html, 'lxml')
    ret_all_article_links = []
    all_div_tags = response.findAll('a', href=re.compile('^(\/wiki\/)((?!User).)*$'))

    print('----------------------')
    print(f'original page_links = {pages_links}')
    print(f'recursive_num = {recursive_num}')
    print('----------------------')
    for ele_tags in all_div_tags:
        if(ele_tags.attrs['href'] not in pages_links):
            new_page_link = ele_tags.attrs['href']
            print('----------------------')
            print(f'new_page_link = {new_page_link}')
            print('----------------------')
            pages_links.add(new_page_link)
            GetAllURLLinks(new_page_link, 1, pages_links, recursive_num)

