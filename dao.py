# -*- coding:utf-8 -*-
import pymysql
import configparser


class Config:
    cf = configparser.ConfigParser()
    cf.read('config.ini', encoding='utf-8')
    MV = [mv for mv in cf.get('tv_type', 'mv').split(',')]
    DM = [dm for dm in cf.get('tv_type', 'dm').split(',')]
    ZY = [zy for zy in cf.get('tv_type', 'zy').split(',')]
    DSJ = [dsj for dsj in cf.get('tv_type', 'dsj').split(',')]


class DB:
    db = pymysql.Connect(host='182.61.172.229', user='root',
                         password='@xwl082933048.', database='tv',
                         charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    @staticmethod
    def query_index_news():
        sql = "select id, tv_id, tv_name, tv_img, tv_actors, tv_type, update_time " \
              "from t_tv order by update_time desc limit 0,12"
        cursor = DB.db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    @staticmethod
    def query_index_mvs(config_tv_type):
        where_str = "','".join(config_tv_type)
        sql = f"select id, tv_id, tv_name, tv_img, tv_actors, tv_type, tv_area, update_time " \
            f"from t_tv where tv_type in('{where_str}') order by update_time desc limit 8"
        cursor = DB.db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()




if __name__ == '__main__':
    print(Config.MV)


