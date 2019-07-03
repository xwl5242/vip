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
    # MYSQL_DB
    _run_mode = conf.get('RUN_MODE', 'mode')
    __db_version = 'PRO' if _run_mode == 'pro' else 'TEST'
    MS_HOST = conf.get(f'MYSQL_DB_{__db_version}', 'host')
    MS_USER = conf.get(f'MYSQL_DB_{__db_version}', 'user')
    MS_PASSWD = conf.get(f'MYSQL_DB_{__db_version}', 'passwd')
    MS_DB = conf.get(f'MYSQL_DB_{__db_version}', 'db')
    MS_PORT = conf.get(f'MYSQL_DB_{__db_version}', 'port')
    MS_CHARSET = conf.get(f'MYSQL_DB_{__db_version}', 'charset')
    # img server
    IMG_WEB = conf.get('IMG_SERVER', 'url')
    # 年代
    YEARS = [y for y in conf.get('YEARS', 'years').split(',')]


if __name__ == '__main__':
    print(Config.TV_VK)

