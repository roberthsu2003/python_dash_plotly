import dash
from dash import Dash, html
import dash_bootstrap_components as dbc


app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server=app.server

app.layout = html.Div(
    [
        dbc.NavbarSimple(
            children=[
                dbc.NavLink("首頁", href="/", active="exact"),
                dbc.NavLink("資料庫", href="/archive", active="exact"),
                dbc.NavLink("統計表", href="/analysis", active="exact"),
            ],
            brand="動畫觀看數統計_以巴哈姆特動畫瘋為例",
            color="success",
            dark=True,
            className='fixed-top'
        ),
        dash.page_container,
    ]
)

if __name__ == '__main__':
    app.run(debug=True)