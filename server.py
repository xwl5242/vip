# -*- coding:utf-8 -*-
import base64
import random
from flask import Flask, render_template, request
from dao import DB, Config

# name, static resource path, templates resource path
# 整体项目中tv_type为视频的大类（如mv:电影，dm:动漫...）,
# tv_item为视频大类下的具体小类（如动作片，微电影，国产剧...）
app = Flask("yo_vip_tv", static_folder="static", template_folder="templates")


@app.route('/')
def index():
    """
    网站首页
    :return:
    """
    # 今日更新和总视频数量
    today, total = DB.query_today_total_update(None)
    # news:最新视频,mvs:电影,dsjs:电视剧,dms:动漫,zys:综艺,today:今日更新,total:总视频,
    # mv_kv_type:电影类型,dm_kv_type:动漫类型,zy_kv_type:综艺类型,dsj_kv_type:电视剧类型,fus:友情链接
    return render_template('index.html', news=DB.query_index_news(), mvs=DB.query_index_mvs(Config.MV),
                           dsjs=DB.query_index_mvs(Config.DSJ), dms=DB.query_index_mvs(Config.DM),
                           zys=DB.query_index_mvs(Config.ZY), mv_kv_type=Config.item_list(Config.MV),
                           dm_kv_type=Config.item_list(Config.DM), zy_kv_type=Config.item_list(Config.ZY),
                           dsj_kv_type=Config.item_list(Config.DSJ), fus=DB.query_friend_urls(), today=today,
                           total=total)
                           # theme_style=Config.THEME_STYLES[random.randint(0, 7)]
    #                            # )


@app.route('/tv/more/<tv_type>')
def tv_more_2_html(tv_type):
    """
    首页tv视频更多页
    :param tv_type:
    :return:
    """
    html = 'tv/tv_news.html' if tv_type == 'all' else 'tv/tv_more.html'
    today, total = DB.query_today_total_update(tv_type)
    tv_more = DB.query_tv_more(tv_type)
    tv_more['cur_type'] = tv_type
    return render_template(html, today=today, total=total, tv_more=tv_more)


@app.route('/tv/more/i-<tv_item>')
def tv_more_item_2_html(tv_item):
    """
    每个小类的更多链接
    :param tv_item:
    :return:
    """
    tv_item = str(base64.b64decode(str(tv_item).encode('utf-8')), 'utf-8')
    return render_template('tv/tv_item.html')


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
    return render_template('tv/tv_detail.html', tv_detail=detail, like_hots=like_hot[0:6])


@app.route('/t-t/<tv_type>-<tv_index>')
def tv_type_2_html(tv_type, tv_index):
    """
    tv视频小类的详情页
    :param tv_type: 视频的大类，如mv：电影，dm：动漫
    :param tv_index: 视频的小类，如动作片，国产剧，微电影
    :return:
    """
    page_no = request.args.get('p')
    page_no = int(page_no) if page_no else 1
    return render_template('tv/tv_item.html',
                           page_vo=DB.query_tv_type_item_page(tv_type, tv_index, page_no))


@app.route('/tv/choose')
def tv_choose_2_html():

    return render_template('tv/tv_with_choose.html', page_vo={'page_no': 1, 'total': 1})


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
    return render_template('tv/tv_play.html', cur_tv_url=url, tv_detail=detail, like_hosts=like_host[0:6])


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
    # 添加自定义过滤器
    app.add_template_filter(split_strings, 'str_split')
    app.add_template_filter(tv_is_mv, 'tv_is_mv')
    app.add_template_filter(get_list, 'get_list')
    app.add_template_filter(get_sub_list, 'get_sub_list')
    app.add_template_filter(b64encode, 'b64encode')
    app.run(port=80, debug=True)

