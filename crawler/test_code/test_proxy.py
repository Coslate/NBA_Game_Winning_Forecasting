#! /usr/bin/env python3.6

from urllib.error import URLError
from urllib.request import ProxyHandler, build_opener
import package_tool_surf.tool_surf as tool_surf
import package_crawler_nba.crawler_nba as crawler_nba

ip_addr = tool_surf.GetPublicIPAddress()
print('----origin----')
print(f'ip address = {ip_addr}')


#proxy = 'username:password@127.0.0.1:9743'
proxy = '186.159.3.49:30981'
'''
proxy_handler = ProxyHandler({
    'http': 'http://' + proxy,
    'https': 'https://' + proxy
})
opener = build_opener(proxy_handler)
try:
    response = opener.open('http://httpbin.org/get')
    print(response.read().decode('utf-8'))
except URLError as e:
    print(e.reason)
'''

crawler_nba.SetProxy(proxy)
ip_addr = tool_surf.GetPublicIPAddress()
print('----after----')
print(f'ip address = {ip_addr}')


