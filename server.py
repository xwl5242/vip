# -*- coding:utf-8 -*-
import json
import base64
import random
from jobs import MyJobs as j
from flask_apscheduler import APScheduler
from flask import Flask, render_template, request, redirect, url_for
from dao import DB, Config

# name, static resource path, templates resource path
# 整体项目中tv_type为视频的大类（如mv:电影，dm:动漫...）,
# tv_item为视频大类下的具体小类（如动作片，微电影，国产剧...）
app = Flask("yo_vip_tv", static_folder="static", template_folder="templates")


def b64_str_decode(b):
    return str(base64.b64decode(str(b).encode('utf-8')), 'utf-8')


def render_template_(html, to_page=False, **kwargs):
    return render_template(html, mv_top=json.loads(j.r.get('mv_top')), dsj_top=json.loads(j.r.get('dsj_top')),
                           zy_top=json.loads(j.r.get('zy_top')),  dm_top=json.loads(j.r.get('dm_top')), to_page=to_page,
                           mv_kv_type=Config.item_list(Config.MV), dm_kv_type=Config.item_list(Config.DM),
                           zy_kv_type=Config.item_list(Config.ZY), dsj_kv_type=Config.item_list(Config.DSJ), **kwargs)


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
def tv_more_2_html(tv_type):
    """
    首页tv视频更多页
    :param tv_type:
    :return:
    """
    today, total = DB.query_today_total_update(tv_type)
    tv_more = DB.query_tv_more(tv_type)
    tv_more['cur_type'] = tv_type
    return render_template_('tv/tv_more.html', today=today, total=total, tv_more=tv_more)


@app.route('/t-d/<tv_id>')
def tv_detail_2_html(tv_id):
    """
    tv视频详情页
    :param tv_id: 视频的id
    :return:
    """
    tv_id = str(base64.b64decode(str(tv_id).encode('utf-8')), 'utf-8')
    detail = DB.query_tv_detail(tv_id)
    like_hot = DB.query_tv_like_hot(detail.get('tv_type'))
    # random select 6 item
    random.shuffle(like_hot)
    return render_template_('tv/tv_detail.html', tv_detail=detail, like_hots=like_hot[0:6])


@app.route('/t-t/a')
def tv_type_all():
    page_no = request.args.get('p')
    page_no = int(page_no) if page_no else 1
    items, total = DB.query_tv_page(' and 1=1 ', page_no)
    return render_template_('tv/tv_item.html', to_page=True, items=items, total=total, page_no=page_no)


@app.route('/t-t/i=<tv_item>')
def tv_type_item_2_html(tv_item):
    """
    每个小类的更多链接
    :param tv_item:
    :return:
    """
    tv_item = str(base64.b64decode(str(tv_item).encode('utf-8')), 'utf-8')
    tv_item_k, tv_type = '', ''
    for kvs in Config.TV_TYPE_KV_DICT:
        for kkvv in Config.TV_TYPE_KV_DICT[kvs]:
            if kkvv['value'] == tv_item:
                tv_type = kvs
                tv_item_k = kkvv['key']
                break
    return redirect(f'/t-t/{tv_type}-{tv_item_k}')


@app.route('/t-t/k=<tv_name>')
def tv_type_4_name_2_html(tv_name):
    """
    根据电影名称搜索，目前用于首页的搜索功能
    :param tv_name: 电影名称
    :return:
    """
    items = DB.query_tv_more_by_name(tv_name)
    return render_template('tv/tv_item.html', items=items)


@app.route('/t-t/<tv_type>-<tv_item>')
def tv_type_2_html(tv_type, tv_item):
    """
    tv视频小类的详情页
    :param tv_type: 视频的大类，如mv：电影，dm：动漫
    :param tv_item: 视频的小类，如动作片，国产剧，微电影
    :return:
    """
    # 获取分页信息中的页码
    page_no = request.args.get('p')
    page_no = int(page_no) if page_no else 1
    # 获取具体的数据库中视频的分类
    tv_type = [(k, v) for (k, v) in Config.item_list(tv_type) if int(k) == int(tv_item)]
    tv_type = tv_type[0][1] if tv_type and len(tv_type) != 0 else None
    # 查询分页数据
    items, total = DB.query_tv_page(f" and tv_type = '{tv_type}'", page_no)
    return render_template_('tv/tv_item.html', to_page=True, items=items, total=total, page_no=page_no)


@app.route('/tv/choose')
def tv_choose_2_html():
    return render_template_('tv/tv_with_choose.html', to_page=True, page_vo={'page_no': 1, 'total': 1})


@app.route('/t-play/<tv_id>/url=<url>')
def tv_play_2_html(tv_id, url):
    """
    视频播放页面，url：视频的地址，detail：视频页面的详情，like_host:热门推荐
    :param tv_id: 播放视频的id
    :param url: 播放视频的url
    :return:
    """
    url = str(base64.b64decode(str(url).encode('utf-8')), 'utf-8')
    tv_id = str(base64.b64decode(str(tv_id).encode('utf-8')), 'utf-8')
    detail = DB.query_tv_detail(tv_id)
    like_host = DB.query_tv_like_hot(detail.get('tv_type'))
    random.shuffle(like_host)
    return render_template_('tv/tv_play.html', cur_tv_url=url, tv_detail=detail, like_hots=like_host[0:6])


def split_strings(s, sep=','):
    s = s if s else ''
    return str(s).split(sep)


def tv_is_mv(t_type):
    t_type = t_type if t_type else 'none'
    return '1' if t_type in Config.MV else '0'


def get_list(l, index):
    return l[index] if l and len(l) > 0 else []


def get_sub_list(l, start, end):
    return l[start:end] if l and len(l) > 0 else []


def b64encode(s):
    return str(base64.b64encode(s.encode('utf-8')), 'utf-8')


if __name__ == '__main__':
    # DEBUG RUN
    j.app_index_job()
    # 添加自定义过滤器
    app.add_template_filter(split_strings, 'str_split')
    app.add_template_filter(tv_is_mv, 'tv_is_mv')
    app.add_template_filter(get_list, 'get_list')
    app.add_template_filter(get_sub_list, 'get_sub_list')
    app.add_template_filter(b64encode, 'b64encode')
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    scheduler.add_job(id='app_index_job', func=j.app_index_job, trigger='interval', seconds=17*60)
    app.run(host='0.0.0.0', port=80, debug=True)

