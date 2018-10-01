from urllib import request
from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.error import HTTPError
from urllib import error
from bs4 import BeautifulSoup


def GetPublicIPAddress():
    ip_url = 'http://ip.42.pl/raw'

    try:
        html = urlopen(ip_url)
    except HTTPError:
        print(f'Cannot access {ip_url}. HTTPError.')
        return None
    except http.client.RemoteDisconnected:
        print(f'Cannot access {ip_url}. RemoteDisconnected.')
        return None

    response = BeautifulSoup(html, 'lxml')
    ip_address = response.get_text()

    return ip_address
