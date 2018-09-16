from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.error import HTTPError
from urllib import error
from bs4 import BeautifulSoup
import re
import sys
import json

def GetAllWikiAtricleLinks(url, is_debug=0):
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

def GetAllURLLinks(url, pages_links, recursive_num, is_debug=0):
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
            try:
                (recursive_num, page_links) = GetAllURLLinks(new_page_link, pages_links, recursive_num, 1)
            except RecursionError:
                print(f"> maximum recursion depth exceeded.")
                print(f"> recursive_num = {recursive_num}")
                print(f"> Program Terminated.")
                return (recursive_num, page_links)

    return (recursive_num, page_links)

def GetEditHistoryIPList(url, is_debug=0):
    # The format of the URL of an editing-history-page is as the following:
    # http://en.wikipedia.org/w/index.php?title=<title_in_url>&action=history
    url = url.replace('/wiki/', '')
    history_url = 'http://en.wikipedia.org/w/index.php?title='+url+'&action=history'
    if(is_debug):
        print(f'history_url = {history_url}')

    html = urlopen(history_url)
    response_obj = BeautifulSoup(html, 'lxml')
    all_ip_possible_address = response_obj.findAll('a', {'class':'mw-userlink mw-anonuserlink'})
    address_list = set()
    for ip_address in all_ip_possible_address:
        ip_address_txt = ip_address.get_text()
        address_list.add(ip_address_txt)

        if(is_debug):
            print('---------------------------')
            print(f"ip_address = {ip_address}")
            print(f"ip_address_txt = {ip_address_txt}")

    return address_list

def GetCountry(ip_address):
    access_key = "7d1d13cee5f609b669d5777029ec0e4f"
    try:
        response = urlopen('http://api.ipstack.com/'+ip_address+'?access_key='+access_key).read().decode('utf-8')
    except error.HTTPError:
        return None
    response_json = json.loads(response)
    return response_json.get('country_name')

def GetInternalLinks(bs_obj, include_url_str, domain):
    internal_links = []
    #Find all the links that begins with '/'
    for link in bs_obj.findAll('a', href=re.compile(include_url_str)):
        if(link.attrs['href'] not in internal_links):
            if(re.match(r'^(/|#)', link.attrs['href']) is not None):
                internal_links.append(domain+link.attrs['href'])
            else:
                internal_links.append(link.attrs['href'])

    return internal_links

def GetExternalLinks(bs_obj, exclude_url_str_list):
    external_links = []
    #Find all the links that begins with 'http' or 'www' except the current URL
#    for link in bs_obj.findAll('a', href=re.compile('^(http|www)((?!{x}).)*$'.format(x=exclude_url_str), re.IGNORECASE)):
    for link in bs_obj.findAll('a', href=re.compile('^(http|www)')):
        get_exclude_str = 0

        for exclude_url_str in exclude_url_str_list:
            print(f'1st exclude_url_str = {exclude_url_str}')
            p = re.compile('{x}'.format(x = exclude_url_str), re.IGNORECASE)
            m = p.match(link.attrs['href'])
            if(m is not None):
                get_exclude_str = 1
                print(f'm--exclude_url_str = {exclude_url_str}')
                print(f'm--link = {link}')
                break

        if(not get_exclude_str):
            print(f'get_exclude_str = {get_exclude_str}')
            if(link.attrs['href'] not in external_links):
                external_links.append(link.attrs['href'])

    return external_links

def GetAllInternalLinks(starting_url):
    print('---------------crawler_nba.GetAllInternalLinks begins-------------------')
    all_internal_links = []
    internal_url_pattern_str = ""
    internal_url_pattern = re.compile(r'.*www.(\S*)\.com.*')
    internal_url_pattern_match = internal_url_pattern.match(starting_url)
    if(internal_url_pattern_match is not None):
        internal_url_pattern_str = internal_url_pattern_match.group(1)
    else:
        internal_url_pattern = re.compile(r'(\S*)\..*')
        internal_url_pattern_match = internal_url_pattern.match(urlparse(starting_url).netloc)
        internal_url_pattern_str = internal_url_pattern_match.group(1)

    print(f'internal_url_pattern_str = {internal_url_pattern_str}')

    try:
        html = urlopen(starting_url)
    except HTTPError:
        print(f'Cannot access {starting_url}')
        return all_internal_links

    bs_obj = BeautifulSoup(html, 'lxml')

    domain = urlparse(starting_url).scheme+"://"+urlparse(starting_url).netloc
    print(f'domain = {domain}')
    all_internal_links = GetInternalLinks(bs_obj, internal_url_pattern_str, domain)

    for ele in all_internal_links:
        print(f'internal link = {ele}')
    print('---------------crawler_nba.GetAllInternalLinks ends-------------------')

    return all_internal_links

def GetAllExternalLinks(starting_url, external_link_str_list):
    print('---------------crawler_nba.GetAllExternalLinks begins-------------------')
    all_external_links = []
    external_url_pattern_str = ""
    external_url_pattern = re.compile(r'.*www.(\S*)\.com.*')
    external_url_pattern_match = external_url_pattern.match(starting_url)
    if(external_url_pattern_match is not None):
        external_url_pattern_str = external_url_pattern_match.group(1)
    else:
        external_url_pattern = re.compile(r'(\S*)\..*')
        external_url_pattern_match = external_url_pattern.match(urlparse(starting_url).netloc)
        external_url_pattern_str = external_url_pattern_match.group(1)

    print(f'external_url_pattern_str = {external_url_pattern_str}')
    if(external_url_pattern_str not in external_link_str_list):
        external_link_str_list.append(external_url_pattern_str)

    try:
        html = urlopen(starting_url)
    except HTTPError:
        print(f'Cannot access {starting_url}')
        return all_external_links

    bs_obj = BeautifulSoup(html, 'lxml')

    domain = urlparse(starting_url).scheme+"://"+urlparse(starting_url).netloc
    print(f'domain = {domain}')
    all_external_links = GetExternalLinks(bs_obj, external_link_str_list)

    for ele in all_external_links:
        print(f'external link = {ele}')
    print('---------------crawler_nba.GetAllExternalLinks ends-------------------')

    return all_external_links


def GetAllExternalLinksThrInternalLinks(url, all_external_links, all_internal_links, external_link_str_list):
    recursive_err = 0
    all_internal_links_loop = GetAllInternalLinks(url)
    all_external_links_loop = GetAllExternalLinks(url, external_link_str_list)

    for external_link in all_external_links_loop:
        if external_link not in all_external_links:
            all_external_links.append(external_link)
            print(f'--> added external_link = {external_link}')

    for internal_link in all_internal_links_loop:
        if internal_link not in all_internal_links:
            all_internal_links.append(internal_link)
            print(f'--> added internal_link = {internal_link}')
            print(f'About to get internal_link = {internal_link}')
            try:
                (all_external_links, all_internal_links, recursive_err) = GetAllExternalLinksThrInternalLinks(internal_link, all_external_links, all_internal_links, external_link_str_list)
                if(recursive_err):
                    break
            except RecursionError:
                recursive_err = 1
                print("Maximum recursive error occurs. Return...")
                print(f"recursive_err = {recursive_err}")
                break

    return (all_external_links, all_internal_links, recursive_err)



