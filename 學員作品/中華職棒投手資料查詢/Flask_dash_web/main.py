from flask import Flask,render_template,url_for
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from dash_file.dash_app1 import dash1
from dash_file.dash_app2 import dash2
from dash_file.dash_app3 import dash3
from dash_file.dash_app4 import dash4
from dash_file.dash_app5 import dash5
from dash_file.dash_app6 import dash6


application = DispatcherMiddleware(
    dash1.server,
    {
    "/dash/app1": dash1.server,
    '/dash/rakuten':dash2.server,
    '/dash/brothers':dash3.server,
    '/dash/lions':dash4.server,
    '/dash/fubon':dash5.server,
    '/dash/dragons':dash6.server,
    }
)

if __name__ == "__main__":
    run_simple("localhost", 8080, application, use_debugger=True, use_reloader=True)