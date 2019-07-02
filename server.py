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
    """
    render template, have tops and tv_type
    :param html: 要渲染的页面路径
    :param to_page: 是否分页
    :param kwargs: 要传递到页面上obj
    :return:
    """
    return render_template(html, to_page=to_page,
                           mv_top=json.loads(j.r.get('mv_top')), dsj_top=json.loads(j.r.get('dsj_top')),
                           zy_top=json.loads(j.r.get('zy_top')),  dm_top=json.loads(j.r.get('dm_top')),
                           mv_kv_type=Config.TV_KV.get('mv'), dm_kv_type=Config.TV_KV.get('dm'),
                           zy_kv_type=Config.TV_KV.get('zy'), dsj_kv_type=Config.TV_KV.get('dsj'), **kwargs)


def to_page_html(req, where, html):
    """
    render template for pagination
    :param req: 请求 request
    :param where: where 查询条件
    :param html: 要渲染的页面路径
    :return:
    """
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
def index_news_more_html():
    """
    首页最近更新视频的"更多"链接
    :return:
    """
    return to_page_html(request, None, 'tv/tv_item.html')


@app.route('/t-t/i=<tv_item>')
def tv_type_item_html(tv_item):
    """
    每个小类的更多链接
    :param tv_item:
    :return:
    """
    tv_item = au.b64_str_decode(tv_item)
    tv_item_k, tv_type = '', ''
    for key in Config.TV_KV:
        for k_v in Config.TV_KV[key]:
            if k_v[1] == tv_item:
                tv_type = key
                tv_item_k = k_v[0]
                break
    return redirect(f'/t-t/{tv_type}-{tv_item_k}')


@app.route('/t-t/actors=<tv_actors>')
def tv_type_4_actors_html(tv_actors):
    """
    根据视频演员搜索相关视频
    :param tv_actors: 演员名字
    :return:
    """
    tv_actors = au.b64_str_decode(tv_actors)
    where = f"tv_actors like '%{tv_actors}%' "
    return to_page_html(request, where, 'tv/tv_item.html')


@app.route('/t-t/director=<tv_director>')
def tv_type_4_director_html(tv_director):
    """
    根据视频导演搜索相关视频
    :param tv_director: 导演名称
    :return:
    """
    tv_director = au.b64_str_decode(tv_director)
    where = f"tv_director like '%{tv_director}%' "
    return to_page_html(request, where, 'tv/tv_item.html')


@app.route('/t-t/area=<tv_area>')
def tv_type_4_area_html(tv_area):
    """
    根据视频所属地域搜索相关视频
    :param tv_area: 地域名称
    :return:
    """
    tv_area = au.b64_str_decode(tv_area)
    if tv_area == 'other':
        where = f"(tv_area like '%其他%' or tv_area like '%其它%')"
    else:
        where = f"tv_area like '%{tv_area}%' "
    return to_page_html(request, where, 'tv/tv_item.html')


@app.route('/t-t/year=<tv_year>')
def tv_type_4_year_html(tv_year):
    """
    根据视频指定的年份搜索相关视频
    :param tv_year: 指定的年份
    :return:
    """
    where = f"tv_year = '{tv_year}' "
    return to_page_html(request, where, 'tv/tv_item.html')


@app.route('/t-t/year_bt-<cur_type>-<year>')
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
    where = f"tv_type in ('{tv_type}') and tv_year >= {year[0]} and tv_year <= {year[1]}"
    return to_page_html(request, where, 'tv/tv_item.html')


@app.route('/t-t/k=<tv_name>')
def tv_type_4_name_html(tv_name):
    """
    根据电影名称搜索，目前用于首页的搜索功能
    :param tv_name: 电影名称
    :return:
    """
    items = DB.index_search(tv_name)
    return render_template_('tv/tv_item.html', items=items)


@app.route('/t-t/<tv_type>-<tv_item>')
def tv_type_html(tv_type, tv_item):
    """
    tv视频小类的详情页
    :param tv_type: 视频的大类，如mv：电影，dm：动漫
    :param tv_item: 视频的小类，如动作片，国产剧，微电影
    :return:
    """
    # 获取具体的数据库中视频的分类
    tv_type = [(k, v) for (k, v) in Config.TV_KV.get(tv_type) if int(k) == int(tv_item)]
    tv_type = tv_type[0][1] if tv_type and len(tv_type) != 0 else None
    # 查询分页数据
    where = f"tv_type = '{tv_type}'"
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
    j.app_index_job()
    # 添加自定义过滤器
    app.add_template_filter(au.split_strings, 'str_split')
    app.add_template_filter(au.tv_is_mv, 'tv_is_mv')
    app.add_template_filter(au.get_list, 'get_list')
    app.add_template_filter(au.get_sub_list, 'get_sub_list')
    app.add_template_filter(au.b64encode, 'b64encode')
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    scheduler.add_job(id='app_index_job', func=j.app_index_job, trigger='interval', seconds=11*60)
    app.run(host='0.0.0.0', port=9999, debug=False)

