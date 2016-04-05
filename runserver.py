from flask import Flask
from werkzeug.serving import run_simple

from catalog import app
app.debug = True
app.secret_key = 'super_secret_key'
app.console_path='/console'

if __name__ == '__main__':
    run_simple('0.0.0.0', 5000, app,
               use_reloader=True, use_debugger=True, use_evalex=True)


# from catalog import app
# from werkzeug.serving import run_simple


# if __name__ == '__main__':
# 	app.secret_key = 'super_secret_key'
#   	# app.debug = True
#   	# app.run(host='0.0.0.0',port=5000)
#   	run_simple('0.0.0.0', 5000, app,
#                use_reloader=True, use_debugger=True)
#                # , use_evalex=True)