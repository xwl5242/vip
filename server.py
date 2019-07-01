# -*- coding:utf-8 -*-
import json
import random
import app.util.apps as au
from app.config import Config
from app.util.jobs import MyJobs as j
from app.db.dao import DB
from flask_apscheduler import APScheduler
from flask import Flask, render_template, request, redirect

# name, static resource path, templates resource path
# 整体项目中tv_type为视频的大类（如mv:电影，dm:动漫...）,
# tv_item为视频大类下的具体小类（如动作片，微电影，国产剧...）
app = Flask("yo_vip_tv", static_folder="static", template_folder="templates")


def render_template_(html, to_page=False, **kwargs):
    return render_template(html, to_page=False,
                           mv_top=json.loads(j.r.get('mv_top')), dsj_top=json.loads(j.r.get('dsj_top')),
                           zy_top=json.loads(j.r.get('zy_top')),  dm_top=json.loads(j.r.get('dm_top')),
                           mv_kv_type=Config.TV_KV.get('mv'), dm_kv_type=Config.TV_KV.get('dm'),
                           zy_kv_type=Config.TV_KV.get('zy'), dsj_kv_type=Config.TV_KV.get('dsj'), **kwargs)


def to_page_html(req, where, html):
    page_no = req.args.get('p')
    page_no = int(page_no) if page_no else 1
    items, total = DB.tv_page(where, page_no)
    return render_template_(html, to_page=True, items=items, total=total, page_no=page_no)


@app.route('/')
def index():
    """
    网站首页
    :return:
    """
    # news:最新视频,mvs:电影,dsjs:电视剧,dms:动漫,zys:综艺,today_:今日更新,total_:总视频,
    # mv_kv_type:电影类型,dm_kv_type:动漫类型,zy_kv_type:综艺类型,dsj_kv_type:电视剧类型,fus:友情链接
    return render_template_('index.html', news=json.loads(j.r.get('news')), mvs=json.loads(j.r.get('mvs')),
                            dsjs=json.loads(j.r.get('dsjs')), dms=json.loads(j.r.get('dms')),
                            zys=json.loads(j.r.get('zys')),  today_=json.loads(j.r.get('today')),
                            total_=json.loads(j.r.get('total')), fus=DB.query_friend_urls())


@app.route('/tv/more/<tv_type>')
def index_more_html(tv_type):
    """
    跳转到首页tv视频更多页
    :param tv_type:
    :return:
    """
    today, total = DB.today_total(tv_type)
    tv_more = DB.index_tv_more(tv_type)
    tv_more['cur_type'] = tv_type
    return render_template_('tv/tv_more.html', _today=today, _total=total, tv_more=tv_more)


@app.route('/t-d/<tv_id>')
def tv_detail_html(tv_id):
    """
    tv视频详情页
    :param tv_id: 视频的id
    :return:
    """
    tv_id = au.b64_str_decode(tv_id)
    detail = DB.tv_detail(tv_id)
    like_hot = DB.like_hot(detail.get('tv_type'))
    # random select 6 item
    random.shuffle(like_hot)
    return render_template_('tv/tv_detail.html', tv_detail=detail, like_hots=like_hot[0:6])


@app.route('/t-t/a')
def tv_type_all():
    return to_page_html(request, None, 'tv/tv_item.html')


@app.route('/t-t/i=<tv_item>')
def tv_type_item_2_html(tv_item):
    """
    每个小类的更多链接
    :param tv_item:
    :return:
    """
    tv_item = au.b64_str_decode(tv_item)
    tv_item_k, tv_type = '', ''
    for kvs in Config.TV_TYPE_KV_DICT:
        for kkvv in Config.TV_TYPE_KV_DICT[kvs]:
            if kkvv['value'] == tv_item:
                tv_type = kvs
                tv_item_k = kkvv['key']
                break
    return redirect(f'/t-t/{tv_type}-{tv_item_k}')


@app.route('/t-t/actors=<tv_actors>')
def tv_type_4_actors_2_html(tv_actors):
    tv_actors = au.b64_str_decode(tv_actors)
    where = f" and tv_actors like '%%{tv_actors}%%' "
    return to_page_html(request, where, 'tv/tv_item.html')


@app.route('/t-t/director=<tv_director>')
def tv_type_4_director_2_html(tv_director):
    tv_director = au.b64_str_decode(tv_director)
    where = f" and tv_director like '%%{tv_director}%%' "
    return to_page_html(request, where, 'tv/tv_item.html')


@app.route('/t-t/area=<tv_area>')
def tv_type_4_area_2_html(tv_area):
    tv_area = au.b64_str_decode(tv_area)
    where = f" and tv_area like '%%{tv_area}%%' "
    return to_page_html(request, where, 'tv/tv_item.html')


@app.route('/t-t/year=<tv_year>')
def tv_type_4_year_2_html(tv_year):
    where = f" and tv_year = '{tv_year}' "
    return to_page_html(request, where, 'tv/tv_item.html')


@app.route('/t-t/k=<tv_name>')
def tv_type_4_name_2_html(tv_name):
    """
    根据电影名称搜索，目前用于首页的搜索功能
    :param tv_name: 电影名称
    :return:
    """
    items = DB.index_search(tv_name)
    return render_template('tv/tv_item.html', items=items)


@app.route('/t-t/<tv_type>-<tv_item>')
def tv_type_2_html(tv_type, tv_item):
    """
    tv视频小类的详情页
    :param tv_type: 视频的大类，如mv：电影，dm：动漫
    :param tv_item: 视频的小类，如动作片，国产剧，微电影
    :return:
    """
    # 获取具体的数据库中视频的分类
    tv_type = [(k, v) for (k, v) in Config.item_list(tv_type) if int(k) == int(tv_item)]
    tv_type = tv_type[0][1] if tv_type and len(tv_type) != 0 else None
    # 查询分页数据
    where = f" and tv_type = '{tv_type}'"
    return to_page_html(request, where, 'tv/tv_item.html')


@app.route('/tv/choose')
def tv_choose_2_html():
    return render_template_('tv/tv_with_choose.html', to_page=True, page_vo={'page_no': 1, 'total': 1})


@app.route('/t-play/<tv_id>/url=<url>')
def tv_play_html(tv_id, url):
    """
    视频播放页面，url：视频的地址，detail：视频页面的详情，like_host:热门推荐
    :param tv_id: 播放视频的id
    :param url: 播放视频的url
    :return:
    """
    url = au.b64_str_decode(url)
    tv_id = au.b64_str_decode(tv_id)
    detail = DB.tv_detail(tv_id)
    like_host = DB.like_hot(detail.get('tv_type'))
    random.shuffle(like_host)
    return render_template_('tv/tv_play.html', cur_tv_url=url, tv_detail=detail, like_hots=like_host[0:6])


if __name__ == '__main__':
    # DEBUG RUN
    # j.app_index_job()
    # 添加自定义过滤器
    app.add_template_filter(au.split_strings, 'str_split')
    app.add_template_filter(au.tv_is_mv, 'tv_is_mv')
    app.add_template_filter(au.get_list, 'get_list')
    app.add_template_filter(au.get_sub_list, 'get_sub_list')
    app.add_template_filter(au.b64encode, 'b64encode')
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    scheduler.add_job(id='app_index_job', func=j.app_index_job, trigger='interval', seconds=17*60)
    app.run(host='0.0.0.0', port=80, debug=True)

