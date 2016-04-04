from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

from pprint import pprint

engine = create_engine('sqlite:///sporty-catalog2.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

categories = [
	[ 
		Category(name='Basketball'), 
	 	[
	 		Item(name='b-ball', description = "This is the b-ball you need!"), 
	 		Item(name='shoes', description = "You are nothing without these shoes! "), 
	 		Item(name='water bottle', description = "How will you survived without water??!")
 		]
	],
	[
		Category(name='Tennis'), 
	 	[
	 		Item(name='Racquet', description = "The only racquet good enough"), 
	 		Item(name='tennis ball', description = "You'll have a BALL playing TENNIS!")
	 	]
	], 
	[
		Category(name='Running'), 
			[
				Item(name='running shoes', description = "Run, don't walk to buy these shoes!"), 
				Item(name='head band', description = "This is the band your head deserves"), 
				Item(name='water belt', description = "Be like the camel")
			]
	]
]

for category in categories:
	current_category = category[0]
	session.add(current_category)
	for item in category[1]:
		item.category= current_category
		session.add(item)
	session.commit()


