import pandas as pd
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

dash1 = Dash(requests_pathname_prefix="/dash/app1/",external_stylesheets=[dbc.themes.BOOTSTRAP])

dash1.title = "Youbike站點車輛訊息"

dash1.layout = html.Div([
    html.H1('捷運大安站Youbike站點車輛訊息'),
    dcc.Graph(id='graph'),
    html.Div([html.A('返回首頁', href='/')])
])

@dash1.callback(
    Output("graph", "figure"),
    Input("graph", "id")
)
def update_line_chart(station):
    df = pd.read_csv('./dash_file/Youbike1221_4.csv')
    fig = px.line(df, x="status", y="number", color='station',text='number')
    fig.update_traces(textposition="bottom right")
    fig.update_layout(paper_bgcolor="rgba(0, 0, 0, 0)")
    
    return fig