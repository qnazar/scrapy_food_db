import scrapy


class ProductItem(scrapy.Item):
    name = scrapy.Field()
    energy = scrapy.Field()
    proteins = scrapy.Field()
    carbohydrates_total = scrapy.Field()
    carbohydrates_sugar = scrapy.Field()
    fats_total = scrapy.Field()
    fats_saturated = scrapy.Field()
    fats_trans = scrapy.Field()
    fats_monounsaturated = scrapy.Field()
    fats_polyunsaturated = scrapy.Field()
    fats_cholesterol = scrapy.Field()
    fibers = scrapy.Field()
    salt = scrapy.Field()
    water = scrapy.Field()
    calcium = scrapy.Field()
    phe = scrapy.Field()
    category = scrapy.Field()
    group = scrapy.Field()
