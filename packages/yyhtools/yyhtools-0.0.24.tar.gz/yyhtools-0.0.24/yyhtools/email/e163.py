#!/usr/bin/env python
# coding=utf-8

'''
163邮箱自己发送给自己，然后转发出去。
'''

import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

import json

config = {}

def set_config(address, pwd):
    global config
    config['address'] = address
    config['pwd'] = pwd



def sendMail(subject,message, address='', pwd=''):
    if not address:
        address = config['address']
    if not pwd:
        pwd = config['pwd']

    sender = address
    receiver = address

    smtpserver = "smtp.163.com"
    username = address
    password = pwd

    msgRoot = MIMEMultipart('related')
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)
    msgRoot['Subject'] = Header(subject, 'utf-8')
    msgAlternative.attach(MIMEText(message, 'html', 'utf-8'))

    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(username, password)

    try:
        smtp.sendmail(sender, receiver, msgRoot.as_string())
    except Exception as e:
        smtp.quit()
        raise e

if __name__ == "__main__":
    pass


