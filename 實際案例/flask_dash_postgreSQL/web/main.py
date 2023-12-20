from flask import Flask,render_template,session
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from dash_file.dash_app1 import dash1
from dash_file.dash_app2 import dash2
from auth.register import register_blue
import secrets

app = Flask(__name__)
app.register_blueprint(register_blue)
app.config['SECRET_KEY'] = secrets.token_hex(16)

application = DispatcherMiddleware(
    app,
    {"/dash/app1": dash1.server,
     "/dash/app2": dash2.server}
)

@app.route("/")
def index():
    if 'username' in session:
        user = session['username']
    else:
        user = None
    return render_template("index.html",username=user)

if __name__ == "__main__":
    run_simple("localhost", 8080, application,use_debugger=True,use_reloader=True)