from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
app = Flask(__name__)

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

engine = create_engine('sqlite:///sporty-catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

from auth_routes import *

@app.route('/')
## consider redirecting this to /catalog to avoid confusion
@app.route('/catalog')
def showCatalog():
	"""Page to display categories and recently added (latest) items"""

	categories = session.query(Category).all()
	latest_items = session.query(Item).order_by(desc(Item.date_created)).limit(3)

	return render_template('showCatalog.html', categories=categories, 
		latest_items=latest_items)

@app.route('/check')
def check():
	showCheck()
	# return "hello!"

@app.route('/catalog.json')
def showCatalogJSON():
	"""Page to display categories and recently added (latest) items"""

	categories = session.query(Category).all()
	category_list = []
	for c in categories:
		category_list.append(c.serialize)
	return jsonify(category = category_list)

@app.route('/catalog/<category_name>')
@app.route('/catalog/<category_name>/items')
def showCategory(category_name):
	"""Page to display items in a given category"""

	items = session.query(Item).filter(Item.category.has(name = category_name)).all()
	return	render_template('showCategory.html', category_name=category_name,
			items=items)

@app.route('/catalog/<category_name>.json')
def showCategoryJSON(category_name):
	"""Page to display items in a given category"""

	category = session.query(Category).filter_by(name = category_name).first()

	return	jsonify(category = category.serialize)


# helper functions
def getItem(category_name, item_name):
	category_items = (
		session.query(Item)
		.filter( Item.category.has(name=category_name) )
	)
	# use .first() to get an empty list if there is no match
	item = category_items.filter_by(name=item_name).first()
	return item


@app.route('/catalog/<category_name>/<item_name>')
def showItem(category_name, item_name):
	"""Page to display the description and image of an item"""

	item = getItem(category_name=category_name, item_name=item_name)
	
	return render_template('showItem.html', category_name=category_name,
			item=item, item_name=item_name)

@app.route('/catalog/<category_name>/<item_name>.json')
def showItemJSON(category_name, item_name):
	"""Page to display the description and image of an item"""

	category_items = (
		session.query(Item)
		.filter( Item.category.has(name=category_name) )
	)
	# use .first() to get an empty list if there is no match
	item = category_items.filter_by(name=item_name).first()

	if item:
		return jsonify(item = item.serialize)
	else: 
	    return 'Item does not exist', 404


@app.route('/catalog/<category_name>/add', methods=['GET','POST'])
def addItem(category_name):
	"""Page to display for adding an item"""
	
	category = session.query(Category).filter_by(name=category_name).first()
	if request.method == 'POST':
		print request.form
		new_item=Item(category_id=category.id)
		new_item.name = request.form['name']
		new_item.description = request.form['description']
		new_item.image = request.form['image']
		session.add(new_item)
		session.commit()
		flash('"%s" item successfully added to "%s" category' % 
			(new_item.name, category_name))
		return redirect(url_for('showCategory', category_name=category_name))
	else: 	
		return render_template('addItem.html', category_name=category_name)


@app.route('/catalog/<category_name>/<item_name>/edit', methods=['GET', 'POST'])
def editItem(category_name, item_name):
	"""Page to display for editing an item"""
	
	category = session.query(Category).filter_by(name=category_name).first()
	itemToEdit = getItem(category_name=category_name, item_name=item_name)
	if request.method == 'POST':
		itemToEdit.name = request.form['name']
		itemToEdit.description = request.form['description']
		itemToEdit.image = request.form['image']
		session.add(itemToEdit)
		session.commit()
		flash('"%s" item successfully edited in "%s" category' % 
			(itemToEdit.name, category_name))
		return redirect(url_for('showItem', category_name=category_name, item_name=itemToEdit.name ))
	return render_template('editItem.html', category_name=category_name,
				item_name=item_name, item=itemToEdit)

@app.route('/catalog/<category_name>/<item_name>/delete', methods=['GET','POST'])
def deleteItem(category_name, item_name):
	"""Page to display for deleting an item"""

	itemToDelete = getItem(category_name=category_name, item_name=item_name)
	print "item: %s " % itemToDelete
	if request.method == 'POST':
		session.delete(itemToDelete)
		session.commit()
		flash('"%s" item successfully deleted from "%s" category' % 
			(item_name, category_name))
		return redirect(url_for('showCategory', category_name=category_name))
	return render_template('deleteItem.html', category_name=category_name,
			item=itemToDelete, item_name=item_name)


@app.route('/catalog/<category_name>/items.json')
def jsonCategory(category_name):
	"""return data in a json format. It might be better to create these 
	endpoints by extending the pre-existing routes. Fortunately, we only 
	need GET endpoints
	GET: 
	/catalog.json
	/<category_name>/items.json
	/catalog/<category_name>/<item_name>.json
	"""

	return jsonify({
		'page': 'category json endpoint.'
		})


@app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404


## This statement detects when the script has been run from the interpreter
if __name__ == "__main__":
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)