# -*- coding:utf-8 -*-
import time
from app.config import Config
from app.db.mysqldb import Base


class DB(Base):

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
        sql = f"select tv_id,tv_ids,tv_name,tv_actors,tv_director,tv_type,tv_area,tv_year,tv_lang,tv_intro,update_time," \
              f"concat('{Config.IMG_WEB}',tv_id,'.jpg') tv_img from t_tv_all where 1=1 and {where} " \
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
        tv_type = Config.TV_KV_LIST.get(tv_type) if tv_type else None
        types = ",".join(['%s' for i in tv_type]) if tv_type else None
        where_str = f" and  tv_type in ({types})" if tv_type else ''
        today_sql = f"select count(1) total from t_tv_all where 1=1 {where_str} and " \
                    f"date_format(update_time,'%Y-%m-%d')=date_format(now(),'%Y-%m-%d') "
        total_sql = f"select count(1) total from t_tv_all where 1=1 {where_str}"
        today = DB.get(today_sql, tv_type)
        total = DB.get(total_sql, tv_type)
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
        top_sql = "select tv_name,tv_img from t_b_t where tv_type=%s"
        tops = Base.query_list(top_sql, (tv_type,))
        if tops and len(tops) > 0:
            for t in tops:
                tn = str(t['tv_name']).strip()
                tvs = DB.query_list(DB.gen_sql("tv_name like %s", 0, 0), ('%'+tn+'%', ))
                if tvs and len(tvs) > 0:
                    result.append({"tv_vo": tvs[0], "tv_img": str(t['tv_img'])})
        return result

    @staticmethod
    def index_news():
        """
        首页最新视频
        :return:
        """
        return DB.query_list(DB.gen_sql('', 0, 12, True), [])

    @staticmethod
    def index_mvs(tv_type):
        """
        首页各种类视频
        :param tv_type: 视频类型 mv,dm,zy,dsj
        :return:
        """
        tv_type = Config.TV_KV_LIST.get(tv_type) if tv_type else None
        types = ",".join(['%s' for i in tv_type]) if tv_type else None
        return DB.query_list(DB.gen_sql(f"tv_type in({types})", 0, 8, True), tv_type)

    @staticmethod
    def like_hot(tv_type_item):
        """
        相关热播，就是同小类型的视频的最新更新的前20个中随机抽取6个
        :param tv_type_item: 视频的小类
        :return:
        """
        return DB.query_list(DB.gen_sql("tv_type = %s", 0, 20, True), (tv_type_item, ))

    @staticmethod
    def tv_detail(tv_id):
        """
        查询tv详情
        :param tv_id: 视频的id
        :return:
        """
        d_sql = DB.gen_sql(f"tv_id=%s", 0, 0)

        u_sql_1 = f"select tv_url,replace(replace(substr(tv_url,1,instr(tv_url,'$')-1),'第',''),'集','') seq, " \
            f"'{Config.TV_SOURCE_MAIN}' as tv_source from t_tv_urls where tv_id=%s"
        u_sql_2 = f"select tv_url,replace(replace(substr(tv_url,1,instr(tv_url,'$')-1),'第',''),'集','') seq, " \
            f"'{Config.TV_SOURCE_3PART}' as tv_source from t_tv_urls_3part where tv_id=%s"
        detail = DB.get(d_sql, (tv_id, ))
        tv_sources = []
        tv_ids = str(detail['tv_ids']).split(',')
        if detail:
            urls = []
            for tid in tv_ids:
                if tid:
                    urls1 = DB.query_list(u_sql_1, (tid, ))
                    urls2 = DB.query_list(u_sql_2, (tid, ))
                    if urls1 and len(urls1) > 0:
                        urls1.sort(key=lambda x: int(x['seq']))
                        urls.extend(urls1)
                        tv_sources.append(Config.TV_SOURCE_MAIN)
                    else:
                        urls2.sort(key=lambda x: int(x['seq']))
                        urls.extend(urls2)
                        tv_sources.append(Config.TV_SOURCE_3PART)
            urls = [(su['tv_source'], su['tv_url']) for su in urls]
            detail['urls'] = urls
            detail['tv_sources'] = tv_sources
        return detail

    @staticmethod
    def index_search(tv_name):
        """
        首页搜素功能
        :param tv_name: 搜索关键字
        :return:
        """
        return DB.query_list(DB.gen_sql("tv_name like %s", 0, 0), ('%'+tv_name+'%', ))

    @staticmethod
    def tv_areas(tv_type):
        """
        某类视频所包含的所有地区
        :param tv_type: 视频的大类
        :return:
        """
        tv_type = Config.TV_KV_LIST.get(tv_type) if tv_type else None
        types = ",".join(['%s' for i in tv_type]) if tv_type else None
        where = f" tv_type in({types}) " if types else ' 1=1 '
        area_sql = f"select group_concat(distinct tv_area) areas from t_tv_all where {where} "
        tv_areas = DB.get(area_sql, tv_type)['areas']
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
        tv_type = Config.TV_KV_LIST.get(tv_type) if tv_type else None
        types = ",".join(['%s' for i in tv_type]) if tv_type else None
        for tty in tv_type:
            result[tty] = DB.query_list(DB.gen_sql(f"tv_type=%s", 0, 12, True), (tty, ))
        result['tv_news'] = DB.query_list(DB.gen_sql(f"tv_type in ({types})", 0, 12, True), tv_type)
        return result

    @staticmethod
    def tv_page(where_str, args):
        """
        分页 tv
        :param where_str: 查询条件
        :param args:
        :return:
        """
        where_str = ' 1=1 ' if not where_str else where_str
        args = [] if not args else args
        return DB.query_page(DB.gen_sql(where_str, 0, 0), args)

    @staticmethod
    def query_friend_urls():
        """
        首页友情链接
        :return:
        """
        sql = "select f_title,f_url from t_f_u where del_flag=%s"
        return DB.query_list(sql, ('0',))

    @staticmethod
    def insert_msg(m_type, msg):
        import uuid
        insert_sql = "insert into t_err_seek_msg(id,type,text,del_flag,create_time) values(%s,%s,%s,%s,%s)"
        print(insert_sql)
        return DB.insert(insert_sql, (str(uuid.uuid4()), m_type, msg, '0',
                                      time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))


if __name__ == '__main__':
    print(DB.tv_page('tv_type=%s', ['动作片', int(0)]))


