import json

import scrapy

from ..items import ProductItem
from ..itemloaders import ProductItemLoader


class ProductsSpider(scrapy.Spider):
    name = 'products'
    allowed_domains = ['tablycjakalorijnosti.com.ua']
    custom_settings = {'LOG_LEVEL': 'DEBUG', 'COMPRESSION_ENABLED': False}
    state = {'item_count': 0, 'page_num': 0, 'number_of_products': 0}

    main_page_url = 'https://www.tablycjakalorijnosti.com.ua'
    api_url = 'https://www.tablycjakalorijnosti.com.ua/foodstuff/filter-list?format=json&page={page}&limit={limit}'
    product_url = 'https://www.tablycjakalorijnosti.com.ua/stravy/'

    def start_requests(self):
        yield scrapy.Request(url='https://www.tablycjakalorijnosti.com.ua/tablytsya-yizhyi',
                             callback=self.parse_first_page)

    def parse_first_page(self, response):
        number_of_products = int(response.css('span[ng-if="foodstuff==null"]::text').get().strip())
        self.state['number_of_products'] = number_of_products

        for product in response.css('table a.p-link'):
            product_url = self.main_page_url + product.css('::attr(href)').get()
            yield scrapy.Request(product_url, callback=self.parse_product_from_main)

        while self.state['page_num'] < 200:
            self.state['page_num'] += 1
            yield scrapy.Request(url=self.api_url.format(page=self.state['page_num'], limit=50),
                                 callback=self.parse_json)

    def parse_product_from_main(self, response):
        """Getting the product values from FIRST PAGE"""
        item = ProductItemLoader(ProductItem(), response=response)
        self.state['item_count'] += 1
        print('Getting item N ', self.state['item_count'])

        categories = response.css('div[typeof="BreadcrumbList"]').css('div > a > span[property="name"]::text').getall()
        data_string = response.css('script[type="application/ld+json"]')[1].css('::text').get().strip()
        data_dict = eval(data_string)
        values = self.list_to_dict(data_dict['keywords'])

        item.add_value('name', data_dict['name'])
        item.add_value('category', categories[-1])
        item.add_value('group', categories[-2])
        item.add_value('energy', values.get('Енергія', None))
        item.add_value('proteins', values.get('Білки', None))
        item.add_value('carbohydrates_total', values.get('Вуглеводи', None))
        item.add_value('carbohydrates_sugar', values.get('Цукор', None))
        item.add_value('fats_total', values.get('Жири', None))
        item.add_value('fats_saturated',  values.get('Насичені жирні кислоти', None))
        item.add_xpath('fats_trans', '//td/div[contains(text(), "Трансжирні")]/../following-sibling::td//span/text()')
        item.add_value('fats_monounsaturated', values.get('Мононенасичені', None))
        item.add_value('fats_polyunsaturated', values.get('Поліненасичені', None))
        item.add_xpath('fats_cholesterol',
                       '//td/div[contains(text(), "Холостерин")]/../following-sibling::td//span/text()')
        item.add_value('fibers', values.get('Волокна', None))
        item.add_value('salt', values.get('Сіль', None))
        item.add_xpath('water', '//td/div[contains(text(), "Вода")]/../following-sibling::td/div/span/text()')
        item.add_value('calcium', values.get('Кальцій'))
        item.add_xpath('phe', '//td/div[contains(text(), "PHE")]/../following-sibling::td/div/span/text()')

        return item.load_item()

    def parse_json(self, response):
        data = json.loads(response.text)
        products: list = data['data']
        for product in products:
            product_url = self.product_url + product.get('url')
            yield scrapy.Request(url=product_url, callback=self.parse_product, cb_kwargs={'product': product})

    def parse_product(self, response, product):
        """Get categories and json info to item"""
        item = ProductItemLoader(ProductItem(), response=response)

        self.state['item_count'] += 1
        print('Getting item N ', self.state['item_count'])

        categories = response.css('div[typeof="BreadcrumbList"]').css('div > a > span[property="name"]::text').getall()

        item.add_value('name', product.get('title'))
        item.add_value('category', categories[-1])
        item.add_value('group', categories[-2])
        item.add_value('energy', product.get('energy'))
        item.add_value('proteins', product.get('protein'))
        item.add_value('carbohydrates_total', product.get('carbohydrate'))
        item.add_value('carbohydrates_sugar', product.get('sugar'))
        item.add_value('fats_total', product.get('fat'))
        item.add_value('fats_saturated',  product.get('saturatedFattyAcid'))
        item.add_value('fats_trans', product.get('transFattyAcid'))
        item.add_value('fats_monounsaturated', product.get('monoSaturated'))
        item.add_value('fats_polyunsaturated', product.get('polySaturated'))
        item.add_value('fats_cholesterol', product.get('cholesterol'))
        item.add_value('fibers', product.get('fiber'))
        item.add_value('salt', product.get('salt'))
        item.add_value('water', product.get('water'))
        item.add_value('calcium', product.get('calcium'))
        item.add_value('phe', product.get('phe'))

        return item.load_item()

    @staticmethod
    def list_to_dict(lst: list) -> dict:
        """Converting list of values to dict"""
        output = {}
        for item in lst:
            key, value = item.split(' : ')
            output[key] = value
        return output
