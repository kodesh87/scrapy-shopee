import scrapy
import json
import urllib
import math

class ProductsSpider(scrapy.Spider):
    name = 'products'
    allowed_domains = ['shopee.co.id']
    start_urls = ['https://shopee.co.id/api/v4/search/search_items?by=sales&categoryids=11043461&keyword=almond&limit=60&newest=0&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&skip_autocorrect=1&version=2']

    def parse(self, response):
        resp = json.loads(response.body)
        items = resp.get('items')
        
        for item in items:
            data = item.get('item_basic')
            yield {
                'name' : data.get('name'),
                'price' : data.get('price') / 100000,
                'price_min' : data.get('price_min') / 100000,
                'price_max' : data.get('price_max') / 100000,
                'stock' : data.get('stock'),
                'sold' : data.get('sold'),
                'historical_sold' : data.get('historical_sold'),
                'liked_count' : data.get('liked_count'),
                'cmt_count' : data.get('cmt_count'),
                'itemid' : data.get('itemid'),
                'shopid' : data.get('shopid'),
                'link' : 'https://shopee.co.id/' + str(data.get('name')).replace(' ', '-').replace('/', '-') + '-i.' + str(data.get('shopid')) + '.' + str(data.get('itemid'))
            }
        newest = int((urllib.parse.parse_qs(urllib.parse.urlsplit(response.request.url).query)).get('newest')[0]) + 60
        total_count = resp.get('total_count')
        print('newest = ' + str(newest) + ', total_count = ' + str(total_count) + '\n')
        if newest < total_count:
            yield scrapy.Request(
                url = 'https://shopee.co.id/api/v4/search/search_items?by=sales&categoryids=11043461&keyword=almond&limit=60&newest=' + str(newest) + '&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&skip_autocorrect=1&version=2',
                callback = self.parse
            )