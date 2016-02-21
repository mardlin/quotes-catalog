from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

from pprint import pprint

engine = create_engine('sqlite:///sporty-catalog.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

categories=session.query(Category)
items=session.query(Item)


def printq(query, prop):
    for q in query:
        print getattr(q,prop)

def pprintall(query):
	for q in query:
		pprint(vars(q))

def simprint(query):
	for q in query:
		r=""
		for key in q.__dict__:
			r+= str(getattr(q,key)) +"|"
		print r + "\n"
		d=""
	for key in query[0].__dict__:
		d+=key+"|"
	print d