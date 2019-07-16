# -*- coding:utf-8 -*-
from app.config import Config
from pymongo import MongoClient, ASCENDING, DESCENDING


def app_mongo(func):
    def wrapper(*args, **kwargs):
        conn = MongoClient(host=Config.MD_HOST, port=Config.MD_PORT)
        try:
            mongo_db = conn[Config.MD_DATABASE]
            mongo_db.authenticate(Config.MD_USER, Config.MD_PWD)
            return func(mongo_db, *args, **kwargs)
        finally:
            conn.close()
    return wrapper


class Mongo:
    # tv_areas = Mongo.get_col('t_tv').aggregate([
    #     {'$match': {'tv_type': {'$in': tv_type}}},
    #     {'$group': {'_id': '$img_save', 'tv_areas': {'$addToSet': '$tv_area'}}}
    # ])

    @classmethod
    def __get_sort(cls, s):
        if s == 'asc':    # 升序
            return ASCENDING
        elif s == 'desc':    # 降序
            return DESCENDING

    @staticmethod
    @app_mongo
    def get_col(mongo_db, col):
        return mongo_db[col]

    @staticmethod
    @app_mongo
    def insert_one(mongo_db, col, data):
        """
        新增一条记录
        :param mongo_db:
        :param col: 集合
        :param data: 数据
        :return:
        """
        assert data, 'data not is null'
        assert isinstance(data, dict), 'data应为dict格式，如：{"id":111, "name":"zhangsan"}'
        ret = mongo_db[col].insert_one(data)
        return ret.inserted_id

    @staticmethod
    @app_mongo
    def insert_many(mongo_db, col, data):
        """
        新增多条记录
        :param mongo_db:
        :param col: 集合
        :param data: 数据
        :return:
        """
        assert data, 'data不为null'
        assert isinstance(data, (list, dict)), 'data应为list或dict格式，如：[{},{},{}...]'
        ret = mongo_db[col].insert_many(data)
        return ret.inserted_ids

    @staticmethod
    @app_mongo
    def update(mongo_db, col, data):
        """
        更新数据
        :param mongo_db:
        :param col: 集合
        :param data:
        :return:
        """
        assert data, 'data不为null'
        assert isinstance(data, dict), 'data应为dict格式，如：{"id":111}'
        # data_filter: 过滤条件；data_revised: set设置
        data_filter, data_revised = {}, {}
        for key in data.keys():
            data_filter[key] = data[key][0]
            data_revised[key] = data[key][1]
        return mongo_db[col].update_many(data_filter, {"$set": data_revised}).modified_count

    @staticmethod
    @app_mongo
    def find_one(mongo_db, col, condition):
        """
        查询一个
        :param mongo_db:
        :param col: 集合
        :param condition: 查询条件
        :return:
        """
        condition = condition if condition else {}
        assert isinstance(condition, dict), 'condition应为dict格式，如：{"id":111}'
        return mongo_db[col].find_one(condition)

    @staticmethod
    @app_mongo
    def find_page(mongo_db, col, condition, page_no):
        skip = (int(page_no)-1)*30
        return Mongo.find(mongo_db, col, condition, skip=skip, limit=30)

    @staticmethod
    @app_mongo
    def find(mongo_db, col, condition, sort_fields=[('update_time', 'desc')], skip=None, limit=None):
        """
        查询多个
        :param mongo_db:
        :param col: 集合
        :param condition: 查询条件
        :param sort_fields: 排序和索引
        :param skip: 偏移
        :param limit: limit
        :return:
        """
        condition = condition if condition else {}
        sort_fields = sort_fields if sort_fields else ()
        assert isinstance(condition, dict), 'condition应为dict格式，如:{"id":1}'
        assert isinstance(sort_fields, list), 'sort_feilds应为tuple格式，如：[(id,asc/desc),(name,asc/desc)]'
        sort_list = []
        # 排序处理，将asc替换为mongo里的1，desc --> -1
        if sort_fields and len(sort_fields) > 0:
            for s in sort_fields:
                sort_list.append((s[0], Mongo.__get_sort(s[1])))
        # 如果有排序存在设置索引
        if sort_list and len(sort_list) > 0:
            mongo_db[col].create_index(sort_list)

        # 查询
        cursor = mongo_db[col].find(condition, {'_id': 0})
        # 设置排序
        if sort_list and len(sort_list) > 0:
            cursor.sort(sort_list)
        # 设置偏移
        if skip:
            cursor.skip(skip)
        # 设置limit
        if limit:
            cursor.limit(limit)
        # 返回list
        return [c for c in cursor] if cursor and cursor.count() > 0 else []

    @staticmethod
    @app_mongo
    def delete(mongo_db, col, condition):
        """
        删除数据
        :param mongo_db:
        :param col: 集合
        :param condition: 删除条件
        :return:
        """
        assert isinstance(condition, dict), 'condition应为dict格式，如：{"id":1}'
        return mongo_db[col].delete_many(filter=condition).deleted_count

    @staticmethod
    @app_mongo
    def count(mongo_db, col, condition):
        """
        统计个数
        :param mongo_db:
        :param col: 集合
        :param condition: 查询条件
        :return:
        """
        condition = condition if condition else {}
        return mongo_db[col].count_documents(condition)


if __name__ == '__main__':
    db = Mongo()
    # db.delete('t_tv', {})
    # db.delete('t_tv_urls', {})
    # print(db.count('t_tv', {}))
    # print(db.count('t_tv_urls', {}))
    print(db.find('t_tv', {}, [('update_time', 'desc')], 0, 1).next())


