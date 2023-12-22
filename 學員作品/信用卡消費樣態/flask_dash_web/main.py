from flask import Flask, redirect
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from dash_file.dash_app import dash
from dash_file.dash_app1 import dash1
from dash_file.dash_app2 import dash2
from dash_file.dash_app3 import dash3
from dash_file.dash_app4 import dash4
from dash_file.dash_index import dash_index


app = Flask(__name__)
application = DispatcherMiddleware(
    app,
    {"/dash/app": dash.server,
     "/dash/app1": dash1.server,
     "/dash/app2": dash2.server,
     "/dash/app3": dash3.server,
     "/dash/app4": dash4.server,
     "/dash/index": dash_index.server
    },
)

@app.route("/")
def index():
    return redirect('/dash/index')

if __name__ == "__main__":
    run_simple("localhost", 8080, application,use_debugger=True,use_reloader=True)