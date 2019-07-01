# -*- coding:utf-8 -*-
from app.config import Config
from app.util.aes import AESUtil


def split_strings(s, sep=','):
    s = s if s else ''
    return str(s).split(sep)


def tv_is_mv(t_type):
    t_type = t_type if t_type else 'none'
    return '1' if t_type in Config.MV else '0'


def get_list(l, index):
    return l[index] if l and len(l) > 0 else []


def get_sub_list(l, start, end):
    return l[start:end] if l and len(l) > 0 else []


def b64encode(s):
    return AESUtil.encrypt(s)


def b64_str_decode(b):
    return AESUtil.decrypt(b)

