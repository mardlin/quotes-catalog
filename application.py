from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
## consider redirecting this to /catalog to avoid confusion
@app.route('/catalog')
def showCatalog():
	"""Page to display categories and recently added (latest) items"""
	
	return "Page to display categories and recently added (latest) items"

@app.route('/catalog/<category_name>')
@app.route('/catalog/<category_name>/items')
def showCategory(category_name):
	"""Page to display items in a given category"""

	return "Page to display items in the {0} category".format(category_name)

@app.route('/catalog/<category_name>/<item_name>')
def showItem(category_name, item_name):
	"""Page to display the description and image of an item"""

	return """Page to display the description and image of the '{0}' name in the 
	'{1}' category.""".format(item_name,category_name)

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






## This statement detects when the script has been run from the interpreter
if __name__ == "__main__":
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)