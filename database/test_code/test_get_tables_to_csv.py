#! /usr/bin/env python3.6

import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

if __name__ == '__main__':
    html = urlopen("https://en.wikipedia.org/wiki/Comparison_of_text_editors")
    bs_obj = BeautifulSoup(html, 'lxml')

    #Get the first table of the page
    table = bs_obj.findAll('table', {'class':'wikitable'})[0]
    rows = table.findAll('tr')

    #Open the csv_file
    csv_file = open('./files/table_editors.csv', 'w+', newline='', encoding='utf-8')
    writer = csv.writer(csv_file)

    try:
        for row in rows:
            csv_row = []
            for cell in row.findAll(['td', 'th']):
                csv_row.append(cell.get_text())
            writer.writerow(csv_row)
    finally:
        csv_file.close()
