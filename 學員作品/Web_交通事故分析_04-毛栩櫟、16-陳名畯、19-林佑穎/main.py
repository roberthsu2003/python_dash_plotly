from flask import Flask,render_template,request
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from dashboard.dashboard2 import app1



app = Flask(__name__)
application = DispatcherMiddleware(app,{
    "/dashboard/dashboard2":app1.server
})

@app.route("/")
def index():
    return render_template("index.html.jinja")

@app.route("/index1")
def index1():
    return render_template('index1.html.jinja')    
    
if __name__ =="__main__":
    run_simple("localhost",8080,application,use_debugger=True,use_reloader=True)