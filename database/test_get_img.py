#! /usr/bin/env python3.6

from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup

#-----------------Execution------------------#
if __name__ == '__main__':
    html = urlopen("http://www.pythonscraping.com")
    bs_obj = BeautifulSoup(html, 'lxml')
#    print(bs_obj.prettify())
    all_image_locs = bs_obj.findAll('a', {"id":"logo"})
    count = 0

    for image_loc_cand in all_image_locs:
        image_loc = image_loc_cand.find('img')['src']
        urlretrieve(image_loc, 'logo_'+str(count)+'.jpg')
        count += 1
