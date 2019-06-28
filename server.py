# -*- coding:utf-8 -*-
import base64
from flask import Flask, render_template, jsonify
from dao import DB, Config
# name, static resource path, templates resource path
app = Flask("yo_vip_tv", static_folder="static", template_folder="templates")


@app.route('/')
def index():
    """
    网站首页
    :return:
    """
    # 今日更新和总视频数量
    today, total = DB.query_index_today_total_update()
    # news:最新视频,mvs:电影,dsjs:电视剧,dms:动漫,zys:综艺,today:今日更新,total:总视频,
    # mv_type:电影类型,dm_type:动漫类型,zy_type:综艺类型,dsj_type:电视剧类型,fus:友情链接
    return render_template('index.html', news=DB.query_index_news(), mvs=DB.query_index_mvs(Config.MV),
                           dsjs=DB.query_index_mvs(Config.DSJ), dms=DB.query_index_mvs(Config.DM),
                           zys=DB.query_index_mvs(Config.ZY), today=today, total=total, mv_type=Config.MV_TYPE,
                           dm_type=Config.DM_TYPE, zy_type=Config.ZY_TYPE, dsj_type=Config.DSJ_TYPE,
                           fus=DB.query_friend_urls())


@app.route('/t-d/<tv_id>')
def tv_detail(tv_id):
    """
    tv视频详情页
    :param tv_id:
    :return:
    """
    return render_template('tv/tv_detail.html', tv_detail=DB.query_tv_detail(tv_id))


@app.route('/t-t/<tv_type>-<tv_index>')
def tv_type(tv_type, tv_index):
    """
    tv视频某一类详情页
    :param tv_id:
    :return:
    """
    return render_template('tv/tv.html')


@app.route('/tv/more/<tv_type>')
def tv_more(tv_type):
    """
    tv视频更多页
    :param tv_type:
    :return:
    """
    # tv_type: all/mv/dm/zy/dsj
    return render_template('tv/tv.html')


@app.route('/t-play/url=<url>')
def tv_play_by_url(url):
    url = str(base64.b64decode(str(url).encode('utf-8')), 'utf-8')
    print(url)


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
    app.add_template_filter(split_strings, 'str_split')
    app.add_template_filter(tv_is_mv, 'tv_is_mv')
    app.add_template_filter(get_list, 'get_list')
    app.add_template_filter(get_sub_list, 'get_sub_list')
    app.add_template_filter(b64encode, 'b64encode')
    app.run(port=80, debug=True)

