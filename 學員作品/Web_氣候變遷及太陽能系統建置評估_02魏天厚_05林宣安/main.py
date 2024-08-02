from flask import Flask, render_template
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from dashboard.board1 import app1
from dashboard.board2 import app2
from dashboard.board3 import app3


app = Flask(__name__)

# 使用 DispatcherMiddleware 將多個 Dash 應用與 Flask 應用結合
application = DispatcherMiddleware(app, {
    "/dashboard/app1": app1.server,
    "/dashboard/app2": app2.server,
    "/dashboard/app3": app3.server,
})

@app.route("/")
def index():
    return render_template("base.html.jinja")

@app.route("/dashboard/app2")
def dashboard_app2():
    return render_template("index.html.jinja")

@app.route("/dashboard/app3")
def dashboard_app3():
    return render_template("index1.html.jinja")

if __name__ == '__main__':
    run_simple("localhost", 8056, application, use_debugger=True, use_reloader=True)
