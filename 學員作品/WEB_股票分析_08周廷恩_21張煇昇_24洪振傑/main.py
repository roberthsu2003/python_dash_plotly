from flask import Flask, send_from_directory, redirect
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from web_stock import app1

# 初始化Flask應用程序
server = Flask(__name__)

# 初始化Dash應用程序
app = dash.Dash(__name__, server=server, url_base_pathname='/')
application = DispatcherMiddleware(server, {
    "/tech": app1.server
})

# 加載CSV文件並根據日期從最新到最舊排序
df = pd.read_csv('2330.csv')
df['Date'] = pd.to_datetime(df['Date'])  # 假設日期列名為' Date'
df = df.sort_values(by='Date', ascending=False) 

# Dash應用程序的佈局
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),  # 添加Location組件來跟踪URL
    html.Div([
        html.H1('台股預測:以台積電為例', style={'textAlign': 'center'}),
        html.Img(src='/image/stock_logo.png', style={'width': '200px'})
    ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'padding': '20px', 'borderBottom': '2px solid #000'}),

    html.Div([
        dcc.Link('首頁', href='/'),
        dcc.Link('技術圖', href='/tech', style={'marginLeft': '20px'}),
    ], style={'textAlign': 'center', 'padding': '20px', 'borderBottom': '2px solid #000'}),

    html.Div(id='page-content', children=[
        html.H2('股票資訊:', style={'color': 'orange'}),
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            style_table={'width': '100%', 'height': '400px', 'overflowY': 'auto'},
            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
            style_cell={'textAlign': 'left'}
        )
    ], style={'padding': '20px', 'border': '2px solid #FFD700', 'borderRadius': '15px', 'marginTop': '20px'})
], style={'fontFamily': 'Arial, sans-serif'})

# 回調函數來處理URL變化
@app.callback(
    dash.dependencies.Output('page-content', 'children'),
    [dash.dependencies.Input('url', 'pathname')]
)
def update_page(pathname):
    if pathname == '/tech':
        return dcc.Location(href="/tech", id="redirect")
    else:
        return html.Div([
            html.H2('股票資訊:', style={'color': 'orange'}),
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                style_table={'width': '100%', 'height': '400px', 'overflowY': 'auto'},
                style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
                style_cell={'textAlign': 'left'}
            )
        ], style={'padding': '20px', 'border': '2px solid #FFD700', 'borderRadius': '15px', 'marginTop': '20px'})

# Flask路由來提供LOGO圖片
@server.route('/image/<path:path>')
def serve_asset(path):
    return send_from_directory('image', path)

# Flask路由來處理 /tech
@server.route("/tech")
def tech_redirect():
    return redirect("/tech", code=302)

# 運行伺服器
if __name__ == '__main__':
    run_simple("localhost", 8080, application, use_debugger=True, use_reloader=True)
