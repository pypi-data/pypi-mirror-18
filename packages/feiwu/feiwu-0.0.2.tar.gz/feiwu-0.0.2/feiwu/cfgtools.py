#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author = "wudb@pv.cc"
__doc__ = \
"""**********************************************************
*************************************************************
**                                                         **
**        Copyright (C) pv.cc 2016 AllRights Reserved      **
**                                                         **
**    HISTORY:                                             **
**          V1.00       2016-11-09       Creation.         **
**                                                         **
*************************************************************

**********************************************************"""
import os, sys
import traceback
import ConfigParser

from flask import current_app

def get_key(identify, section, key):
    """
    @identify: 配置文件名称(不带key文件后缀), 例如 fund51.key 则传 fund51
    @section: 配置文件的配置项名称，例如fund51.key内的[fund51_prod]
    @key: 配置项的key名称，该函数将返回该key对应的value值
    为了避免频繁的磁盘io读取配置文件，将采用redis缓存缓存该key3600秒的时间
    """
    config_file = "keys/%s.key" % identify
    redis_key = 'keys-' + identify + section + key

    value = current_app.redis.get(redis_key)
    if value:
        return value

    cp = ConfigParser.ConfigParser()
    try:
        cp.read(config_file)
        value = cp.read(section, key)
    except Exception, e:
        raise traceback.format_exc()

    current_app.redis.set(redis_key, value)
    current_app.redis.expire(redis_key, 3600)

    return value
