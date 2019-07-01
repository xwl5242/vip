# -*- coding:utf-8 -*-

import platform
from app.config import Config
if platform.system() == 'Windows':
    from Cryptodome.Cipher import AES
elif platform.system() == 'Linux':
    from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


class AESUtil:

    @staticmethod
    def encrypt(data):
        key = str(Config.AES_KEY).encode()
        my_cipher = AES.new(key, AES.MODE_CFB, key)
        cipher_text = key + my_cipher.encrypt(data.encode())
        return b2a_hex(cipher_text[16:]).decode()

    @staticmethod
    def decrypt(data):
        key = str(Config.AES_KEY).encode()
        cipher_text = a2b_hex(data.encode())
        my_decrypt = AES.new(key, AES.MODE_CFB, key)
        return my_decrypt.decrypt(cipher_text).decode()


if __name__ == '__main__':
    au = AESUtil()
    a = au.encrypt('全心全意')
    print(a)
    print(au.decrypt('b9bf88696da7bdba1691e014'))


