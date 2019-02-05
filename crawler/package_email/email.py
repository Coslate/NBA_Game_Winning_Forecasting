from urllib import request
from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.error import HTTPError
from urllib import error
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText


def SendMail(gmail_user, gmail_password, content, title, to_addr, cc_addr):
    msg = MIMEText(content)
    msg['Subject'] = title
    msg['From'] = gmail_user
    msg['To'] = to_addr
    msg['Cc'] = cc_addr

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.send_message(msg)
    server.quit()

    print("package_email.SendMail : Email Sent!")
