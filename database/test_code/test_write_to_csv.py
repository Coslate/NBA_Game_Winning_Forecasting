#! /usr/bin/env python3.6

import csv

if __name__ == '__main__':
    csv_file = open('./files/test.csv', 'w+', newline='')
    try:
        writer = csv.writer(csv_file)
        writer.writerow(('number', 'number + 2', 'number * 2'))
        for i in range(10):
            writer.writerow((i, i+2, i*2))
    finally:
        csv_file.close()
