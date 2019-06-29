# -*- coding:utf-8 -*-
import json
import datetime
import redis
from dao import DB, Config


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


class MyJobs:
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
    r = redis.Redis(connection_pool=pool)

    @classmethod
    def app_index_job(cls):
        import time
        s = time.time()
        print('init--redis')
        news = json.dumps(DB.query_index_news(), ensure_ascii=False, cls=DateEncoder)
        mvs = json.dumps(DB.query_index_mvs(Config.MV), ensure_ascii=False, cls=DateEncoder)
        dsjs = json.dumps(DB.query_index_mvs(Config.DSJ), ensure_ascii=False, cls=DateEncoder)
        dms = json.dumps(DB.query_index_mvs(Config.DM), ensure_ascii=False, cls=DateEncoder)
        zys = json.dumps(DB.query_index_mvs(Config.ZY), ensure_ascii=False, cls=DateEncoder)
        mv_top = json.dumps(DB.query_index_tops(Config.MV)[0:6], ensure_ascii=False, cls=DateEncoder)
        dsj_top = json.dumps(DB.query_index_tops(Config.DSJ)[0:6], ensure_ascii=False, cls=DateEncoder)
        zy_top = json.dumps(DB.query_index_tops(Config.ZY)[0:6], ensure_ascii=False, cls=DateEncoder)
        dm_top = json.dumps(DB.query_index_tops(Config.DM)[0:6], ensure_ascii=False, cls=DateEncoder)
        # 今日更新和总视频数量
        today, total = DB.query_today_total_update(None)
        print(f'{time.time()-s}')
        cls.r.set('news', news)
        cls.r.set('mvs', mvs)
        cls.r.set('dsjs', dsjs)
        cls.r.set('dms', dms)
        cls.r.set('zys', zys)
        cls.r.set('mv_top', mv_top)
        cls.r.set('dsj_top', dsj_top)
        cls.r.set('zy_top', zy_top)
        cls.r.set('dm_top', dm_top)
        cls.r.set('today', today)
        cls.r.set('total', total)
        del news, mvs, dsjs, dms, zys, mv_top, dsj_top, zy_top, dm_top


if __name__ == '__main__':
    MyJobs.app_index_job()
    print(MyJobs.r.get('news'))
