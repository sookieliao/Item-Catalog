import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

################################


class Category(Base):
    __tablename__ = 'category'
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)

class Brand(Base):
    __tablename__ = 'brand'
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)

class User(Base):
    __tablename__ = 'user'
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    account_name = Column(String(20), nullable = False)
    password = Column(String(20), nullable = False)

class Camera(Base):
    __tablename__ = 'camera'
    name = Column(String(100), nullable = False)
    brand = relationship(Brand)
    brand_id = Column(Integer, ForeignKey('brand.id'))
    description = Column(String(250))
    price = Column(String(8))
    condition = Column(String(15))
    id = Column(Integer, primary_key = True)
    category = relationship(Category)
    category_id = Column(Integer, ForeignKey('category.id'))
    user = relationship(User)
    user_id = Column(Integer, ForeignKey('user.id'))


    @property
    def serialize(self):
        #Returns object data in easily serializable format for JSON
        return {
            'name'  : self.name,
            'id'    : self.id,
            'category_id' : self.category_id,
            'brand_id': self.brand_id,
            'description' : self.description,
            'price' : self.price,
            'user_id':self.user_id

        }


################################

engine = create_engine('sqlite:///cameras.db')

Base.metadata.create_all(engine)