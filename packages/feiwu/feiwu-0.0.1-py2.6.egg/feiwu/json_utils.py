#coding:utf8

'''
    JSON工具
'''
import ujson
from flask import escape

def loads(d):
    return ujson.loads(d)

def dumps(d, html_safe=False):
    if html_safe:
        d = html_escape(d)
    return ujson.dumps(d)

def html_escape(d):
    if type(d) == dict:
        for k in d:
            d[k] = html_escape(d[k])
    elif type(d) in [list, tuple]:
        for i in xrange(len(d)):
            d[i] = html_escape(d[i])
    elif type(d) in [int, float]:
        pass
    else:
        d = str(escape(d))
    return d


def json_success(**kwargs):
    kwargs['code'] = 0
    return kwargs
