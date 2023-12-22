from dash import Dash, html, dash_table
import pandas as pd
import dash_bootstrap_components as dbc
from collections import OrderedDict

dash2 = Dash(requests_pathname_prefix="/dash/app2/",external_stylesheets=[dbc.themes.BOOTSTRAP])

dash2.title = "台北市東區Qtime"

data = OrderedDict(
    [
        ("Date",["2015-0101","2015-10-24","2016-05-10","2017-01-10","2018-05-10","2018-08-15"]),
        ("Region",["Montreal","Toronto","New York City","Miami","San Francisco","London"]),
        ("Temperature",[1,-20,3.512,4,10423,-441.2]),
        ("Humidity",[10,20,30,40,50,60]),
        ("Pressure",[2,10924,3912,-10,3591.2,15]),        
    ])

df=pd.DataFrame(
    OrderedDict([(name,col_data * 10) for (name,col_data) in data.items()])
)


dash2.layout = html.Div(
    [
        dbc.Container([
            html.Div([
                html.Div([
                    html.H1("台北市東區Qtime")
                ],className="col text-center")
            ],
            className="row",
            style={"paddingTop":"2rem"}),
            html.Div([
                html.Div([
                    dash_table.DataTable(
                        data=df.to_dict('records'),
                        columns=[{'id':column,'name':column} for column in df.columns],
                        page_size=20,
                        style_table={'height': '300px', 'overflowY': 'auto'}
                    ),
                ],className="col text-center")
            ],
            className="row",
            style={"paddingTop":'2rem'}),
        ])
    ],
    className="container-lg"
    )
