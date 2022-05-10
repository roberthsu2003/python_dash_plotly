
## Dash and Flask 整合

```python
from dash import Dash,html
from flask import Flask

server = Flask(__name__)


@server.route("/")
def home():
    return "Hello, Flask!"


app = Dash(server=server, routes_pathname_prefix="/dash/")

app.layout = html.Div("This is the Dash app.")

if __name__ == "__main__":
    app.run_server(debug=True)
```

```python
import dash
import dash_html_components as html
import flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

server = flask.Flask(__name__)


@server.route("/")
def home():
    return "Hello, Flask!"


app1 = dash.Dash(requests_pathname_prefix="/app1/")
app1.layout = html.Div("Hello, Dash app 1!")

app2 = dash.Dash(requests_pathname_prefix="/app2/")
app2.layout = html.Div("Hello, Dash app 2!")

application = DispatcherMiddleware(
    server,
    {"/app1": app1.server, "/app2": app2.server},
)

if __name__ == "__main__":
    run_simple("localhost", 8050, application)
```

