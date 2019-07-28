# -*- coding:utf-8 -*-
import top.api
from app.config import Config


class TBApi:

    @staticmethod
    def get_tb_goods():
        goods = ''
        try:
            # 获取商品库列表
            favorites_id = ''
            req = top.api.TbkUatmFavoritesGetRequest()
            req.set_app_info(top.appinfo(Config.TB_AK, Config.TB_AS))
            resp = dict(req.getResponse())
            if resp:
                favorites = resp.get('tbk_uatm_favorites_get_response')\
                    .get('results').get('tbk_favorites')
                favorites_id = dict(list(favorites)[0]).get('favorites_id')
            # 获取所有商品
            if favorites_id:
                d_req = top.api.TbkUatmFavoritesItemGetRequest(Config.TB_AD_ZONE_ID)
                d_req.set_app_info(top.appinfo(Config.TB_AK, Config.TB_AS))
                d_req.favorites_id = favorites_id
                d_resp = dict(d_req.getResponse())
                if d_resp:
                    goods = d_resp.get('tbk_uatm_favorites_item_get_response')\
                        .get('results').get('uatm_tbk_item')
            return goods if goods else None
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(repr(e))




