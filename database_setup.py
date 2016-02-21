import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()

class Category(Base):
	__tablename__ = 'category'

	id = Column(Integer, primary_key=True)
	name = Column(String(50))
	
	item = relationship("Item", back_populates='category')

	# @property
	# def serialize(self):
	# 	return {}

class Item(Base):
	__tablename__ = 'item'

	id = Column(Integer, primary_key=True)
	name = Column(String(50))
	image = Column(String(200))
	
	category_id = Column(Integer, ForeignKey('category.id'))
	category = relationship("Category", back_populates='item')

	# @property
	# def serialize(self):
	# 	return {}


engine = create_engine('sqlite:///sporty-catalog.db')
Base.metadata.create_all(engine)