#!/usr/bin/env python

from yyhtools.track import *

def test():
    reset()
    success('ni')
    fail('nnn')
    logs = get_logs()
    assert len(logs) == 2
    reset()
    logs = get_logs()
    assert len(logs) == 0
