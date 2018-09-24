#! /usr/bin/env python3.6

import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

if __name__ == '__main__':
    html = urlopen("https://en.wikipedia.org/wiki/Comparison_of_text_editors")
    bs_obj = BeautifulSoup(html)
    print(bs_obj.prettify())
    csv_file = open('./files/table.csv', 'w+', newline='', encoding='utf-8')
'''
    try:
        writer = csv.writer(csv_file)
        writer.writerow(('number', 'number + 2', 'number * 2'))
        for i in range(10):
            writer.writerow((i, i+2, i*2))
    finally:
        csv_file.close()
'''
