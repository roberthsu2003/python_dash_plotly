from dash import Dash, html, dash_table, callback, Input, Output, dcc
import dash_bootstrap_components as dbc
import pandas as pd
from . import data
import plotly.express as px

dash_index = Dash(
    requests_pathname_prefix="/dash/index/", external_stylesheets=[dbc.themes.QUARTZ]
)
dash_index.title = "2023信用卡消費樣態"
lastest_data = data.search_data(dataName="年齡層",tableName="age")
lastest_df = pd.DataFrame(
    lastest_data, columns=["年", "月", "地區", "產業別", "年齡層", "信用卡交易筆數", "信用卡交易金額"]
)

dash_index.layout = html.Div(
    [
        dbc.Container(
            [
                html.Div(
                    [html.Div([html.H1("2023信用卡消費樣態")], className="col text-center")],
                    className="row",
                    style={"padding": "3rem 0 1rem 0"},
                ),
                html.Div([
                    dcc.Graph(id="graph_line"),
                ]),
                html.Div(
                    [
                        dbc.Button("教育程度", color="info", className="me-4", href="/dash/app/", external_link=True, style={"fontWeight": "bold"}),
                        dbc.Button("年齡層", color="secondary", className="me-4", href="/dash/app1/", external_link=True, style={"fontWeight": "bold"}),
                        dbc.Button("職業類別", color="success", className="me-4", href="/dash/app2/", external_link=True, style={"fontWeight": "bold"}),
                        dbc.Button("性別", color="warning", className="me-4", href="/dash/app3/", external_link=True, style={"fontWeight": "bold"}),
                        dbc.Button("年收入", color="primary", className="me-4", href="/dash/app4/", external_link=True, style={"fontWeight": "bold"}),
                    ],
                    className="d-flex justify-content-center",
                    style={"paddingTop": "2.5rem"},
                ),
            ]
        )
    ],
    className="container-lg",
)

@dash_index.callback(
    Output("graph_line", "figure"),
    Input("graph_line", "id")
)
def line_chart(graph_id):
    global lastest_df
    monthly_total = lastest_df.groupby(['年', '月'])['信用卡交易金額'].sum().reset_index()
    fig = px.line(monthly_total, x="月", y="信用卡交易金額", color="年", markers=True)
    for trace in fig.data:
        trace.line.color = 'goldenrod'
        trace.line.width = 2.5
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0.1)',
        },
        showlegend=False,
        xaxis={'showgrid': False, 'color':'white'},
        yaxis={'showgrid': True, 'color':'white'})
    return fig


