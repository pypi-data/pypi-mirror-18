#coding:utf8

'''
    额外工具
'''
import struct
import socket
import hashlib

from flask import request, current_app, request, session
from qiniu import Auth, put_data 


def Ip2Int(ip):
    return struct.unpack("!I",socket.inet_aton(ip))[0]

def Int2Ip(i):
    return socket.inet_ntoa(struct.pack("!I",i))

def get_ip():
    if 'X-Forwarded-For' in request.headers:
        return request.headers['X-Forwarded-For'].split(',')[0]

    return request.headers.get('X-Real-Ip') or request.remote_addr

def upload_img(filename, data, bucket_name, config=None):
    if not config:
        config = current_app.config

    cfg = config['QINIU_SETTINGS']
    access_key = cfg['access_key']
    secret_key = cfg['secret_key']
    
    q = Auth(access_key, secret_key)
    token = q.upload_token(bucket_name, filename)
    ret, info = put_data(token, filename, data)
    
    assert ret['key'] == filename
    host = cfg['buckets'][bucket_name]
    return 'http://%s/%s'%(host, filename)

def hash_pwd(pwd):
    return hashlib.sha1(pwd).hexdigest()
