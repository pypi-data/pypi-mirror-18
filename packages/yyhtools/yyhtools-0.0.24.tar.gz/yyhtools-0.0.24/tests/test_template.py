#!/usr/bin/env python

import yyhtools
import yyhtools.html.template as template
from yyhtools.track import *


def test():
    reset()
    success("success")
    fail("fail")
    loader = template.Loader(yyhtools.static_dir)
    print loader.load("stock.html").generate(logs=get_logs())

