
## Dash and Flask 整合

### requirements.txt

```
requests
dash
pandas
gunicorn
flask
```

### 以dash app 為執行檔的方式

```python
#app.py
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

#### 執行方式

```
$ python app.py
```

---

### 以flask app 為主要執行檔方式1

```python
#app.py
from dash import Dash, html
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
    run_simple("localhost", 8080, application,application,use_debugger=True,use_reloader=True)
```

#### 執行方式1(flask執行,可以debug)

```
$ python app.py
```

#### 執行方式2(gunicorn,本地端執行)

```
gunicorn通常使用的参数如下：
-c CONFIG, --config=CONFIG
# 设定配置文件。
-b BIND, --bind=BIND
# 设定服务需要绑定的端口。建议使用HOST:PORT。
-w WORKERS, --workers=WORKERS
# 设置工作进程数。建议服务器每一个核心可以设置2-4个。
-k MODULE
# 选定异步工作方式使用的模块。
```

```
$ gunicorn -b 127.0.0.1:8080 app:application
```

#### 執行方式2(gunicorn,本地端正式執行執行)

- port:80-需使用sudo

```
$ sudo gunicorn -b 0.0.0.0:80 test2:application
```

### 上傳Render WebService程式碼

- [上傳Render程式碼](https://github.com/roberthsu2003/dash_flask_web)

- [Render_WebService展示-等待30秒](https://dash-flask-web.onrender.com/app1/)

- requirements.txt

```txt
requests
flask
pandas
dash
gunicorn
```

---
- app.py

```python
import flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

from app1 import app1
from app2 import app2

server = flask.Flask(__name__)


@server.route("/")
def home():
    return "請看-/app1,/app2"

application = DispatcherMiddleware(
    server,
    {"/app1": app1.server, "/app2": app2.server},
)

if __name__ == "__main__":
    run_simple("localhost", 8080, application,use_debugger=True,use_reloader=True)
```

---

- app1.py

```python
from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px

# Incorporate data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

app1 = Dash(requests_pathname_prefix="/app1/")
app1.layout = html.Div([
    html.Div(children='My First App with Data and a Graph'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10),
    dcc.Graph(figure=px.histogram(df, x='continent', y='lifeExp', histfunc='avg'))
])

```

---

- app2.py

```python
from dash import Dash, html, dash_table, dcc

app2 = Dash(requests_pathname_prefix="/app2/")
app2.layout = html.Div("Hello, Dash app 2!")
```


### 上傳至Render展示




