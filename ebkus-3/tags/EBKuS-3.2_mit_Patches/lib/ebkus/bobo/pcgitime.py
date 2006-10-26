#!/usr/local/bin/python
# coding: latin-1
# pcgitime.py - pcgi test script - JeffBauer@bigfoot.com
from time import asctime, localtime, time

beginTime = "<html><pre>time started: %s" % \
            asctime(localtime(time()))

def getTime(arg=None):
    """current local time"""
    import log
    log.log(': getTime called')
    return "%s\ncurrent time: %s" % \
        (beginTime, asctime(localtime(time())))
