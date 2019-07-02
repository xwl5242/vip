# -*- coding:utf-8 -*-
from app.config import Config
from app.db.base import Base


class DB(Base):

    @staticmethod
    def gen_sql(where, _limit, limit_, use_limit=False):
        """
        因为sql中有很多公用的部分，现在只需传递where条件和是否分页
        :param where: where条件
        :param use_limit: 是否用limit
        :param _limit: limit 开始
        :param limit_: limit 结束
        :return:
        """
        where = where if where else ' 1=1 '
        where = str(where).strip()
        where = where[3:] if where.startswith('and') or where.startswith('AND') else where
        sql = f"select tv_id,tv_name,tv_actors,tv_director,tv_type,tv_area,tv_year,tv_lang,tv_intro,update_time," \
              f"concat('{Config.IMG_WEB}',tv_id,'.jpg') tv_img from t_tv where 1=1 and {where} " \
              f"order by update_time desc"
        if use_limit:
            sql = sql + f' limit {_limit},{limit_} '
        return sql

    @staticmethod
    def today_total(tv_type):
        """
        首页今日更新和总视频数量
        :param tv_type: 视频类型mv,dm,zy,dsj;None:all
        :return:
        """
        tv_type = Config.TV_KV_LIST.get(tv_type) if tv_type else None
        types = "','".join(tv_type) if tv_type else None
        where_str = f" and  tv_type in ('{types}')" if tv_type else ''
        today_sql = f"select count(1) total from t_tv where 1=1 {where_str} and " \
                    f"date_format(update_time,'%Y-%m-%d')=date_format(now(),'%Y-%m-%d') "
        total_sql = f"select count(1) total from t_tv where 1=1 {where_str}"
        today = DB.get(today_sql)
        total = DB.get(total_sql)
        today = today['total'] if today and today['total'] else 0
        total = total['total'] if total and total['total'] else 0
        return today, total

    @staticmethod
    def index_tops(tv_type):
        """
        查询首页热门推荐数据，数据来源百度风云榜
        :param tv_type: 视频类型 mv,dm,zy,dsj
        :return:
        """
        result = []
        top_sql = f"select tv_name,tv_top from t_tv_top where tv_type='{tv_type}'"
        tops = Base.query_list(top_sql)
        if tops and len(tops) > 0:
            for t in tops:
                tvs = DB.query_list(DB.gen_sql(f"tv_name like '%%{t['tv_name']}%%'", 0, 0))
                if tvs and len(tvs) > 0:
                    result.append({"tv_vo": tvs[0], "tv_top": int(t['tv_top'])})
        return result

    @staticmethod
    def index_news():
        """
        首页最新视频
        :return:
        """
        return DB.query_list(DB.gen_sql('', 0, 12, True))

    @staticmethod
    def index_mvs(tv_type):
        """
        首页各种类视频
        :param tv_type: 视频类型 mv,dm,zy,dsj
        :return:
        """
        where_str = "','".join(Config.TV_KV_LIST.get(tv_type))
        return DB.query_list(DB.gen_sql(f"tv_type in('{where_str}')", 0, 8, True))

    @staticmethod
    def like_hot(tv_type_item):
        """
        相关热播，就是同小类型的视频的最新更新的前20个中随机抽取6个
        :param tv_type_item: 视频的小类
        :return:
        """
        return DB.query_list(DB.gen_sql(f"tv_type = '{tv_type_item}'", 0, 20, True))

    @staticmethod
    def tv_detail(tv_id):
        """
        查询tv详情
        :param tv_id: 视频的id
        :return:
        """
        d_sql = DB.gen_sql(f"tv_id='{tv_id}'", 0, 0)
        u_sql = f"select tv_url from t_tv_urls where tv_id='{tv_id}'"
        detail = DB.get(d_sql)
        if detail:
            urls = DB.query_list(u_sql)
            urls = [url['tv_url'] for url in urls]
            detail['urls'] = urls
        return detail

    @staticmethod
    def index_search(tv_name):
        """
        首页搜素功能
        :param tv_name: 搜索关键字
        :return:
        """
        return DB.query_list(DB.gen_sql(f"tv_name like '%%{tv_name}%%'", 0, 0))

    @staticmethod
    def tv_areas(tv_type):
        """
        某类视频所包含的所有地区
        :param tv_type: 视频的大类
        :return:
        """
        where_str = "','".join(Config.TV_KV_LIST.get(tv_type)) if tv_type else None
        where = f" tv_type in('{where_str}') " if where_str else ' 1=1 '
        area_sql = f"select group_concat(distinct tv_area) areas from t_tv where {where} "
        tv_areas = DB.get(area_sql)['areas']
        tv_areas = [aa for aa in str(tv_areas).split(',') if '其' not in aa]
        return tv_areas

    @staticmethod
    def index_tv_more(tv_type):
        """
        首页每项视频的更多功能
        :param tv_type: 视频的大类
        :return:
        """
        result = {}
        where_str = "','".join(Config.TV_KV_LIST.get(tv_type))
        for tty in Config.TV_KV_LIST.get(tv_type):
            result[tty] = DB.query_list(DB.gen_sql(f"tv_type='{tty}'", 0, 12, True))
        result['tv_news'] = DB.query_list(DB.gen_sql(f"tv_type in ('{where_str}')", 0, 12, True))
        return result

    @staticmethod
    def tv_page(where_str, page_no):
        """
        分页 tv
        :param where_str: 查询条件
        :param page_no:
        :return:
        """
        where_str = ' 1=1 ' if not where_str else where_str
        return DB.query_page(DB.gen_sql(where_str, 0, 0), page_no)

    @staticmethod
    def query_friend_urls():
        """
        首页友情链接
        :return:
        """
        sql = "select f_title,f_url from t_f_u where del_flag='0'"
        return DB.query_list(sql)


if __name__ == '__main__':
    print(DB.today_total(None))


