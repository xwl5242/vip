# -*- coding:utf-8 -*-
import json
import pymysql
from DBUtils.PooledDB import PooledDB


class Config:
    """
    全局配置类
    """
    JSON_DICT = {}
    MV, DM, ZY, DSJ = 'mv', 'dm', 'zy', 'dsj'

    with open('config.json', 'r', encoding='utf-8') as f:
        JSON_DICT = json.loads(f.read())
    TV_TYPE_KV_DICT = JSON_DICT['tv_types']
    THEME_STYLES = list(JSON_DICT['theme_styles'])

    POOL = PooledDB(pymysql, 5, host='182.61.172.229', user='root', passwd='@xwl082933048.',
                    db='tv', port=3306, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    @classmethod
    def item_value_list(cls, t):
        return [dict(tt).get('value') for tt in dict(cls.TV_TYPE_KV_DICT).get(t)]

    @classmethod
    def item_list(cls, t):
        return [(dict(tt).get('key'), dict(tt).get('value')) for tt in dict(cls.TV_TYPE_KV_DICT).get(t)]


def app_db(func):
    def wrapper(*args, **kwargs):
        try:
            conn = Config.POOL.connection()
            cursor = conn.cursor()
            return func(cursor, *args, **kwargs)
        finally:
            cursor.close()
            conn.close()
    return wrapper


class DB:

    @staticmethod
    @app_db
    def query_today_total_update(cursor, tv_type):
        """
        首页今日更新和总视频数量
        :param cursor: 数据库
        :param tv_type: None:所有，not None:当前类型的影片更新情况
        :return:
        """
        tv_type = Config.item_value_list(tv_type) if tv_type else None
        types = "','".join(tv_type) if tv_type else None
        where_str = f" and  tv_type in ('{types}')" if tv_type else ''
        today_sql = f"select count(1) total from t_tv where 1=1 {where_str} and " \
                    f"date_format(update_time,'%Y-%m-%d')=date_format(now(),'%Y-%m-%d') "
        total_sql = f"select count(1) total from t_tv where 1=1 {where_str}"
        cursor.execute(today_sql)
        today = cursor.fetchone()
        cursor.execute(total_sql)
        total = cursor.fetchone()
        today = today['total'] if today and today['total'] else 0
        total = total['total'] if total and total['total'] else 0
        return today, total

    @staticmethod
    @app_db
    def query_index_tops(cursor, tv_type):
        result = []
        top_sql = f"select tv_name,tv_top from t_tv_top where tv_type='{tv_type}'"
        cursor.execute(top_sql)
        tops = cursor.fetchall()
        if tops and len(tops) > 0:
            for t in tops:
                sql = "select id, tv_id, tv_name, tv_img, tv_actors, tv_type, tv_area, update_time " \
                      "from t_tv where tv_name like '%%%s%%' order by update_time desc" % t['tv_name']
                cursor.execute(sql)
                tvs = cursor.fetchall()
                if tvs and len(tvs) > 0:
                    result.append({"tv_vo": tvs[0], "tv_top": int(t['tv_top'])})
        return result

    @staticmethod
    @app_db
    def query_index_news(cursor):
        """
        首页最新视频
        :return:
        """
        sql = "select id, tv_id, tv_name, tv_img, tv_actors, tv_type, update_time " \
              "from t_tv order by update_time desc limit 0,12"
        cursor.execute(sql)
        return cursor.fetchall()

    @staticmethod
    @app_db
    def query_index_mvs(cursor, tv_type):
        """
        首页各种类视频
        :param cursor:
        :param tv_type:
        :return:
        """
        where_str = "','".join(Config.item_value_list(tv_type))
        sql = f"select id, tv_id, tv_name, tv_img, tv_actors, tv_type, tv_area, update_time " \
            f"from t_tv where tv_type in('{where_str}') order by update_time desc limit 8"
        cursor.execute(sql)
        return cursor.fetchall()

    @staticmethod
    @app_db
    def query_tv_like_hot(cursor, tv_type_item):
        """
        相关热播，就是同小类型的视频的最新更新的前20个中随机抽取6个
        :param cursor:
        :param tv_type_item: 视频的小类
        :return:
        """
        sql = f"select tv_id,tv_img,tv_name,tv_actors,tv_area,tv_year,update_time " \
            f"from t_tv where tv_type = '{tv_type_item}' order by update_time desc limit 20"
        cursor.execute(sql)
        return cursor.fetchall()

    @staticmethod
    @app_db
    def query_tv_detail(cursor, tv_id):
        """
        查询tv详情
        :param cursor:
        :param tv_id: 视频的id
        :return:
        """
        d_sql = f"select tv.tv_id, tv_img, tv_name, tv_actors, tv_director, tv_type, tv_area, tv_lang, " \
                f"tv_year, tv_intro, tv_remark, update_time from t_tv tv where tv.tv_id='{tv_id}'"
        u_sql = f"select tv_url from t_tv_urls where tv_id='{tv_id}'"
        cursor.execute(d_sql)
        detail = cursor.fetchone()
        if detail:
            cursor.execute(u_sql)
            urls = cursor.fetchall()
            urls = [url['tv_url'] for url in urls]
            detail['urls'] = urls
        return detail

    @staticmethod
    @app_db
    def query_tv_more_by_name(cursor, tv_name):
        sql = "select tv_id,tv_img,tv_name,tv_actors,tv_area, tv_year,update_time " \
              "from t_tv where tv_name like '%%%s%%' order by update_time desc " % tv_name
        cursor.execute(sql)
        return cursor.fetchall()

    @staticmethod
    @app_db
    def query_tv_more(cursor, tv_type):
        """
        首页每项视频的更多功能
        :param cursor:
        :param tv_type: 视频的大类
        :return:
        """
        result = {}
        for tty in Config.item_value_list(tv_type):
            sql = f"select tv_id,tv_img,tv_name,tv_actors,tv_area,tv_year,update_time " \
                  f"from t_tv where tv_type='{tty}' order by update_time desc limit 12"
            cursor.execute(sql)
            result[tty] = cursor.fetchall()
        result['tv_types'] = Config.item_list(tv_type)
        where_str = "','".join(Config.item_value_list(tv_type))
        area_sql = f"select group_concat(distinct tv_area) areas from t_tv where tv_type in('{where_str}')"
        cursor.execute(area_sql)
        tv_areas = cursor.fetchone()['areas']
        tv_areas = [aa for aa in str(tv_areas).split(',') if '其' not in aa]
        result['tv_areas'] = tv_areas
        return result

    @staticmethod
    @app_db
    def query_tv_page(cursor, where_str, page_no):
        """
        分页 tv
        :param cursor:
        :param where_str: 查询条件
        :param page_no:
        :return:
        """
        items, total = [], 0

        if where_str:
            sql = f"select tv_id,tv_img,tv_name,tv_actors,tv_area," \
                  f"tv_year,update_time from t_tv where 1=1 {where_str}" \
                  f"order by update_time desc limit {(page_no-1)*30},{page_no*30}"
            cursor.execute(sql)
            items = cursor.fetchall()
            count_sql = f"select count(1) total from t_tv where 1=1 {where_str}"
            cursor.execute(count_sql)
            total = cursor.fetchone()['total']
        return items, total

    @staticmethod
    @app_db
    def query_friend_urls(cursor):
        """
        首页友情链接
        :param cursor:
        :return:
        """
        sql = "select f_title,f_url from t_f_u where del_flag='0'"
        cursor.execute(sql)
        return cursor.fetchall()


if __name__ == '__main__':
    t, u = DB.query_today_total_update('mv')
    print(t, u)

