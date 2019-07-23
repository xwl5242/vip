# -*- coding:utf-8 -*-
import re
import os
import json
import random
from app.db.dao import DB
from app.config import Config
from app.util.jobs import MyJobs
from app.appserver import AppServer
from flask import request, jsonify, send_from_directory


app_server = AppServer()
app = app_server.server_app


@app.route('/')
def index():
    """
    网站首页
    :return:
    """
    # news:最新视频,mvs:电影,dsjs:电视剧,dms:动漫,zys:综艺,today_:今日更新,total_:总视频,
    # mv_kv_type:电影类型,dm_kv_type:动漫类型,zy_kv_type:综艺类型,dsj_kv_type:电视剧类型,fus:友情链接
    tvs = {'mv': json.loads(MyJobs.r.get('mvs')), 'dsj': json.loads(MyJobs.r.get('dsjs')),
           'dm': json.loads(MyJobs.r.get('dms')), 'zy': json.loads(MyJobs.r.get('zys'))}
    return app_server.render('index.html', news=json.loads(MyJobs.r.get('news')), tvs=tvs,
                             today_=json.loads(MyJobs.r.get('today')), total_=json.loads(MyJobs.r.get('total')),
                             fus=DB.query_friend_urls(), banners=DB.index_tops('banner'),)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/t-t/k=<tv_name>')
def tv_type_4_name_html(tv_name):
    """
    根据电影名称搜索，目前用于首页的搜索功能
    :param tv_name: 电影名称
    :return:
    """
    items = DB.index_search(tv_name)
    return app_server.render('tv/tv_item.html', items=items)


@app.route('/err-seek-msg', methods=['POST'])
def err_seek_msg():
    m_type = request.form.get('m_type')
    msg = request.form.get('msg')
    r = DB.insert_msg(m_type, msg)
    return jsonify({'code': 'success' if r else 'fail'})


@app.route('/t-choose/tt=<tv_type>/ti=<tv_item>/ta=<tv_area>/ty=<tv_year>')
def tv_choose_html(tv_type, tv_item, tv_area, tv_year):
    _tv_type = tv_type
    where = []
    if tv_item != 'all':
        tv_type = [(k, v) for (k, v) in Config.TV_KV.get(tv_type) if int(k) == int(tv_item)]
        tv_type = tv_type[0][1] if tv_type and len(tv_type) != 0 else None
        where.append({'tv_type': tv_type})
    if tv_area != 'all':
        where.append({'tv_area': tv_area})
    if tv_year != 'all':
        year = [y for y in Config.YEARS if str(y).startswith(tv_year + ':')]
        year = str(year).split(':')[1]
        year = str(year).split('@')
        where.append({'tv_year': {'$gte': year[0]}})
        where.append({'tv_year': {'$lte': year[1]}})
    return app_server.ti_page_render(request, {'$and': where}, is_choose=True, tv_type=_tv_type,
                                     tv_item=tv_item, tv_area=tv_area, tv_year=tv_year)


@app_server.on_dispatch('index_tv_more_html')
def index_tv_more_html(tv_type):
    """
    跳转到首页tv视频更多页
    :param tv_type:
    :return:
    """
    today, total = DB.today_total(tv_type)
    tv_more = DB.index_tv_more(tv_type)
    tv_more['cur_type'] = tv_type
    tv_more['tv_areas'] = DB.tv_areas(tv_type)
    tv_more['tv_types'] = Config.TV_KV.get(tv_type)
    return app_server.render('tv/tv_more.html', _today=today, _total=total,
                             tv_more=tv_more, banners=DB.index_tops(tv_type))


@app_server.on_dispatch('tv_detail_html')
def tv_detail_html(tv_id):
    """
    tv视频详情页
    :param tv_id: 视频的id
    :return:
    """
    detail = DB.tv_detail(tv_id)
    like_hot = DB.like_hot(detail.get('tv_type'))
    # random select 6 item
    random.shuffle(like_hot)
    return app_server.render('tv/tv_detail.html', tv_detail=detail, like_hots=like_hot[0:6])


@app_server.on_dispatch('index_news_more_html')
def index_news_more_html():
    """
    首页最近更新视频的"更多"链接
    :return:
    """
    return app_server.ti_page_render(request, {})


@app_server.on_dispatch('tv_type_item_html')
def tv_type_item_html(tv_item):
    """
    每个小类的更多链接
    :param tv_item:
    :return:
    """
    tv_item_k, tv_type = '', ''
    for key in Config.TV_KV:
        for k_v in Config.TV_KV[key]:
            if k_v[1] == tv_item:
                tv_type = key
                tv_item_k = k_v[0]
                break
    return tv_type_html(tv_type, tv_item_k)


@app_server.on_dispatch('tv_type_4_actors_html')
def tv_type_4_actors_html(tv_actors):
    """
    根据视频演员搜索相关视频
    :param tv_actors: 演员名字
    :return:
    """
    return app_server.ti_page_render(request, {'tv_actors': re.compile(tv_actors)})


@app_server.on_dispatch('tv_type_4_director_html')
def tv_type_4_director_html(tv_director):
    """
    根据视频导演搜索相关视频
    :param tv_director: 导演名称
    :return:
    """
    return app_server.ti_page_render(request, {'tv_director': re.compile(tv_director)})


@app_server.on_dispatch('tv_type_4_area_html')
def tv_type_4_area_html(tv_area):
    """
    根据视频所属地域搜索相关视频
    :param tv_area: 地域名称
    :return:
    """
    if tv_area == 'other':
        where = {'$and': [{'tv_area': re.compile('其他')}, {'tv_area': re.compile('其它')}]}
    else:
        where = {'tv_area': re.compile(tv_area)}
    return app_server.ti_page_render(request, where)


@app_server.on_dispatch('tv_type_4_year_html')
def tv_type_4_year_html(tv_year):
    """
    根据视频指定的年份搜索相关视频
    :param tv_year: 指定的年份
    :return:
    """
    return app_server.ti_page_render(request, {'tv_year': tv_year})


@app_server.on_dispatch('tv_type_4_between_year_html')
def tv_type_4_between_year_html(cur_type, year):
    """
    根据视频指定的年代搜索相关视频
    :param cur_type: 当前视频类型
    :param year: 年代
    :return:
    """
    year = [y for y in Config.YEARS if str(y).startswith(year+':')]
    year = str(year).split(':')[1]
    year = str(year).split('@')
    tv_type = "','".join(Config.TV_KV_LIST.get(cur_type))
    where = {'$and': [{'tv_type': tv_type}, {'tv_year': {'$gte': year[0]}}, {'tv_year': {'$lte': year[1]}}]}
    return app_server.ti_page_render(request, where)


@app_server.on_dispatch('tv_type_html')
def tv_type_html(tv_type, tv_item):
    """
    tv视频小类的详情页
    :param tv_type: 视频的大类，如mv：电影，dm：动漫
    :param tv_item: 视频的小类，如动作片，国产剧，微电影
    :return:
    """
    # 获取具体的数据库中视频的分类
    _tv_type = tv_type
    tv_type = [(k, v) for (k, v) in Config.TV_KV.get(tv_type) if int(k) == int(tv_item)]
    tv_type = tv_type[0][1] if tv_type and len(tv_type) != 0 else None
    # 查询分页数据
    return app_server.ti_page_render(request, {'tv_type': tv_type}, is_choose=True, tv_type=_tv_type, tv_item=tv_item)


@app_server.on_dispatch('tv_play_html')
def tv_play_html(tv_id, tv_index, tv_source, tv_url):
    """
    视频播放页面，url：视频的地址，detail：视频页面的详情，like_host:热门推荐
    :param tv_id: 播放视频的id
    :param tv_url: 播放视频的url
    :param tv_index:
    :param tv_source:
    :return:
    """
    detail = DB.tv_detail(tv_id)
    like_host = DB.like_hot(detail.get('tv_type'))
    random.shuffle(like_host)
    cur_tv_info = {'index': tv_index, 'source': tv_source, 'url': tv_url}
    return app_server.render('tv/tv_play.html', cur_tv_info=cur_tv_info, tv_detail=detail, like_hots=like_host[0:6])


if __name__ == '__main__':
    # 添加自定义过滤器
    app_server.run()

