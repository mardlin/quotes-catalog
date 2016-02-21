from flask import Flask
app = Flask(__name__)

@app.route('/')
@app.route('/catalog')
def listCatalog():
	"""Page to display categories and recently added (latest) items"""
	
	return "Page to display categories and recently added (latest) items"
	
## This statement detects when the script has been run from the interpreter
if __name__ == "__main__":
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)