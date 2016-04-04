from flask import Flask
app = Flask(__name__)

import catalog.views
import catalog.auth_views