from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
app = Flask(__name__)

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

engine = create_engine('sqlite:///sporty-catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


## consider redirecting this to /catalog to avoid confusion
def showCheck():
	"""test page"""

	# categories = session.query(Category).all()
	# latest_items = session.query(Item).order_by(desc(Item.date_created)).limit(3)

	return "Hello girls"