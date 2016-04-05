import os
import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()

class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True)
	name = Column(String(100))
	email = Column(String(100))	
	picture = Column(String(250), nullable=False)

	# Set up a one-many (user-restaurant) relationship
	category = relationship("Category", back_populates="user")
	item = relationship("Item", back_populates="user")

	@property
	def serialize(self):
		"""Return object data in easily serializeable format"""
		return {
			'name'         : self.name,
			'id'           : self.id,
			'email'        : self.email,
			'picture'      : self.picture,
	   }


class Category(Base):
	__tablename__ = 'category'

	id = Column(Integer, primary_key=True)
	name = Column(String(50))
	items = relationship("Item", back_populates='category')

	user_id = Column(Integer, ForeignKey("user.id"))
	user = relationship("User")

	@property
	def serialize(self):
		# create a list of serialized items in the category
		items_list = []
		for i in self.items:
			items_list.append( i.serialize )
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
	
	# Configured so that adding a category_id will also create the relationship
	category_id = Column(Integer, ForeignKey('category.id'))
	category = relationship("Category", back_populates='items')

	user_id = Column(Integer, ForeignKey("user.id"))
	user = relationship("User")

	@property
	def serialize(self):
		return {
			'id' : self.id,
			'name': self.name,
			'description': self.description,
			'image': self.image,
			'date_created': self.date_created
		}


engine = create_engine('sqlite:///sporty-catalog3.db')
Base.metadata.create_all(engine)