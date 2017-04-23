#!/usr/bin/env python
# coding:utf-8

import json
import logging
import os
import random
import sys
import time

from Login import Login


def log():
    logging.basicConfig(filename='QQRobot.log',
                        level=logging.DEBUG,
                        format='[%(levelname)s] [%(asctime)s]: %(message)s',
                        datefmt='%d/%b/%Y %H:%M:%S')
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(levelname)-6s[%(asctime)s]]: %(message)s')
    handler.setFormatter(formatter)
    logging.getLogger('').addHandler(handler)
    return logging

LOG = log()


def hand_msg(msg):
    if 'error' in msg:
        return 'None New Message'
    msg_dict = json.loads(msg)
    msg_content = msg_dict['result'][0]['value']['content'][-1]
    from_uin = msg_dict['result'][0]['value']['from_uin']
    msg_type = msg_dict['result'][0]['poll_type']
    return [msg_content, from_uin, msg_type]


SEND_MSG = ("[自动回复]这里是机器人~")

def main():
    bot = Login()
    LOG.info('请扫描二维码.')
    print(bot.get_QRcode())
    os.remove("QRcode.png")
    IS_LOGIN = False
    while not IS_LOGIN:
        time.sleep(2)
        res = bot.is_login().split(',')[-2]
        LOG.info(res)
        IS_LOGIN = True if '登录成功' in res else False
    LOG.info('获取ptwebqq...')
    bot.get_ptwebqq()
    LOG.info('获取vfwebqq...')
    bot.get_vfwebqq()
    LOG.info('获取psessionid...')
    bot.get_psessionid()
    LOG.info('等待消息...')
    STOP = False
    IS_OPEN = True
    while not STOP:
        time.sleep(1)
        try:
            msg = bot.poll()
            msg_content, from_uin, msg_type = hand_msg(msg[0])
            LOG.info('{0} 发来一条消息: {1}'.format(from_uin, msg_content.encode('utf-8')))
            if (IS_OPEN is True) and ('STOP' not in msg_content):
                msg = "{0}[{1}]".format(SEND_MSG, random.randint(0, 10))
                send_status = bot.send_msg(msg, from_uin, msg_type)
                LOG.info('回复 {0}: {1}'.format(from_uin, send_status))
            elif 'STOP' in msg_content:
                LOG.info('CLOSE...')
                bot.send_msg('CLOSED', from_uin, msg_type)
                IS_OPEN = False
            elif 'START' in msg_content:
                LOG.info('STARTED')
                bot.send_msg('OPENED', from_uin, msg_type)
                IS_OPEN = True

        except KeyboardInterrupt:
            LOG.info('See You...')
            STOP = True
        except:
            LOG.error(sys.exc_info())

if __name__ == '__main__':
    main()
