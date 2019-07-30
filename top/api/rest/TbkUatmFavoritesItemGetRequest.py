from top.api.base import RestApi


class TbkUatmFavoritesItemGetRequest(RestApi):
    def __init__(self, adzone_id, domain='gw.api.taobao.com', port=80):
        RestApi.__init__(self, domain, port)
        self.page_no = 1
        self.page_size = 20
        self.fields = "num_iid,title,pict_url,small_images,reserve_price,zk_final_price," \
                      "user_type,provcity,item_url,seller_id,volume,nick,shop_title,zk_final_price_wap," \
                      "tk_rate,status,type,click_url"
        self.adzone_id = adzone_id

    def getapiname(self):
        return 'taobao.tbk.uatm.favorites.item.get'




