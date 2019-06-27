# -*- coding:utf-8 -*-

import pymysql


class DB:
    db = pymysql.Connect(host='182.61.172.229', user='root',
                         password='@xwl082933048.', database='tv',
                         charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    @staticmethod
    def query_index_news():
        sql = "select id, tv_id, tv_name, tv_img, tv_actors, update_time from t_tv order by update_time desc limit 0,12"
        cursor = DB.db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    @staticmethod
    def query_index_mv():
        sql = ""



