from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

from pprint import pprint

engine = create_engine('sqlite:///sporty-catalog.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

categories = [
	[Category(name='Basketball'), [Item(name='b-ball'), Item(name='shoes'), Item(name='water bottle')]],
	[Category(name='Tennis'), [Item(name='Racquet'), Item(name='tennis ball')]], 
	[Category(name='Running'), [Item(name='running shoes'), Item(name='head band'), Item(name=
		'water belt')]]
	]

for category in categories:
	current_category = category[0]
	session.add(current_category)
	for item in category[1]:
		item.category= current_category
		session.add(item)
	session.commit()


