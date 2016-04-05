from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User

from pprint import pprint

engine = create_engine('sqlite:///sporty-catalog3.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

# Create dummy user
User1 = User(name="Bort", email="bort@email.com",
             picture='https://placeholder.it/100/100')
session.add(User1)
session.commit()

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
		item.category = current_category
		item.user = User1
		session.add(item)
	session.commit()


