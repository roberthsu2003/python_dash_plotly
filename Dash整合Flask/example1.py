#from dash import Dash,html
from flask import Flask

server = Flask(__name__)


@server.route("/")
def home():
    return "Hello, Flask!"


#app = Dash(server=server, routes_pathname_prefix="/dash/")

#app.layout = html.Div("This is the Dash app.")

if __name__ == "__main__":
    server.run_server(debug=True)