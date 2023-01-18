from sqlalchemy import create_engine, Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Numeric

from scrapy.utils.project import get_project_settings

settings = get_project_settings()
Base = declarative_base()


def db_connect():
    return create_engine(url='postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}'.format(
        user=settings.get('PG_USER'),
        password=settings.get('PG_PASSWORD'),
        host=settings.get('PG_HOST'),
        port=settings.get('PG_PORT'),
        name=settings.get('PG_DATABASE')
        )
    )


def create_table(engine):
    Base.metadata.create_all(engine)


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String(512), unique=True, nullable=False)

    energy = Column(Numeric(precision=5, scale=2, asdecimal=True))
    proteins = Column(Numeric(precision=5, scale=2, asdecimal=True))
    carbohydrates_total = Column(Numeric(precision=5, scale=2, asdecimal=True))
    carbohydrates_sugar = Column(Numeric(precision=5, scale=2, asdecimal=True))
    fats_total = Column(Numeric(precision=5, scale=2, asdecimal=True))
    fats_saturated = Column(Numeric(precision=5, scale=2, asdecimal=True))
    fats_trans = Column(Numeric(precision=5, scale=2, asdecimal=True))
    fats_monounsaturated = Column(Numeric(precision=5, scale=2, asdecimal=True))
    fats_polyunsaturated = Column(Numeric(precision=5, scale=2, asdecimal=True))
    fats_cholesterol = Column(Numeric(precision=5, scale=2, asdecimal=True))
    fibers = Column(Numeric(precision=5, scale=2, asdecimal=True))
    salt = Column(Numeric(precision=5, scale=2, asdecimal=True))
    water = Column(Numeric(precision=5, scale=2, asdecimal=True))
    calcium = Column(Numeric(precision=5, scale=2, asdecimal=True))
    phe = Column(Numeric(precision=5, scale=2, asdecimal=True))

    category_id = Column(Integer, ForeignKey('category.id'))

    def __str__(self):
        return f'<Product: {self.name}>'


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), unique=True, nullable=False)

    group_id = Column(Integer, ForeignKey('category_group.id'))
    products = relationship('Product', backref='category')

    def __str__(self):
        return f'<Category: {self.name}>'


class CategoryGroup(Base):
    __tablename__ = 'category_group'

    id = Column(Integer, primary_key=True)
    name = Column(String(256), unique=True, nullable=False)

    categories = relationship('Category', backref='group')

    def __str__(self):
        return f'<CategoryGroup: {self.name}>'
