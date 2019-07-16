# -*- coding:utf-8 -*-
import re
import time
from app.config import Config
from app.db.mongod import Mongo


class DB(Mongo):

    @staticmethod
    def gen_sql(where, _limit, limit_, use_limit=False):
        """
        因为sql中有很多公用的部分，现在只需传递where条件和是否分页
        :param where: where条件
        :param _limit: limit
        :param limit_: limit
        :param use_limit: 使用limit
        :return:
        """
        where = where if where else ' 1=1 '
        where = str(where).strip()
        where = where[3:] if where.startswith('and') or where.startswith('AND') else where
        sql = f"select tv_id,tv_name,tv_actors,tv_director,tv_type,tv_area,tv_year,tv_lang,tv_intro,update_time," \
              f"concat('{Config.IMG_WEB}',tv_id,'.jpg') tv_img from t_tv where 1=1 and {where} " \
              f"order by update_time desc"
        if use_limit:
            sql += f' limit {_limit},{limit_} '
        return sql

    @staticmethod
    def today_total(tv_type):
        """
        首页今日更新和总视频数量
        :param tv_type: 视频类型mv,dm,zy,dsj;None:all
        :return:
        """
        now = time.strftime('%Y-%m-%d', time.localtime())
        tv_type = Config.TV_KV_LIST.get(tv_type) if tv_type else None
        tv_type_condition = {'tv_type': {'$in': tuple(tv_type)}} if tv_type else {}
        today = Mongo.count('t_tv', {'$and': [tv_type_condition, {'update_time': f'/^{now}/'}]})
        total = Mongo.count('t_tv', tv_type_condition)
        today = today if today else 0
        total = total if total else 0
        return today, total

    @staticmethod
    def index_tops(tv_type):
        """
        查询首页热门推荐数据，数据来源百度风云榜
        :param tv_type: 视频类型 mv,dm,zy,dsj
        :return:
        """
        result = []
        tops = Mongo.find('t_tv_banner_top', {'tv_type': tv_type})
        if tops and len(tops) > 0:
            for t in tops:
                tn = str(t['tv_name']).strip()
                tvs = Mongo.find('t_tv', {'tv_name': re.compile(tn)})
                if tvs and len(tvs) > 0:
                    result.append({"tv_vo": tvs[0], "tv_img": str(t['tv_img'])})
        return result

    @staticmethod
    def index_news():
        """
        首页最新视频
        :return:
        """
        return Mongo.find('t_tv', {}, skip=0, limit=12)

    @staticmethod
    def index_mvs(tv_type):
        """
        首页各种类视频
        :param tv_type: 视频类型 mv,dm,zy,dsj
        :return:
        """
        tv_type = Config.TV_KV_LIST.get(tv_type) if tv_type else None
        return Mongo.find('t_tv', {'tv_type': {'$in': tuple(tv_type)}}, skip=0, limit=8)

    @staticmethod
    def like_hot(tv_type_item):
        """
        相关热播，就是同小类型的视频的最新更新的前20个中随机抽取6个
        :param tv_type_item: 视频的小类
        :return:
        """
        return Mongo.find('t_tv', {'tv_type': tv_type_item}, skip=0, limit=20)

    @staticmethod
    def tv_detail(tv_id):
        """
        查询tv详情
        :param tv_id: 视频的id
        :return:
        """
        detail = Mongo.find_one('t_tv', {'tv_id': tv_id})
        if detail:
            urls = Mongo.find('t_tv_urls', {'tv_id': tv_id})
            urls = [(su['tv_source'], su['tv_url']) for su in urls]
            detail['urls'] = urls
        return detail

    @staticmethod
    def index_search(tv_name):
        """
        首页搜素功能
        :param tv_name: 搜索关键字
        :return:
        """
        return Mongo.find('t_tv', {'tv_name': re.compile(tv_name)})

    @staticmethod
    def tv_areas(tv_type):
        """
        某类视频所包含的所有地区
        :param tv_type: 视频的大类
        :return:
        """
        area_list = []
        tv_type = Config.TV_KV_LIST.get(tv_type) if tv_type else None
        tv_areas = Mongo.get_col('t_tv').aggregate([
            {'$match': {'tv_type': {'$in': tv_type}}},
            {'$group': {'_id': '$img_save', 'tv_areas': {'$addToSet': '$tv_area'}}}
        ])
        for tao in tv_areas:
            if tao.get('_id') == '1':
                tas = tao.get('tv_areas')
                for ta in tas:
                    if '其' not in ta and '更新时间' not in ta and ta not in area_list:
                        area_list.append(ta)
        return area_list

    @staticmethod
    def index_tv_more(tv_type):
        """
        首页每项视频的更多功能
        :param tv_type: 视频的大类
        :return:
        """
        result = {}
        tv_type = Config.TV_KV_LIST.get(tv_type) if tv_type else None
        for tty in tv_type:
            result[tty] = Mongo.find('t_tv', {'tv_type': tv_type}, skip=0, limit=12)
        result['tv_news'] = Mongo.find('t_tv', {'tv_type': {'$in': tv_type}}, skip=0, limit=12)
        return result

    @staticmethod
    def tv_page(condition, page_no):
        """
        分页 tv
        :param condition: 查询条件
        :param page_no: 分页页码
        :return:
        """
        items = Mongo.find_page('t_tv', condition, page_no)
        total = Mongo.count('t_tv', condition)
        return items, total

    @staticmethod
    def query_friend_urls():
        """
        首页友情链接
        :return:
        """
        return Mongo.find('t_f_u', {'del_flag': '0'})

    @staticmethod
    def insert_msg(m_type, msg):
        import uuid
        return Mongo.insert_one('t_err_seek_msg', {'id': str(uuid.uuid4()),
                                                   'type': m_type, 'text': msg, 'del_flag': '0',
                                                   'create_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())})


if __name__ == '__main__':
    print(DB.tv_areas('mv'))

