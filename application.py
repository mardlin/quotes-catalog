from flask import Flask, render_template, request, redirect, url_for, jsonify 
app = Flask(__name__)

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

engine = create_engine('sqlite:///sporty-catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
## consider redirecting this to /catalog to avoid confusion
@app.route('/catalog')
def showCatalog():
	"""Page to display categories and recently added (latest) items"""

	categories = session.query(Category).all()
	latest_items = session.query(Item).order_by(desc(Item.date_created)).limit(3)

	return render_template('showCatalog.html', categories=categories, 
		latest_items=latest_items)

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


@app.route('/catalog/<category_name>/<item_name>')
def showItem(category_name, item_name):
	"""Page to display the description and image of an item"""

	category_items = (
		session.query(Item)
		.filter( Item.category.has(name=category_name) )
	)
	# use .first() to get an empty list if there is no match
	item = category_items.filter_by(name=item_name).first()
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


@app.route('/catalog/<category_name>/<item_name>/edit')
def editItem(category_name, item_name):
	"""Page to display for editing an item"""

	return """Page for editing the '{0}' name in the 
	'{1}' category.""".format(item_name,category_name)


@app.route('/catalog/<category_name>/<item_name>/delete')
def deleteItem(category_name, item_name):
	"""Page to display for deleting an item"""

	return """Page for deleting the '{0}' name in the 
	'{1}' category.""".format(item_name,category_name)


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
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)