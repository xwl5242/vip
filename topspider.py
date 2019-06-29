# -*- coding:utf-8 -*-

import pymysql
import random
import requests
from lxml import etree


class TopSpider:

    def __init__(self):
        self.user_agent_list = [
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
            "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
        ]
        self.tv_type_url_map = {'mv': 'http://top.baidu.com/buzz?b=26&c=1&fr=topcategory_c1',
                                'dsj': 'http://top.baidu.com/buzz?b=4&c=2&fr=topcategory_c2',
                                'zy': 'http://top.baidu.com/buzz?b=19&c=3&fr=topcategory_c3',
                                'dm': 'http://top.baidu.com/buzz?b=23&c=5&fr=topcategory_c5'}
        self.tops = []

    def parse_top(self, html):
        if html and isinstance(html, str):
            root = etree.HTML(html)
            name = root.xpath("//div[@class='grayborder']//table//a[@class='list-title']//text()")
            num = root.xpath("//div[@class='grayborder']//table//span[starts-with(@class,'icon')]//text()")
            self.tops = [(n, num[i]) for (i, n) in enumerate(name)]

    def fetch_top(self, tv_type):
        db = pymysql.Connect(host='182.61.172.229', user='root',
                             password='@xwl082933048.', database='tv',
                             charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        try:
            url = self.tv_type_url_map.get(tv_type, '')
            r = requests.get(url, headers={'User-Agent': random.choice(self.user_agent_list)})
            self.parse_top(r.content.decode('GB18030'))
            if self.tops and len(self.tops) > 0:
                cursor = db.cursor()
                del_sql = f"delete from t_tv_top where tv_type='{tv_type}'"
                cursor.execute(del_sql)
                for top in self.tops:
                    insert_sql = f"insert into t_tv_top(tv_type,tv_name,tv_top) values('{tv_type}','{top[0]}','{top[1]}')"
                    cursor.execute(insert_sql)
                db.commit()
        except Exception as e:
            db.rollback()
            print(repr(e))


if __name__ == '__main__':
    import time
    ts = TopSpider()
    ts.fetch_top('mv')
    time.sleep(1)
    ts.fetch_top('dsj')
    time.sleep(1)
    ts.fetch_top('dm')
    time.sleep(1)
    ts.fetch_top('zy')

