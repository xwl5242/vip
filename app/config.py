# -*- coding:utf-8 -*-
import os
import configparser


class Config:
    cfg = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.ini')
    conf = configparser.ConfigParser()
    conf.read(cfg, encoding='utf-8')
    # AES_KEY
    AES_KEY = conf.get('AES_KEY', 'aes_key')
    # TV_TYPE_ITEM
    TV_KV = {}
    for ty in conf.get('TV_TYPE_ITEM', 'tv_type').split(','):
        kvs = conf.get('TV_TYPE_ITEM', f'{ty}_type_kv').split(',')
        TV_KV[ty] = [(kv.split(':')[0], kv.split(':')[1]) for kv in kvs]
    # EVERY TV ITEM
    MV = [mv for mv in conf.get('TV_TYPE_ITEM', 'mv').split(',')]
    DSJ = [dsj for dsj in conf.get('TV_TYPE_ITEM', 'dsj').split(',')]
    ZY = [zy for zy in conf.get('TV_TYPE_ITEM', 'zy').split(',')]
    DM = [dm for dm in conf.get('TV_TYPE_ITEM', 'dm').split(',')]
    TV_KV_LIST = {'mv': MV, 'dsj': DSJ, 'zy': ZY, 'dm': DM}
    # MYSQL_DB
    MS_HOST = conf.get('MYSQL_DB', 'host')
    MS_USER = conf.get('MYSQL_DB', 'user')
    MS_PASSWD = conf.get('MYSQL_DB', 'passwd')
    MS_DB = conf.get('MYSQL_DB', 'db')
    MS_PORT = conf.get('MYSQL_DB', 'port')
    MS_CHARSET = conf.get('MYSQL_DB', 'charset')
    # img server
    IMG_WEB = 'http://img.yoviptv.com/'
    # 年代
    YEARS = [y for y in conf.get('YEARS', 'years').split(',')]


if __name__ == '__main__':
    print(Config.TV_VK)

