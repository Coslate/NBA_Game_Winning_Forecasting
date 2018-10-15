#! /usr/bin/env python3.6

import pymysql

conn = pymysql.connect(host='localhost',
                       unix_socket='/var/run/mysqld/mysqld.sock',
                       user='root',
                       passwd='p78003425',
                       db='mysql')

cur = conn.cursor()
cur.execute('USE scraping;')
cur.execute('SELECT * FROM pages WHERE id=1;')
print('-------SELECT--------')
print(cur.fetchall())
print('----------------')
cur.execute('DESCRIBE pages;')
print('------DESCRIBE---------')
print(cur.fetchone())
print('----------------')
cur.execute('SELECT * FROM pages')
print('------SHOW pages---------')
ret_data = cur.fetchall()
print(ret_data)
print(type(ret_data))
for data in ret_data:
    print('<><><><><><><><><><><><><>')
    print(f'ret_data_ele = {data}')
    for data_ele in data:
        print(f'     data_ele = {data_ele}')
print('----------------')
cur.close()
conn.close()

