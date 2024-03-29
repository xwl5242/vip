# -*- coding:utf-8 -*-
import pymysql
from app.config import Config
from DBUtils.PooledDB import PooledDB

# database pool
POOL = PooledDB(pymysql, 5, host=Config.MS_HOST, user=Config.MS_USER,
                passwd=Config.MS_PWD, db=Config.MS_DATABASE, port=Config.MS_PORT,
                charset=Config.MS_CHARSET, cursorclass=pymysql.cursors.DictCursor)


# database decorator, auto connect and auto close db, cursor
def app_db(func):
    def wrapper(*args, **kwargs):
        conn = POOL.connection()
        cursor = conn.cursor()
        try:
            return func(cursor, *args, **kwargs)
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(repr(e))
            conn.rollback()
        finally:
            conn.commit()
            cursor.close()
            conn.close()
    return wrapper


# database operator base
class Base:

    @staticmethod
    @app_db
    def query_page(cursor, select_sql, args):
        """
        query list for page, fixed page size 30
        :param cursor: cursor
        :param select_sql: select sql
        :return:
        """
        select_count_sql = "select count(1) total "+select_sql[select_sql.index('from'):]
        select_sql = select_sql + ' limit %s,30'
        cursor.execute(select_count_sql, args[:-1])
        total = cursor.fetchone()['total']
        cursor.execute(select_sql, args)
        items = cursor.fetchall()
        return items, total

    @staticmethod
    @app_db
    def query_list(cursor, select_sql, args):
        """
        query list
        :param cursor: cursor
        :param select_sql: select sql
        :return:
        """
        cursor.execute(select_sql, args)
        return cursor.fetchall()

    @staticmethod
    @app_db
    def get(cursor, get_sql, args):
        """
        get one
        :param cursor: cursor
        :param get_sql: get sql
        :param args:
        :return:
        """
        cursor.execute(get_sql, args)
        return cursor.fetchone()

    @staticmethod
    @app_db
    def insert(cursor, sql, args):
        print(args)
        return cursor.execute(sql, args)


