#!/usr/bin/env python

import os

project_dir = os.path.abspath(os.path.dirname(__file__))
static_dir = os.path.join(project_dir, 'static')

email_address = ''
email_pwd = ''

try:
    from config import *
except:
    pass


import track
from track import *
import notice
from notice import *
