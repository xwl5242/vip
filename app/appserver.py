# -*- coding:utf-8 -*-
import json
from functools import wraps
from app.config import Config
from app.util.jobs import MyJobs
from app.util import filters as ft
from flask_apscheduler import APScheduler
from flask import Flask, render_template
if Config.RUN_PLATFORM == 'mysql':
    from app.db.mysql_dao import DB
else:
    from app.db.mongo_dao import DB


def _dispatch_decorator():
    def deco_decorator(self, router):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            self._handlers[router] = wrapper
            return wrapper
        return decorator
    return deco_decorator


class AppServer:

    def __init__(self):
        self._handlers = dict()
        self.scheduler = APScheduler()
        self._server_app = Flask('yoviptv')
        self._server_app.route('/cnm/<route>')(self._dispatch)

    @property
    def server_app(self):
        """
        flask app, 并添加filters，jobs
        :return:
        """
        self._server_app.add_template_filter(ft.split_strings, 'str_split')
        self._server_app.add_template_filter(ft.get_tuple, 'get_tuple')
        self._server_app.add_template_filter(ft.get_list, 'get_list')
        self._server_app.add_template_filter(ft.get_sub_list, 'get_sub_list')
        self._server_app.add_template_filter(ft.b64encode, 'b64encode')
        self.scheduler.init_app(self._server_app)
        self.scheduler.add_job(id='app-job', func=MyJobs.app_index_job, trigger='interval', seconds=11 * 60)
        self.scheduler.start()
        return self._server_app

    on_dispatch = _dispatch_decorator()

    def _dispatch(self, route):
        """
        dispatch，请求跳转，根据地址中的加密字段进行跳转
        :param route: 请求地址中的加密字段，包含要执行的router名称和参数
        :return:
        """
        route = ft.b64_str_decode(route)
        if route:
            if ';;;' in route:
                func = route.split(';;;')[0]
                params = route.split(';;;')[1]
                params = params.split('@')
                handler = self._handlers.get(func)
                if handler:
                    return handler(*params)
            else:
                handler = self._handlers.get(route)
                if handler:
                    return handler()

    def run(self, host='127.0.0.1', port=9999, **kwargs):
        """
        flask启动
        :param host: host，默认是127.0.0.1
        :param port: 端口，默认是9999
        :param kwargs: 其他flask app run的参数，如 debug=False
        :return:
        """
        self._server_app.run(host=host, port=port, **kwargs)

    @staticmethod
    def render(html, to_page=False, **kwargs):
        """
        render template, have tops and tv_type
        :param html: 要渲染的页面路径
        :param to_page: 是否分页
        :param kwargs: 要传递到页面上obj
        :return:
        """
        tv_tops = {'mv': json.loads(MyJobs.r.get('mv_top')), 'dsj': json.loads(MyJobs.r.get('dsj_top')),
                   'dm': json.loads(MyJobs.r.get('dm_top')), 'zy': json.loads(MyJobs.r.get('zy_top'))}
        tv_types = {'mv': Config.TV_KV.get('mv'), 'dsj': Config.TV_KV.get('dsj'),
                    'dm': Config.TV_KV.get('dm'), 'zy': Config.TV_KV.get('zy')}
        ads = json.loads(MyJobs.r.get('ads'))
        return render_template(html, to_page=to_page, tv_tops=tv_tops, tv_types=tv_types,
                               tv=Config.TV, tv_years=Config.YEARS, ads=ads, **kwargs)

    @staticmethod
    def ti_page_render(req, condition, args, is_choose=False, tv_type=None, tv_item=None, tv_area='all', tv_year='all'):
        """
        render template for pagination
        :param req: 请求 request
        :param condition: where 查询条件
        :param args: where 查询条件中对应的值
        :param is_choose: 要渲染的页面是否需要筛选功能展示
        :param tv_type: is_choose为True时必填 tv的大类
        :param tv_item: is_choose为True时必填 tv的小类
        :param tv_area: 页面筛选条件中的地区
        :param tv_year: 页面筛选条件中的年份
        :return:
        """
        page_no = req.args.get('p')
        page_no = int(page_no) if page_no else 1
        args = list(args)
        args.append(page_no)
        items, total = DB.tv_page(condition, tuple(args))
        tv_choose = {}
        if is_choose and tv_type and tv_item:
            tv_choose['tvs'] = Config.TV
            tv_choose['tv_types'] = Config.TV_KV
            tv_choose['tv_areas'] = DB.tv_areas(tv_type)
            tv_choose['tv_years'] = Config.YEARS
        return AppServer.render('tv/tv_item.html', to_page=True, page_no=page_no,
                                cur_tv_area=tv_area, cur_tv_year=tv_year, cur_tv_type=tv_type,
                                cur_tv_item=tv_item, is_choose=is_choose, items=items, total=total,
                                tv_choose=tv_choose)



