# -*- coding:utf-8 -*-
import os
import configparser


class Config:
    # 从config.ini文件中读取配置信息
    cfg = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.ini')
    conf = configparser.ConfigParser()
    conf.read(cfg, encoding='utf-8')

    # AES_KEY AES加密key
    AES_KEY = conf.get('AES_KEY', 'aes_key')

    # TV_TYPE_ITEM tv视频大类和小类
    TV = []
    TV_KV = {}
    for ty in conf.get('TV_TYPE_ITEM', 'tv_type').split(','):
        ty = str(ty).split(':')
        TV.append((ty[0], ty[1]))
        kvs = conf.get('TV_TYPE_ITEM', f'{ty[0]}_type_kv').split(',')
        TV_KV[ty[0]] = [(kv.split(':')[0], kv.split(':')[1]) for kv in kvs]

    # 每个视频大类所包含的小类
    MV = [mv for mv in conf.get('TV_TYPE_ITEM', 'mv').split(',')]
    DSJ = [dsj for dsj in conf.get('TV_TYPE_ITEM', 'dsj').split(',')]
    ZY = [zy for zy in conf.get('TV_TYPE_ITEM', 'zy').split(',')]
    DM = [dm for dm in conf.get('TV_TYPE_ITEM', 'dm').split(',')]
    TV_KV_LIST = {'mv': MV, 'dsj': DSJ, 'zy': ZY, 'dm': DM}

    # mongodb配置相关
    MD_HOST = str(conf.get('MONGODB', 'host'))
    MD_PORT = int(conf.get('MONGODB', 'port'))
    MD_DATABASE = str(conf.get('MONGODB', 'database'))
    MD_USER = str(conf.get('MONGODB', 'user'))
    MD_PWD = str(conf.get('MONGODB', 'pwd'))

    # mysql配置相关
    MS_HOST = str(conf.get('MYSQL_DB', 'host'))
    MS_USER = str(conf.get('MYSQL_DB', 'user'))
    MS_PWD = str(conf.get('MYSQL_DB', 'pwd'))
    MS_DATABASE = str(conf.get('MYSQL_DB', 'database'))
    MS_PORT = int(conf.get('MYSQL_DB', 'port'))
    MS_CHARSET = str(conf.get('MYSQL_DB', 'charset'))

    # img server
    IMG_WEB = conf.get('IMG_SERVER', 'url')

    # 年代
    YEARS = [y for y in conf.get('YEARS', 'years').split(',')]

    # webservice secret
    WEBSERVICE_SERET = conf.get('WEBSERVICE', 'secret')

    TV_SOURCE_MAIN, TV_SOURCE_3PART = 'main', '3part'

    _3PART_API_URL = str(conf.get('3PART_API', 'url'))

    RUN_PLATFORM = str(conf.get('RUN', 'platform'))


if __name__ == '__main__':
    print(Config.TV_VK)

