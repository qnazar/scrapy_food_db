from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose

from utils import extract_numeric_value


class ProductItemLoader(ItemLoader):
    default_input_processor = MapCompose(extract_numeric_value)
    default_output_processor = TakeFirst()

    name_in = MapCompose(lambda n: n.strip().capitalize())

    category_in = MapCompose(lambda c: c.strip().strip('"').capitalize())
    group_in = MapCompose(lambda g: g.strip().strip('"').capitalize())
