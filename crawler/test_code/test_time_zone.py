#! /usr/bin/env python3.6
import pytz
import time
import datetime

print(pytz.country_timezones('us'))
tz = pytz.timezone('America/New_York')
a = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
print(f'a = {a}')
current_time = datetime.datetime.now(tz)
current_date = str(current_time.month).zfill(2)+'/'+str(current_time.day).zfill(2)+'/'+str(current_time.year)
print(f'current_date = {current_date}')
