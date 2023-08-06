#coding=utf-8

from functools import wraps, partial
from flask import abort, current_app, request, g


def get_param(key, default=None, type=None, required=False, mapping_key=None, \
                    minvalue=None, maxvalue=None, choices=None, autominvalue=False, automaxvalue=False):
    """获取request参数
    :param key: 参数名
    :param default: 参数默认值
    :param type: 参数类型
    :param mapping: request.XXXX (args, form, headers, values)
    :param required: 参数是否必须
    :param minvalue 限制参数最小值
    :param maxvalue 限制参数最大值
    :param choices 限制参数值选择
    :param autominvalue 值小于minvalue则调整为minvalue
    :param automaxvalue 值大于maxvalue则调整为maxvalue
    """
    mapping = getattr(request, mapping_key, {}) 
    if required is True and key not in mapping:
        print "missing param %s" % key 
        abort(400, "missing param %s" % key) 
    value = mapping.get(key, default)
    if type is not None:
        try:
            value = type(value)
        except ValueError, TypeError:
            print "invild param type %s, %s needed" % (key, type) 
            abort(400, "invild param type %s, %s needed" % (key, type)) 
        except Exception, e:
            print e
            abort(500)
    if minvalue is not None and value < minvalue:
        if autominvalue is True:
            value = minvalue
        else:
            abort(400, "param %s less than minvalue %s" % (key, minvalue))
    if maxvalue is not None and value > maxvalue:
        if automaxvalue is True:
            value = maxvalue
        else:
            abort(400, "param %s bigger than maxvalue %s" % (key, maxvalue))
    if choices is not None and value not in choices:
        abort(400, "prams %s is not available" % key)
    return value

request_args = partial(get_param, mapping_key="args")
request_form = partial(get_param, mapping_key="form")
request_values = partial(get_param, mapping_key="values")
request_headers = partial(get_param, mapping_key="headers")


def mysql_read_slave(func):
    @wraps(func)
    def decorate(*args, **kwargs):
        g.__bind = 'slave'
        return func(*args, **kwargs)
    return decorate
