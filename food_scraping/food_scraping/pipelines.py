from sqlalchemy.orm import sessionmaker, Session
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

from .models import db_connect, create_table, Product, Category, CategoryGroup


class SaveToPostgresPipeline:

    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session: Session = self.Session()
        adapter = ItemAdapter(item)
        product = Product()
        category = Category()
        group = CategoryGroup()

        group.name = adapter['group']

        category.name = adapter['category']

        product.name = adapter.get('name')
        product.energy = adapter.get('energy')
        product.proteins = adapter.get('proteins')
        product.carbohydrates_total = adapter.get('carbohydrates_total')
        product.carbohydrates_sugar = adapter.get('carbohydrates_sugar')
        product.fats_total = adapter.get('fats_total')
        product.fats_saturated = adapter.get('fats_saturated')
        product.fats_trans = adapter.get('fats_trans')
        product.fats_monounsaturated = adapter.get('fats_monounsaturated')
        product.fats_polyunsaturated = adapter.get('fats_polyunsaturated')
        product.fats_cholesterol = adapter.get('fats_cholesterol')
        product.fibers = adapter.get('fibers')
        product.salt = adapter.get('salt')
        product.water = adapter.get('water')
        product.calcium = adapter.get('calcium')
        product.phe = adapter.get('phe')

        exist_category = session.query(Category).filter_by(name=category.name).first()
        if exist_category:
            product.category = exist_category
        else:
            product.category = category

            exist_group = session.query(CategoryGroup).filter_by(name=group.name).first()
            if exist_group:
                category.group = exist_group
            else:
                category.group = group

        try:
            session.add(product)
            session.commit()
        except Exception as ex:
            print(ex)
            session.rollback()
            raise DropItem()
        finally:
            session.close()

        return item
