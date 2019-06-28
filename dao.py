# -*- coding:utf-8 -*-
import pymysql
import configparser


class Config:
    """
    全局配置类
    """
    # 读取全局配置文件config.ini
    cf = configparser.ConfigParser()
    cf.read('config.ini', encoding='utf-8')
    # 视频类型section
    MV = [mv for mv in cf.get('tv_type', 'mv').split(',')]
    DM = [dm for dm in cf.get('tv_type', 'dm').split(',')]
    ZY = [zy for zy in cf.get('tv_type', 'zy').split(',')]
    DSJ = [dsj for dsj in cf.get('tv_type', 'dsj').split(',')]
    MV_TYPE = [(mv.split(':')[0], mv.split(':')[1]) for mv in cf.get('tv_type', 'mv_type').split(',')]
    DM_TYPE = [(dm.split(':')[0], dm.split(':')[1]) for dm in cf.get('tv_type', 'dm_type').split(',')]
    ZY_TYPE = [(zy.split(':')[0], zy.split(':')[1]) for zy in cf.get('tv_type', 'zy_type').split(',')]
    DSJ_TYPE = [(dsj.split(':')[0], dsj.split(':')[1]) for dsj in cf.get('tv_type', 'dsj_type').split(',')]
    TYPES = {'mv': MV_TYPE, 'dm': DM_TYPE, 'zy': ZY_TYPE, 'dsj': DSJ_TYPE}


class DB:
    """
    数据库操作类
    """
    db = pymysql.Connect(host='182.61.172.229', user='root',
                         password='@xwl082933048.', database='tv',
                         charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    @staticmethod
    def query_index_today_total_update():
        """
        首页今日更新和总视频数量
        :return:
        """
        today_sql = "select count(1) total from t_tv where date_format(update_time,'%Y-%m-%d')=date_format(now(),'%Y-%m-%d') "
        total_sql = "select count(1) total from t_tv"
        cursor = DB.db.cursor()
        cursor.execute(today_sql)
        today = cursor.fetchone()
        cursor.execute(total_sql)
        total = cursor.fetchone()
        today = today['total'] if today and today['total'] else 0
        total = total['total'] if total and total['total'] else 0
        return today, total

    @staticmethod
    def query_index_news():
        """
        首页最新视频
        :return:
        """
        sql = "select id, tv_id, tv_name, tv_img, tv_actors, tv_type, update_time " \
              "from t_tv order by update_time desc limit 0,12"
        cursor = DB.db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    @staticmethod
    def query_index_mvs(config_tv_type):
        """
        首页各种类视频
        :param config_tv_type:
        :return:
        """
        where_str = "','".join(config_tv_type)
        sql = f"select id, tv_id, tv_name, tv_img, tv_actors, tv_type, tv_area, update_time " \
            f"from t_tv where tv_type in('{where_str}') order by update_time desc limit 8"
        cursor = DB.db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    @staticmethod
    def query_tv_detail(tv_id):
        d_sql = f"select tv.tv_id, tv_img, tv_name, tv_actors, tv_director, tv_type, tv_area, tv_lang, " \
                f"tv_year, tv_intro, tv_remark, update_time from t_tv tv where tv.tv_id='{tv_id}'"
        u_sql = f"select tv_url from t_tv_urls where tv_id='{tv_id}'"
        cursor = DB.db.cursor()
        cursor.execute(d_sql)
        detail = cursor.fetchone()
        if detail:
            cursor.execute(u_sql)
            urls = cursor.fetchall()
            urls = [url['tv_url'] for url in urls]
            detail['urls'] = urls
        return detail

    @staticmethod
    def query_friend_urls():
        """
        首页友情链接
        :return:
        """
        sql = "select f_title,f_url from t_f_u where del_flag='0'"
        cursor = DB.db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()


if __name__ == '__main__':
    print(Config.MV)


