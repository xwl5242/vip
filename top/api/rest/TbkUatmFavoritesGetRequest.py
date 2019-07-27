from top.api.base import RestApi


class TbkUatmFavoritesGetRequest(RestApi):
    def __init__(self, domain='gw.api.taobao.com', port=80):
        RestApi.__init__(self, domain, port)
        self.page_no = 1
        self.page_size = 20
        self.fields = "favorites_title,favorites_id,type"
        self.type = 1

    def getapiname(self):
        return 'taobao.tbk.uatm.favorites.get'




