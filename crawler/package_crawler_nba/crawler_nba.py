from urllib import request
from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.error import HTTPError
from urllib import error
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from tabulate import tabulate
import pandas as pd
import package_tool_surf.tool_surf as tool_surf
import package_email.email as email
import re
import sys
import json
import http.client
import random
import time
import pymysql

def MySQLDBClose(cur, conn):
    cur.close()
    conn.close()
    print('Close MySQL Database connection.')

def MySQLDBInitialize(password, table, unix_socket, database_name):
    global conn
    global cur
    conn = pymysql.connect(host       ='localhost',
                           unix_socket= unix_socket,
                           user       ='root',
                           passwd     = password,
                           db         ='mysql')
    cur = conn.cursor()
    cur.execute('CREATE DATABASE IF NOT EXISTS {x};'.format(x=database_name))
    cur.execute('USE {x};'.format(x=database_name))
    cur.execute('DROP TABLE IF EXISTS {x};'.format(x=table))
    cur.execute('CREATE TABLE IF NOT EXISTS {x} (id BIGINT(7) NOT NULL AUTO_INCREMENT\
                , title VARCHAR(255)\
                , url VARCHAR(255)\
                , content TEXT(65535)\
                , created TIMESTAMP DEFAULT CURRENT_TIMESTAMP\
                , PRIMARY KEY (id)\
                , UNIQUE KEY title_idx (title)\
                , UNIQUE KEY url_idx (url)\
                , UNIQUE KEY created_idx (created));'.format(x=table))

                #, UNIQUE KEY content_idx (content));'.format(x=table))

def StoreWikiToMySQL(table, cur, url, title, content):
    print('Storing...')
    print(f'table   = {table}')
    print(f'title   = {title}')
    print(f'url     = {url}')
    print(f'content = {content}')

    title   = '"'+title+'"'
    url     = '"'+url+'"'
    content = '"'+content+'"'

    cur.execute('SELECT * FROM {x} WHERE url={url_name}'.format(x=table, url_name=url))
    if cur.rowcount==0:
        execute_str = 'INSERT INTO {table_name} (title, url, content) VALUES ({title_name}, {url_name}, {content_name});'.format(table_name = table, url_name = url, title_name = title, content_name = content)
        print(f'execute_str = {execute_str}')
        cur.execute(execute_str)
        cur.connection.commit()
        return 0;
    else:
        print('Already existed. Skipping...')
        return 1;

def GetNBADataRequest(starting_url, thresh_change_proxy, thresh_change_proxy_list):
    print("> GetNBADataRequest...")
    global request_num
    global proxy_list
    global proxy_used
    global proxy_index

    print('---------------crawler_nba.GetNBADataRequest begins-------------------')
    print(f'starting_url = {starting_url}')
    print(f'request_num = {request_num}')

    all_data_loop          = []
    all_data_item_href     = []
    columns                = []

    try:
        ip_addr = tool_surf.GetPublicIPAddress()
        print(f'ip address = {ip_addr}')

        if(request_num % thresh_change_proxy == 0):
            if(proxy_index != -1):
                del proxy_list[proxy_index]

            if(request_num != 0):
                print(f'Request number reaches {thresh_change_proxy}. Change the proxy.')
                proxy_index = RandomProxy(proxy_list)
                proxy_used = proxy_list[proxy_index]
                SetProxy(proxy_used['ip']+':'+proxy_used['port'])
        if((request_num % thresh_change_proxy_list == 0) and (request_num != 0)):
            print(f'Request number reaches {thresh_change_proxy_list}. Change the proxy list.')
            proxy_list = GetProxyList(1)

        print("> Use Webdriver...")
        browser = webdriver.Chrome()
        browser.get(starting_url)
        request_num += 1
    except HTTPError as err:
        print(f'Cannot access {starting_url}. {err}')
        if(re.match(r'\s*HTTP\s*Error\s*404.*', str(err)) is not None):
            print(f'Return with original data.')

        return (all_data_loop, columns, browser, all_data_item_href)
    except http.client.RemoteDisconnected as disconnected_err:
        print(f'Cannot access {starting_url}. RemoteDisconnected. {disconnected_err}')
        print(f'Randomly set new proxy, and try again.')
        if(any(((proxy_in_list['ip'] == proxy_used['ip']) and (proxy_in_list['port'] == proxy_used['port'])) for proxy_in_list in proxy_list)):
            proxy_list.remove(proxy_used)

        #randomly set new proxy
        proxy_index = RandomProxy(proxy_list)
        proxy_used = proxy_list[proxy_index]
        SetProxy(proxy_used['ip']+':'+proxy_used['port'])
        (all_data_loop, columns, browser, all_data_item_href)  = GetNBADataRequest(starting_url, thresh_change_proxy, thresh_change_proxy_list)
        return (all_data_loop, columns, browser, all_data_item_href)
    except error.URLError as err:
        print(f'Cannot access {starting_url}. Remote end closed connection without response. {err}')
        print(f'Randomly set new proxy, and try again.')
        if(any(((proxy_in_list['ip'] == proxy_used['ip']) and (proxy_in_list['port'] == proxy_used['port'])) for proxy_in_list in proxy_list)):
            proxy_list.remove(proxy_used)

        #randomly set new proxy
        proxy_index = RandomProxy(proxy_list)
        proxy_used = proxy_list[proxy_index]
        SetProxy(proxy_used['ip']+':'+proxy_used['port'])
        (all_data_loop, columns, browser, all_data_item_href) = GetNBADataRequest(starting_url, thresh_change_proxy, thresh_change_proxy_list)
        return (all_data_loop, columns, browser, all_data_item_href)
    except Exception as err:
        print('Unexpected Error occurs : {x}. Cannot access {y}.'.format(x = err, y = starting_url))
        print(f'Randomly set new proxy, and try again.')
        if(any(((proxy_in_list['ip'] == proxy_used['ip']) and (proxy_in_list['port'] == proxy_used['port'])) for proxy_in_list in proxy_list)):
            proxy_list.remove(proxy_used)

        #randomly set new proxy
        proxy_index = RandomProxy(proxy_list)
        proxy_used = proxy_list[proxy_index]
        SetProxy(proxy_used['ip']+':'+proxy_used['port'])
        (all_data_loop, columns, browser, all_data_item_href) = GetNBADataRequest(starting_url, thresh_change_proxy, thresh_change_proxy_list)
        return (all_data_loop, columns, browser, all_data_item_href)

    time.sleep(5)

    #Set Page to 'All'
    #browser.find_element_by_xpath('/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[3]/div/div/select/option[1]').click()

    #Get the data table by css
    table = browser.find_elements_by_class_name('nba-stat-table__overflow')
    print(f'type of table = {type(table)}')
    columns = GetNBAData(table, all_data_loop, all_data_item_href, browser)
    print('---------------crawler_nba.GetNBADataRequest ends-------------------')

    return (all_data_loop, columns, browser, all_data_item_href)

def GetNBAData(table_obj, all_data_loop, all_data_item_href, browser):
    print("> GetNBAData...")
    if(len(table_obj) > 1):
        print("Error: table_obj has more than one candidate. Need to specify which data table to use.")
        sys.exit(1)

    table_cand  = table_obj[0]
    columns_item=table_cand.find_elements_by_xpath('.//thead/tr/th')
    columns     =[x.text if(x.text != '') else None for x in columns_item]
    print('---')
    print(f'columns = {columns}')
    print('---')
    data_all_lines = table_cand.find_elements_by_xpath('.//tbody/tr')
    num_data_all_lines = len(data_all_lines)
    print(f'len(data_all_lines) = {num_data_all_lines}')

    i=0
    for data_line in data_all_lines:
        print('> Progress = {:.2f}%'.format((i/num_data_all_lines)*100))
        data_item = data_line.find_elements_by_xpath('.//td')
        data_revised_line = [x.text if(x.text != '') else None for x in data_item]
        all_data_loop.append(data_revised_line)
        game_set = data_item[1].find_element_by_xpath('.//a')
        all_data_item_href.append(game_set.get_attribute('href'))
        i += 1

    print('> Progress = {:.2f}%'.format(((i+1)/num_data_all_lines)*100))
    return columns

def GetStartersOfEachGame(href_list, browser, team_list, starters_data_dict):
    for (index, team) in enumerate(team_list):
        print(f'index = {index}, team = {team}, href = {href_list[index]}')
        if(team in starters_data_dict):
            continue
        else:
            #Get statistics of the starters of the team
            browser.get(href_list[index])
            team_name_list     = browser.find_elements_by_xpath("//td[@class='team-name show-for-medium']")
            print(f'len of team_name_list = {len(team_name_list)}')
            players_table_list = browser.find_elements_by_class_name('nba-stat-table__overflow')
            print(f'len of players_table_list = {len(players_table_list)}')

            for (j, team_scraped) in enumerate(team_name_list):
                print(f'team_scraped = {team_scraped.text}')
                columns_item=players_table_list[j].find_elements_by_xpath('.//thead/tr/th')
                columns     =[x.text if(x.text != '') else None for x in columns_item]
                print('---')
                print(f'columns = {columns}')
                print('---')
                data_all_lines = players_table_list[j].find_elements_by_xpath('.//tbody/tr')
                all_data_loop  = []
                num_data_all_lines = 5 #Just get starters(the top 5 players) statistics
                for (i, data_line) in enumerate(data_all_lines):
                    if(i>num_data_all_lines-1):
                        break
                    print('> Progress = {:.2f}%'.format((i/num_data_all_lines)*100))
                    data_item = data_line.find_elements_by_xpath('.//td')
                    data_revised_line = [x.text if(x.text != '') else None for x in data_item]
                    all_data_loop.append(data_revised_line)
                print('> Progress = {:.2f}%'.format((i/num_data_all_lines)*100))
                print('---')
                all_data_df = pd.DataFrame(data = all_data_loop, columns = columns)
                all_data_df.dropna(axis=1, how='all', inplace=True) #Delete the empty columns
                starters_data_dict[team_scraped.text] = all_data_df

    print('===========SHOW==========')
    for (team, data) in starters_data_dict.items():
        print(f'{team} starting players: ')
        content = tabulate(data, headers='keys', tablefmt='psql')
        print(content)
        print('<><><><><><><><><><><><><><><><><><><><><><><><><')
        print('<><><><><><><><><><><>>END<><><><><><><><><><><><')
        print('<><><><><><><><><><><><><><><><><><><><><><><><><')



def CheckDateHasSpecifiedTeam(date, team, all_data_df, browser, all_data_item_href):
    match_list         = list(all_data_df['MATCH UP'].values)
    date_list          = list(all_data_df['GAME DATE'].values)
    index_val_selected = [i for (i, x) in enumerate(match_list) if((re.match(r'.*{}.*'.format(team), x)) and (date_list[i] == date))]
    selected_df_list   = [all_data_df.iloc[index] for index in index_val_selected]
    selected_df        = pd.DataFrame(data=selected_df_list, columns = all_data_df.columns, index=all_data_df.index[0:len(selected_df_list)])

    #Only select a few interested columns to send emails
    short_col_list = ['TEAM', 'GAME DATE', 'W/L', 'PTS']
    short_sel_df   = selected_df[short_col_list]
    get_wanted_data= 1 if(len(selected_df_list) > 1) else 0
    game_set_num   = len(selected_df_list)/2

    #Get the interested game statistics of the starters of the teams
    starters_data_dict = {}
    team_list          = list(selected_df['TEAM'].values)
    href_selected_list = [all_data_item_href[index] for index in index_val_selected]
    GetStartersOfEachGame(href_selected_list, browser, team_list, starters_data_dict)

    return(game_set_num, get_wanted_data, selected_df, short_sel_df, starters_data_dict)

def CheckTeamLose(team, all_data_df):
    team_list  = list(all_data_df['TEAM'].values)
    match_list = list(all_data_df['MATCH UP'].values)
    win_list   = list(all_data_df['W/L'].values)
    index_val_selected = [i for (i, x) in enumerate(team_list) if(((re.match(r'.*{}.*'.format(team), x)) and (win_list[i] == 'L')) or ((not(re.match(r'.*{}.*'.format(team), x))) and (re.match(r'.*{}.*'.format(team), match_list[i])) and (win_list[i] == 'W')))]
    selected_df_list   = [all_data_df.iloc[index] for index in index_val_selected]
    selected_df        = pd.DataFrame(data=selected_df_list, columns = all_data_df.columns, index=all_data_df.index[0:len(selected_df_list)])

    #Only select a few interested columns to send emails
    short_col_list  = ['TEAM', 'GAME DATE', 'W/L', 'PTS']
    short_sel_df    = selected_df[short_col_list]
    get_wanted_data = 1 if(len(selected_df_list) > 1) else 0
    game_set_num    = len(selected_df_list)/2

    return(game_set_num, get_wanted_data, selected_df, short_sel_df)

def CheckSendMails(date_usa, game_set_num, selected_data_df, short_selected_data_df, get_wanted_data, password, team, starters_data_dict):
    if(get_wanted_data):
        gmail_user     = 'coslate@media.ee.ntu.edu.tw'
        gmail_password = password # your gmail password
        content  = 'There is a game ' if(game_set_num==1) else 'There are {x} games '.format(x=game_set_num)
        content += 'that {x} plays today : \n'.format(x=team)
        content += tabulate(short_selected_data_df, headers='keys', tablefmt='psql')
        content += '\n\n\n'+'detailed : '+'\n'
        content += tabulate(selected_data_df, headers='keys', tablefmt='psql')
        #Also show the statistics of the starting players of the teams
        team_list  = list(selected_data_df['TEAM'].values)
        for team in team_list:
            content += '\n\n\n {} starting players : '.format(team)+'\n'
            content += tabulate(starters_data_dict[team], headers='keys', tablefmt='psql')

        title    = 'NBA game statistics for {x}'.format(x = team)
        to_addr  = gmail_user
        cc_addr  = gmail_user+', '+'vickiehsu828@gmail.com'
        email.SendMail(gmail_user, gmail_password, content, title, to_addr, cc_addr)
        print(f'There are NBA games for {team} at {date_usa}. Email sent!')
    else:
        print(f'No NBA games for {team} at {date_usa}.')

def CheckSendMailsToINO(date, team, all_data_df, password, browser, all_data_item_href):
    get_wanted_send_data = 0
    (game_set_num, get_wanted_data, selected_data_df, short_selected_df, starters_data_dict) = CheckDateHasSpecifiedTeam(date, team, all_data_df, browser, all_data_item_href)
    if(get_wanted_data):
        (get_send_data_set_num, get_wanted_send_data, selected_send_data_df, short_selected_send_data_df) = CheckTeamLose(team, selected_data_df)

    if(get_wanted_send_data):
        gmail_user     = 'coslate@media.ee.ntu.edu.tw'
        gmail_password = password # your gmail password
        content  = 'Oops!!!!!! {x} lost the games : \n'.format(x=team) if(get_send_data_set_num > 1) else 'Oops!!!!!! {x} lost the game : \n'.format(x=team)
        content += tabulate(short_selected_send_data_df, headers='keys', tablefmt='psql')
        content += '\n\n\n'+'detailed : '+'\n'
        content += tabulate(selected_send_data_df, headers='keys', tablefmt='psql')
        #Also show the statistics of the starting players of the teams
        team_list  = list(selected_send_data_df['TEAM'].values)
        for team in team_list:
            content += '\n\n\n {} starting players : '.format(team)+'\n'
            content += tabulate(starters_data_dict[team], headers='keys', tablefmt='psql')

        title    = 'NBA game statistics for {x}'.format(x = team)
        to_addr  = gmail_user
        cc_addr  = gmail_user+', '+'vickiehsu828@gmail.com'
        email.SendMail(gmail_user, gmail_password, content, title, to_addr, cc_addr)
        print(f'There are NBA games that {team} lost at {date}. Email sent!')
    else:
        print(f'No NBA games for {team} losing at {date}.')

def GetWikiLinksContent(starting_url, cur, table):
    all_internal_links_loop = []
    skipping = 0
    try:
        ip_addr = tool_surf.GetPublicIPAddress()
        print(f'ip address = {ip_addr}')

        head = {}
        #user_agent = random.choice(USER_AGENT_LIST)
        ua = UserAgent()
        user_agent = ua.random
        head['User-Agent'] = user_agent
        print(f'user_agent = {head["User-Agent"]}')

        #Set Proxy
        proxy_index = RandomProxy(proxy_list)
        proxy_used = proxy_list[proxy_index]
        SetProxy(proxy_used['ip']+':'+proxy_used['port'])

        req = request.Request(starting_url, headers=head)
        html = urlopen(req)
    except HTTPError as err:
        print(f'Cannot access {starting_url}. {err}')
        skipping = 1
        return all_internal_links_loop, skipping
    except http.client.RemoteDisconnected as disconnected_err:
        print(f'Cannot access {starting_url}. RemoteDisconnected. {disconnected_err}')
        print(f'Randomly set new proxy, and try again.')
        if(any(((proxy_in_list['ip'] == proxy_used['ip']) and (proxy_in_list['port'] == proxy_used['port'])) for proxy_in_list in proxy_list)):
            proxy_list.remove(proxy_used)

        #randomly set new proxy
        proxy_index = RandomProxy(proxy_list)
        proxy_used = proxy_list[proxy_index]
        SetProxy(proxy_used['ip']+':'+proxy_used['port'])
        all_internal_links_loop, skipping = GetWikiLinksContent(starting_url, cur, table)
        return all_internal_links_loop, skipping
    except error.URLError as err:
        print(f'Cannot access {starting_url}. Remote end closed connection without response. {err}')
        print(f'Randomly set new proxy, and try again.')
        if(any(((proxy_in_list['ip'] == proxy_used['ip']) and (proxy_in_list['port'] == proxy_used['port'])) for proxy_in_list in proxy_list)):
            proxy_list.remove(proxy_used)

        #randomly set new proxy
        proxy_index = RandomProxy(proxy_list)
        proxy_used = proxy_list[proxy_index]
        SetProxy(proxy_used['ip']+':'+proxy_used['port'])
        all_internal_links_loop, skipping = GetWikiLinksContent(starting_url, cur, table)
        return all_internal_links_loop, skipping
    except Exception as err:
        print('Unexpected Error occurs : {x}. Cannot access {y}.'.format(x = err, y = starting_url))
        skipping = 1
        return all_internal_links_loop, skipping

    bs_obj       = BeautifulSoup(html, 'lxml')
    domain       = urlparse(starting_url).scheme+"://"+urlparse(starting_url).netloc
    title        = bs_obj.find('h1').get_text()
    content_list = bs_obj.find('div', {'id' : 'mw-content-text'}).findAll('p')
    content = ""

    for content_ele in content_list:
        if(content_ele.has_attr('class')):
            if(re.match(r'.*empty.*', content_ele.attrs['class'][-1]) is not None):
                print(f'filtered -------> content_ele = {content_ele}')
                continue
        content += content_ele.get_text().strip('\n')
    content = content.replace('\n', ' ')
    content = content.replace('\"', '\'')

    all_internal_links_loop = bs_obj.find('div', {'id' : 'bodyContent'}).findAll('a', href=re.compile('^(/wiki/)((?!:).)*$'))
    skipping = StoreWikiToMySQL(table, cur, starting_url, title, content)

    return all_internal_links_loop, skipping

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
    print(f'> SetProxy: {proxy}')
    try :
        proxy_support = request.ProxyHandler({'http':proxy,
                                              'https':proxy})
#        proxy_support = request.ProxyHandler({'https':proxy})
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
    print("> RandomProxy...")
    return random.randint(0, len(proxy_list)-1)

def GetProxyList(is_debug):
    print("> GetProxyList...")
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

def init(is_debug=0):
    print('> Initialization...')
    global request_num
    global USER_AGENT_LIST
    global proxy_list
    global proxy_used
    global proxy_index

    #Initialization of PyMySQL
    global conn
    global cur

    request_num = 0
    proxy_index = -1
    proxy_used  = {}
    proxy_list  = []
    proxy_list  = GetProxyList(is_debug)
    proxy_index = RandomProxy(proxy_list)
    proxy_used  = proxy_list[proxy_index]
    SetProxy(proxy_used['ip']+':'+proxy_used['port'])
    if(is_debug):
        pass
        #print(f"proxy_used = {proxy_used}")

#The following three lines of code will cause 'http.client.RemoteDisconnected: Remote end closed connection without response' error when using webdriver.Chrome()
#    print('--------------------------Resolve "http.client.IncompleteRead" Error--------------------------')
#    http.client.HTTPConnection._http_vsn = 10
#    http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'
