# -*- coding:utf-8 -*-
from app.util.aes import AESUtil


def split_strings(s, sep=','):
    """
    split strings
    :param s:
    :param sep:
    :return:
    """
    s = s if s else ''
    return str(s).split(sep)


def get_list(l, index):
    """
    get list an specified element
    :param l:
    :param index:
    :return:
    """
    return l[index] if l and len(l) > 0 else []


def get_sub_list(l, start, end):
    """
    get sub list
    :param l:
    :param start:
    :param end:
    :return:
    """
    return l[start:end] if l and len(l) > 0 else []


def b64encode(s):
    """
    AES encrypt
    :param s:
    :return:
    """
    return AESUtil.encrypt(s)


def b64_str_decode(b):
    """
    AES decrypt
    :param b:
    :return:
    """
    return AESUtil.decrypt(b)

