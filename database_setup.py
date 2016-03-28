import os
import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()

class Category(Base):
	__tablename__ = 'category'

	id = Column(Integer, primary_key=True)
	name = Column(String(50))
	items = relationship("Item", back_populates='category')

	@property
	def serialize(self):
		# create a list of serialized items in the category
		items_list = []
		for i in self.items:
			items_list.append( i.serialize )
		# this is a dict
		serial = {
			'id' : self.id,
			'name' : self.name,
			'items' : items_list
		}
		return serial

class Item(Base):
	__tablename__ = 'item'

	id = Column(Integer, primary_key=True)
	name = Column(String(50))
	description = Column(String(250))
	image = Column(String(200))
	date_created = Column(DateTime, default=datetime.datetime.now)
	
	category_id = Column(Integer, ForeignKey('category.id'))
	category = relationship("Category", back_populates='items')

	@property
	def serialize(self):
		return {
			'id' : self.id,
			'name': self.name,
			'description': self.description,
			'image': self.image,
			'date_created': self.date_created
		}


engine = create_engine('sqlite:///sporty-catalog.db')
Base.metadata.create_all(engine)