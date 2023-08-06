#coding:utf-8
import bisect
import socket,struct
import json
from SimpleXMLRPCServer import SimpleXMLRPCServer
import SocketServer
from os.path import join, dirname

class ipCool(object):
    def __init__(self, path = None):
        if not path:
            path = join(dirname(__file__), 'ipcool')
        self.ipmap = {}
        self.iplist = []
        self.ipfile = open(path, 'r')
        self.readIps()
        self.ipfile.close()
        _tmp = json.load(open(join(dirname(__file__), 'provinces.json')))
        d = {}
        for row in _tmp['provinces']:
            _x = {}
            for _c in row['citys']:
                _x.update(_c)
            id = str(row['id'])
            d[id] = {
                'name': row['name'],
                'citys': _x
            }
        self.locations = d
        self.isps = {
            '1' : u'电信',
            '2' : u'联通',
            '3' : u'教育',
            '4' : u'移动',
            '5' : u'铁通',
            '6' : u'网通',
            '0' : u'',
         }

        
    def readIps(self):
        lines = self.ipfile.read().split('\n')
        for line in lines:
            if line == '' : continue
            nums = line.split('\t')
            key = int(nums[0].strip())
            self.iplist.append(key)
            self.ipmap[key] = nums[1:]
        self.iplist.sort()


    def targetIp(self, ipnum):
        ipnum = int(ipnum)
        pos = bisect.bisect_right(self.iplist, ipnum) - 1
        key = self.iplist[pos]
        if int(self.ipmap[key][0]) < ipnum:
            return ['0', '0', '0']
        return self.ipmap[key][1:] 
    
    def ipaton(self, ipstr):
        return struct.unpack('!I', socket.inet_aton(ipstr))[0]

_IC = ipCool()
def parse_ip(ip, detail = True):
    try:
        _tmp = _IC.ipaton(ip)
    except:
        return {'pro' : "", 'city' : "", 'isp' : ""}
    pro, city, isp = _IC.targetIp(_tmp)
    ret = {'pro' : pro, 'city' : city, 'isp' : isp}
    if detail:
        info = _IC.locations.get(pro, {})
        ret['pro_d'] = info.get('name', '')
        ret['city_d'] = info.get('citys', {}).get(city, '')
        ret['isp_d'] = _IC.isps.get(isp, '')
    return ret

def list_locations():
    return _IC.locations 

def list_isps():
    return _IC.isps

class ThreadingRPCServer(SocketServer.ThreadingMixIn, SimpleXMLRPCServer):
    pass

if __name__ == '__main__':
    print parse_ip('113.66.189.243')

