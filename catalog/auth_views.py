from catalog import app
from flask import render_template, request, redirect, url_for
from flask import jsonify, flash, make_response

from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User

# login_session will be a dict for storing a user's session variables
from flask import session as login_session
# Imports for anti-forgergy state tokens
import random, string
# Import for opening client_secrets.json file
import json
# Import requests for http
import requests

# Imports for handling Google OAuth flow
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']

engine = create_engine('sqlite:///sporty-catalog3.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Inject login_session to standard context for templates 
@app.context_processor
def inject_login_session():
	return dict(login_session=login_session)


@app.route('/login')
def showLogin():
	"""Page to display categories and recently added (latest) items"""
		
	state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
	login_session['state'] = state
	print login_session
	# return "The current session state is %s" % login_session['state']
	return render_template('/login.html', STATE=state)

# Define user helper functions step2

def createUser(login_session):
  newUser = User(name = login_session['username'], email = login_session['email'],
    picture = login_session['picture'])
  session.add(newUser)
  session.commit()
  user = session.query(User).filter_by(email=login_session['email']).one()
  return user.id

def getUserInfo(user_id):
  user = session.query(User).get(user_id)
  return user

def getUserID(email):
  try:
    user = session.query(User).filter_by(email=email).one()
    return user.id
  except: 
    return None


# Post only route called by the Google SDK script in the client when
# a user grants permission to our app
@app.route('/gconnect', methods=['POST'])
def gconnect():
	## 1: Verify that the client state matches the state sent by the server
	# to make sure that it is the same client. 
	if request.args.get('state') != login_session['state']:
		# response = make_response(json.dumps('Invalid state parameter'), 401)
		response = make_response('Invalid state parameter', 401)
		response.headers['Content-Type']='text'
		return response
	# Obtain authorization code
	code = request.data

	## 2: Attempt to exchange code with G+ server for an access token
	try: 
		# Get the Access Token
		oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
		oauth_flow.redirect_uri = 'postmessage'
		credentials = oauth_flow.step2_exchange(code)
	except FlowExchangeError:
		response = make_response( 
		json.dumps('Failed to upgrade the authorization code.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response



	## 3: Validate the Access Token 
	# 3.1: Request information about the token from Google
	access_token = credentials.access_token
	r = requests.get('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' 
	% access_token)
	result = r.json()

	# 3.2 Handle error response
	  # If Google returned error in the access token info, abort.  
	if result.get('error') is not None:
		response = make_response(json.dumps(result.get('error')), 500)
		response.headers['Content-Type'] = 'application/json'
		return response

	# 3.3: Verify User
	  # Verify that the access token is for this user by comparing the original
	  # credentials object to the token_info response
	gplus_id = credentials.id_token['sub'] 
	if result['user_id'] != gplus_id:
		response = make_response(json.dumps("This token is for the wrong user"), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# 3.4 Verify App
	# Verify that the access token is valid for this app
	if result['issued_to'] != CLIENT_ID:
		response = make_response(
			json.dumps("Token's client ID does not match app's."), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# 3.5 Verify that user isn't already connected 
	stored_credentials = login_session.get('credentials')
  	stored_gplus_id = login_session.get('gplus_id')
  	if stored_credentials is not None and gplus_id == stored_gplus_id:
		response = make_response(json.dumps('Current user is already connected.'), 200)
		response.headers['Content-Type'] = 'application/json'
		return response

  	# Store the access token in the session for later use.
  	login_session['provider'] = 'google'
  	# login_session['credentials'] = credentials
  	login_session['gplus_id'] = gplus_id

	# Well, OK then, so we've tucked those guys away
	# Now let's get some more info about the user from Google.
	userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
	params = {'access_token':credentials.access_token, 'alt':'json'}
	answer = requests.get(userinfo_url, params=params)

	data = answer.json()

	login_session['email'] = data['email']
	login_session['username'] = data['name']
	login_session['picture'] = data['picture']
  

	# Check to see if user is already in our DB 
	user_id = getUserID(login_session['email'])

	if user_id is None:
	    user_id = createUser(login_session)
  
	login_session['user_id'] = user_id
	user_info = getUserInfo(user_id)

	# prefer local username and picture to g+ data 
	login_session['username'] = user_info.name
	login_session['picture'] = user_info.picture

	output = 'something'
	output += '<h1>Welcome, '
	output += login_session['username']
	output += '!</h1>'
	output += '<img src="'
	output += login_session['picture']
	output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
	flash("you are now logged in as %s" % login_session['username'])
	flash("you are now logged in")
	print "done!"
	return output


@app.route('/logout')
def showLogout():
	# make sure user is actually logged in
	# 

	# Delete login_session variables
	for ls in login_session:
		del ls
	flash('User logged out')
	return redirect(url_for('showCatalog'))






