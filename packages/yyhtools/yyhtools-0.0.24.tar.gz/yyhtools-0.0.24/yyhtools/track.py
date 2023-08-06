#!/usr/bin/env python

from collections import namedtuple
import datetime

__all__ = ['success', 'fail', 'reset', 'get_logs', 'info', 'error']

TrackLog = namedtuple('TrackLog', ['dt', 'level', 'text'])

_logs = []


def success(s):
    _logs.append(TrackLog(dt=datetime.datetime.now(), level=0, text=s))

info = success

def fail(s):
    _logs.append(TrackLog(dt=datetime.datetime.now(), level=1, text=s))

error = fail

def reset():
    global _logs
    _logs = []

def get_logs():
    return _logs

def show():
    for i in _logs:
        print i.text

if __name__ == "__main__":
    reset()
    success('ni')
    fail('nnn')
    print get_logs()
    reset()
    print get_logs()

