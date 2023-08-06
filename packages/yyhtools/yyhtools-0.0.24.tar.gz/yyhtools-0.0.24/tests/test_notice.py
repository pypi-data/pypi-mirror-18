#!/usr/bin/env python

import yyhtools.notice as notice
from yyhtools.track import *

def test():
    success("hello")
    fail("fail")
    logs = get_logs()
    notice.send(logs)
    notice.send(logs, style='stock')

