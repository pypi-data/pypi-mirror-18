# coding:utf8

'''
    这个模块包含设置告警的代码
'''
import os
import sys
import random
import string
import logging
import logging.handlers
from flask import request, current_app

reload(sys)
sys.setdefaultencoding('utf8')


def get_ip_address(ifname='eth1'):
    import socket
    import fcntl
    import struct
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915, # SIOCGIFADDR  
            struct.pack('256s', ifname[:15])
        )[20:24])
    except:
        return ''

ip = get_ip_address()

try:
    #server = os.environ["HOSTNAME"]
    import socket
    server = socket.gethostname()
except:
    server = "unkown"

class MySMTPHandler(logging.handlers.SMTPHandler):

    def emit(self, record):
        try:
            #r = random.randint(0,100)
            #if r <= 30:
            #    return
            import smtplib
            try:
                from email.utils import formatdate
            except ImportError:
                formatdate = self.date_time
            port = self.mailport
            if not port:
                port = smtplib.SMTP_PORT
            smtp = smtplib.SMTP(self.mailhost, port)
            real_ip = request.headers.get("X-Real-Ip", "")
            ref = request.headers.get("Referer", "")
            header = "From: %s(%s)\r\n\r\nX-Real-Ip:%s\r\nReferer:%s\r\n" % (server, ip, real_ip, ref)
            msg = header + "%s\r\n%s\r\n%s\r\n" % (ip, request.url, request.values.to_dict()) + self.format(record)
            msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\n\r\n%s" % (
                            self.fromaddr,
                            string.join(self.toaddrs, ","),
                            "%s (%s)" % (self.getSubject(record), server),
                            formatdate(), msg)
            if self.username:
                smtp.login(self.username, self.password)
            smtp.sendmail(self.fromaddr, self.toaddrs, msg)
            smtp.quit()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


def enable_logging(app):
    config = app.config['LOGGING']
    config_mail = config.get('SMTP')
    if config_mail:  #如果存在smtp配置
        app.logger.info('Add SMTP Logging Handler')
        mail_handler = MySMTPHandler(
            config_mail['HOST'],  #smtp 服务器地址
            config_mail['USER'],  #smtp 发件人
            config_mail['TOADDRS'],  #smtp 收件人
            config_mail['SUBJECT'],  #smtp 主题
            (config_mail['USER'], config_mail['PASSWORD']))  #smtp账号密码
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
    else:
        app.logger.info('No SMTP Config Found')

    config_file = config.get('FILE')
    if config_file:  #如果存在文件配置
        app.logger.info('Add File Logging Handler')
        file_handler = logging.handlers.RotatingFileHandler(
            config_file['PATH'],  #文件路径
            #但个文件大小 默认10M 
            maxBytes=config_file.setdefault('MAX_BYTES', 1024 * 1024 * 10),
            #文件备份>数量 默认5个
            backupCount=config_file.setdefault('BACKUP_COUNT', 5),
        )
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('[%(asctime)s | %(levelname)s | %(funcName)s] %(message)s')
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)
    else:
        app.logger.info('No FILE Config Found')

