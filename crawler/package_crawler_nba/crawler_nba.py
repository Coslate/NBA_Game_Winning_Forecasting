from urllib import request
from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.error import HTTPError
from urllib import error
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import package_tool_surf.tool_surf as tool_surf
import re
import sys
import json
import http.client
import random
import time

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
            if(re.match(r'^(/|#|[a-zA-z0-9])', link.attrs['href']) is not None):
                if(re.match(r'^(https|http)', link.attrs['href']) is not None):
                    internal_links.append(link.attrs['href'])
                else:
                    if(re.match(r'.*:.*', link.attrs['href']) is not None):
                        pass
                    else:
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
            p = re.compile('.*{x}.*'.format(x = exclude_url_str), re.IGNORECASE)
            m = p.match(link.attrs['href'])
            if(m is not None):
                get_exclude_str = 1
                break

        if(not get_exclude_str):
            if(link.attrs['href'] not in external_links):
                external_links.append(link.attrs['href'])

    return external_links

def SetProxy(proxy):
    print(f'Set proxy : {proxy}')
    try :
        proxy_support = request.ProxyHandler({'http':proxy,
                                          'https':proxy})
        opener = request.build_opener(proxy_support)
        request.install_opener(opener)
        ip_addr = tool_surf.GetPublicIPAddress()
        print(f'Set ip address = {ip_addr}')
    except Exception as err :
        print(err)
        print('Randomly get new proxy.')
        proxy_index = RandomProxy(proxy_list)
        proxy_used = proxy_list[proxy_index]
        SetProxy(proxy_used['ip']+':'+proxy_used['port'])




def GetAllInternalLinks(starting_url, thresh_change_proxy, thresh_change_proxy_list, all_internal_links):
    global request_num
    global proxy_list
    global proxy_used
    global proxy_index

    print('---------------crawler_nba.GetAllInternalLinks begins-------------------')
    print(f'starting_url = {starting_url}')
    print(f'request_num = {request_num}')
    all_internal_links_loop = []
    internal_url_pattern_str = ""
    internal_url_pattern = re.compile(r'.*www.(\S*?)\.com.*')
    internal_url_pattern_match = internal_url_pattern.match(starting_url)
    if(internal_url_pattern_match is not None):
        internal_url_pattern_str = internal_url_pattern_match.group(1)
    else:
        internal_url_pattern = re.compile(r'(\S*?)\..*')
        internal_url_pattern_match = internal_url_pattern.match(urlparse(starting_url).netloc)
        internal_url_pattern_str = internal_url_pattern_match.group(1)

    print(f'internal_url_pattern_str = {internal_url_pattern_str}')

    try:
        ip_addr = tool_surf.GetPublicIPAddress()
        print(f'ip address = {ip_addr}')

        head = {}
        #user_agent = random.choice(USER_AGENT_LIST)
        ua = UserAgent()
        user_agent = ua.random
        head['User-Agent'] = user_agent
        print(f'user_agent = {head["User-Agent"]}')

        if(request_num % thresh_change_proxy == 0):
            if(request_num != 0):
                print(f'Request number reaches {thresh_change_proxy}. Change the proxy.')
            if(proxy_index != -1):
                del proxy_list[proxy_index]

            proxy_index = RandomProxy(proxy_list)
            proxy_used = proxy_list[proxy_index]
            SetProxy(proxy_used['ip']+':'+proxy_used['port'])
        if((request_num % thresh_change_proxy_list == 0) and (request_num != 0)):
            print(f'Request number reaches {thresh_change_proxy_list}. Change the proxy list.')
            proxy_list = GetProxyList(1)

        req = request.Request(starting_url, headers=head)
        html = urlopen(req)
        request_num += 1
    except HTTPError as err:
        print(f'Cannot access {starting_url}. {err}')
        if(re.match(r'\s*HTTP\s*Error\s*404.*', str(err)) is not None):
            print(f'Remove the url : {starting_url}')
            if(any(url_check == starting_url for url_check in all_internal_links)):
                all_internal_links.remove(starting_url)

        return all_internal_links_loop
    except http.client.RemoteDisconnected as disconnected_err:
        print(f'Cannot access {starting_url}. RemoteDisconnected. {disconnected_err}')
        print(f'Randomly set new proxy, and try again.')
        if(any(((proxy_in_list['ip'] == proxy_used['ip']) and (proxy_in_list['port'] == proxy_used['port'])) for proxy_in_list in proxy_list)):
            proxy_list.remove(proxy_used)

        #randomly set new proxy
        proxy_index = RandomProxy(proxy_list)
        proxy_used = proxy_list[proxy_index]
        SetProxy(proxy_used['ip']+':'+proxy_used['port'])
        all_internal_links_loop = GetAllInternalLinks(starting_url, thresh_change_proxy, thresh_change_proxy_list, all_internal_links)
        return all_internal_links_loop
    except error.URLError as err:
        print(f'Cannot access {starting_url}. Remote end closed connection without response. {err}')
        print(f'Randomly set new proxy, and try again.')
        if(any(((proxy_in_list['ip'] == proxy_used['ip']) and (proxy_in_list['port'] == proxy_used['port'])) for proxy_in_list in proxy_list)):
            proxy_list.remove(proxy_used)

        #randomly set new proxy
        proxy_index = RandomProxy(proxy_list)
        proxy_used = proxy_list[proxy_index]
        SetProxy(proxy_used['ip']+':'+proxy_used['port'])
        all_internal_links_loop = GetAllInternalLinks(starting_url, thresh_change_proxy, thresh_change_proxy_list, all_internal_links)
        return all_internal_links_loop
    except Exception as err:
        print('Unexpected Error occurs : {x}. Cannot access {y}.'.format(x = err, y = starting_url))
        return all_internal_links_loop

    bs_obj = BeautifulSoup(html, 'lxml')
    domain = urlparse(starting_url).scheme+"://"+urlparse(starting_url).netloc
    print(f'domain = {domain}')
    all_internal_links_loop = GetInternalLinks(bs_obj, internal_url_pattern_str, domain)

    for ele in all_internal_links_loop:
        print(f'this loop internal link = {ele}')
    print('---------------crawler_nba.GetAllInternalLinks ends-------------------')

    return all_internal_links_loop

def GetAllExternalLinks(starting_url, external_link_str_list, thresh_change_proxy, thresh_change_proxy_list, all_external_links):
    global request_num
    global proxy_list
    global proxy_used
    global proxy_index

    print('---------------crawler_nba.GetAllExternalLinks begins-------------------')
    print(f'starting_url = {starting_url}')
    print(f'request_num = {request_num}')
    all_external_links_loop = []
    external_url_pattern_str = ""
    external_url_pattern = re.compile(r'.*www.(\S*?)\.com.*')
    external_url_pattern_match = external_url_pattern.match(starting_url)
    if(external_url_pattern_match is not None):
        external_url_pattern_str = external_url_pattern_match.group(1)
    else:
        external_url_pattern = re.compile(r'(\S*?)\..*')
        external_url_pattern_match = external_url_pattern.match(urlparse(starting_url).netloc)
        external_url_pattern_str = external_url_pattern_match.group(1)

    print(f'external_url_pattern_str = {external_url_pattern_str}')
    if(external_url_pattern_str not in external_link_str_list):
        external_link_str_list.append(external_url_pattern_str)

    try:
        ip_addr = tool_surf.GetPublicIPAddress()
        print(f'ip address = {ip_addr}')

        head = {}
        #user_agent = random.choice(USER_AGENT_LIST)
        ua = UserAgent()
        user_agent = ua.random
        head['User-Agent'] = user_agent
        print(f'user_agent = {user_agent}')

        if(request_num % thresh_change_proxy == 0):
            if(request_num != 0):
                print(f'Request number reaches {thresh_change_proxy}. Change the proxy.')
            if(proxy_index != -1):
                del proxy_list[proxy_index]

            proxy_index = RandomProxy(proxy_list)
            proxy_used = proxy_list[proxy_index]
            SetProxy(proxy_used['ip']+':'+proxy_used['port'])
        if((request_num % thresh_change_proxy_list == 0) and (request_num != 0)):
            print(f'Request number reaches {thresh_change_proxy_list}. Change the proxy list.')
            proxy_list = GetProxyList(1)

        req = request.Request(starting_url, headers=head)
        html = urlopen(req)
        request_num += 1
    except HTTPError as err:
        print(f'Cannot access {starting_url}. {err}')
        if(re.match(r'\s*HTTP\s*Error\s*404.*', str(err)) is not None):
            print(f'Remove the url : {starting_url}')
            if(any(url_check == starting_url for url_check in all_external_links)):
                all_external_links.remove(starting_url)

        return all_external_links_loop
    except http.client.RemoteDisconnected as disconnected_err:
        print(f'Cannot access {starting_url}. RemoteDisconnected. {disconnected_err}')
        print(f'Randomly set new proxy, and try again.')
        if(any(((proxy_in_list['ip'] == proxy_used['ip']) and (proxy_in_list['port'] == proxy_used['port'])) for proxy_in_list in proxy_list)):
            proxy_list.remove(proxy_used)

        #randomly set new proxy
        proxy_index = RandomProxy(proxy_list)
        proxy_used = proxy_list[proxy_index]
        SetProxy(proxy_used['ip']+':'+proxy_used['port'])

        all_external_links_loop = GetAllExternalLinks(starting_url, external_link_str_list, thresh_change_proxy, thresh_change_proxy_list, all_external_links)
        return all_external_links_loop
    except error.URLError as err:
        print(f'Cannot access {starting_url}. Remote end closed connection without response. {err}')
        print(f'Randomly set new proxy, and try again.')
        if(any(((proxy_in_list['ip'] == proxy_used['ip']) and (proxy_in_list['port'] == proxy_used['port'])) for proxy_in_list in proxy_list)):
            proxy_list.remove(proxy_used)

        #randomly set new proxy
        proxy_index = RandomProxy(proxy_list)
        proxy_used = proxy_list[proxy_index]
        SetProxy(proxy_used['ip']+':'+proxy_used['port'])

        all_external_links_loop = GetAllExternalLinks(starting_url, external_link_str_list, thresh_change_proxy, thresh_change_proxy_list, all_external_links)
        return all_external_links_loop
    except Exception as err:
        print('Unexpected Error occurs : {x}. Cannot access {y}.'.format(x = err, y = starting_url))
        return all_external_links_loop

    bs_obj = BeautifulSoup(html, 'lxml')
    domain = urlparse(starting_url).scheme+"://"+urlparse(starting_url).netloc
    print(f'domain = {domain}')
    all_external_links_loop = GetExternalLinks(bs_obj, external_link_str_list)

    for ele in all_external_links_loop:
        print(f'this loop external link = {ele}')
    print('---------------crawler_nba.GetAllExternalLinks ends-------------------')

    return all_external_links_loop


def GetAllExternalLinksThrInternalLinks(url, all_external_links, all_internal_links, external_link_str_list, thresh_change_proxy, thresh_change_proxy_list):
    recursive_err = 0
    all_internal_links_loop = GetAllInternalLinks(url, thresh_change_proxy, thresh_change_proxy_list, all_internal_links)
    all_external_links_loop = GetAllExternalLinks(url, external_link_str_list, thresh_change_proxy, thresh_change_proxy_list, all_external_links)

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
                (all_external_links, all_internal_links, recursive_err) = GetAllExternalLinksThrInternalLinks(internal_link, all_external_links, all_internal_links, external_link_str_list, thresh_change_proxy, thresh_change_proxy_list)
                if(recursive_err):
                    break
            except RecursionError:
                recursive_err = 1
                print("Maximum recursive error occurs. Return...")
                print(f"recursive_err = {recursive_err}")
                break

    return (all_external_links, all_internal_links, recursive_err)

def RandomProxy(proxy_list):
    return random.randint(0, len(proxy_list)-1)

def GetProxyList(is_debug):
    #proxy_list_url = 'http://www.freeproxylists.net/zh/'
    proxy_list_url = 'https://www.sslproxies.org/'
    proxy_list = []
    head = {}
    #user_agent = random.choice(USER_AGENT_LIST)
    ua = UserAgent()
    user_agent = ua.random
    head['User-Agent'] = user_agent
    print(f'user_agent = {head["User-Agent"]}')

    try:
        req = request.Request(proxy_list_url, headers=head)
        html = urlopen(req)
    except Exception as err:
        print('Unexpected Error occurs during scraping proxy list : {x}. Cannot access {y}.'.format(x = err, y = proxy_list_url))
        print('Sleep 5 minutes and try again.')
        time.sleep(5*60)
        return GetProxyList(1)

    bs_obj = BeautifulSoup(html, 'lxml')
    proxy_table = bs_obj.find('table', {'id' : 'proxylisttable'})
    for row in proxy_table.tbody.findAll('tr'):
        anonymity    = row.findAll('td')[4].string

        if(re.match(r'elite\s*proxy', anonymity) is not None):
            ip_address = row.findAll('td')[0].string
            ip_port    = row.findAll('td')[1].string
            ip_country = row.findAll('td')[3].string
            ip_region  = row.findAll('td')[2].string

            proxy_list.append({
                'ip':   ip_address,
                'port': ip_port
            })
            if(is_debug):
                print('-----------------------')
                print(f'PROXY, ip_address   = {ip_address}')
                print(f'PROXY, ip_port      = {ip_port}')
                print(f'PROXY, anonymity    = {anonymity}')
                print(f'PROXY, ip_country   = {ip_country}')
                print(f'PROXY, ip_region    = {ip_region}')

    return proxy_list

def init():
    print('--------------------------Initialization--------------------------')
    global request_num
    global USER_AGENT_LIST
    global proxy_list
    global proxy_used
    global proxy_index

    request_num = 0
    proxy_index = -1
    proxy_used  = {}
    proxy_list  = []
    proxy_list  = GetProxyList(0)
    proxy_index = RandomProxy(proxy_list)
    proxy_used  = proxy_list[proxy_index]

    print('--------------------------Resolve "http.client.IncompleteRead" Error--------------------------')
    http.client.HTTPConnection._http_vsn = 10
    http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'

    USER_AGENT_LIST = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    ]
