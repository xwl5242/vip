# -*- coding:utf-8 -*-
import pymysql
from app.config import Config
from DBUtils.PooledDB import PooledDB

POOL = PooledDB(pymysql, 5, host=Config.MS_HOST, user=Config.MS_USER,
                passwd=Config.MS_PASSWD, db=Config.MS_DB, port=int(Config.MS_PORT),
                charset=Config.MS_CHARSET, cursorclass=pymysql.cursors.DictCursor)


def app_db(func):
    def wrapper(*args, **kwargs):
        try:
            conn = POOL.connection()
            cursor = conn.cursor()
            return func(cursor, *args, **kwargs)
        finally:
            cursor.close()
            conn.close()
    return wrapper


class Base:

    @staticmethod
    @app_db
    def query_page(cursor, select_sql, page_no):
        page_no = 1 if page_no or page_no == '0' or page_no == 0 else int(page_no)
        select_count_sql = "select count(1) total "+select_sql[select_sql.index('from'):]
        select_sql = select_sql + f' limit {(page_no-1)*30},{page_no*30}'
        cursor.execute(select_count_sql)
        total = cursor.fetchone()['total']
        cursor.execute(select_sql)
        items = cursor.fetchall()
        return items, total

    @staticmethod
    @app_db
    def query_list(cursor, select_sql):
        cursor.execute(select_sql)
        return cursor.fetchall()

    @staticmethod
    @app_db
    def get(cursor, get_sql):
        cursor.execute(get_sql)
        return cursor.fetchone()
