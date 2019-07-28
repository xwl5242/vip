# -*- coding:utf-8 -*-
import json
import redis
from app.taobao import TBApi
from app.config import Config
if Config.RUN_PLATFORM == 'mysql':
    from app.db.mysql_dao import DB
else:
    from app.db.mongo_dao import DB


class MyJobs:
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
    r = redis.Redis(connection_pool=pool)

    @classmethod
    def app_index_job(cls):
        """
        cron, init index info
        :return:
        """
        import time
        s = time.time()
        print('init--redis')
        news = json.dumps(DB.index_news(), ensure_ascii=False)
        mvs = json.dumps(DB.index_mvs('mv'), ensure_ascii=False)
        dsjs = json.dumps(DB.index_mvs('dsj'), ensure_ascii=False)
        dms = json.dumps(DB.index_mvs('dm'), ensure_ascii=False)
        zys = json.dumps(DB.index_mvs('zy'), ensure_ascii=False)
        mv_top = json.dumps(DB.index_tops('mv')[0:6], ensure_ascii=False)
        dsj_top = json.dumps(DB.index_tops('dsj')[0:6], ensure_ascii=False)
        zy_top = json.dumps(DB.index_tops('zy')[0:6], ensure_ascii=False)
        dm_top = json.dumps(DB.index_tops('dm')[0:6], ensure_ascii=False)
        # 今日更新和总视频数量
        today, total = DB.today_total(None)
        # 淘宝广告
        ads = json.dumps(TBApi.get_tb_goods(), ensure_ascii=False)
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
        cls.r.set('ads', ads)
        del news, mvs, dsjs, dms, zys, mv_top, dsj_top, zy_top, dm_top, ads
        print(f'{time.time() - s}')

