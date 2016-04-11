from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
from sqlalchemy.ext.hybrid import hybrid_property

from pprint import pprint

engine = create_engine('sqlite:///quotes.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


users = session.query(User).all()
categories = session.query(Category).all()
items = session.query(Item).all()


def printq(query, prop):
    for q in query:
        print getattr(q, prop)


def pprintall(query):
    for q in query:
        pprint(vars(q))


def simprint(query):
    for q in query:
        r = ""
        for key in q.__dict__:
            r += str(getattr(q, key)) + "|"
        print r + "\n"
        d = ""
    for key in query[0].__dict__:
        d += key+"|"
    print d
