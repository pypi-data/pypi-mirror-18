#!/usr/bin/env python
#-*-coding:utf-8-*-

import yyhtools
import yyhtools.email.e163 as em163
import yyhtools.track as ytrack
import yyhtools.html.template as template

__all__ = ['send']

def send(logs, style='', title=''):
    loader = template.Loader(yyhtools.static_dir)
    if style == 'stock':
        t = loader.load("stock.html")
    elif style == 'error':
        t = loader.load("error.html")
    else:
        t = loader.load("base.html")
    html = t.generate(logs=logs)
    if not title:
        title = "数据已经处理完成"
    em163.sendMail(title, html,
                   yyhtools.email_address,
                   yyhtools.email_pwd)

