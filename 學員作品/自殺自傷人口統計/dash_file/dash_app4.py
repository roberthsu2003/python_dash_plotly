from dash import dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, callback,State,ctx
from dash import callback_context
from dash.dependencies import Input, Output
from . import data as DA

dash4 = Dash(requests_pathname_prefix="/dash/app4/")
dash4.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    dbc.Container([
        
        html.Div([html.H1("Suicide Ideation "),html.H2('自殺及自傷方式統計')],      
         className="title"),
        html.Div([
            html.Button('', id='btn-nclicks-0', n_clicks=0,className="buttonbox" ),
            html.Button('', id='btn-nclicks-1', n_clicks=0,className="buttonbox"),
            html.Button('', id='btn-nclicks-2', n_clicks=0 ,className="buttonbox"),
            html.Button('', id='btn-nclicks-3', n_clicks=0,className="buttonbox" ),
            html.Button('', id='btn-nclicks-4', n_clicks=0 ,className="buttonbox"),
            html.Button('', id='btn-nclicks-5', n_clicks=0,className="buttonbox" ),
            html.Button('', id='btn-nclicks-6', n_clicks=0 ,className="buttonbox"),
            html.Button('', id='btn-nclicks-7', n_clicks=0,className="buttonbox" ),
            html.Button('', id='btn-nclicks-8', n_clicks=0 ,className="buttonbox")
        ],className="bigbox"),
        html.Div(html.P("人生自古誰無死 , 早死晚死都得死"),className="txt"),
        html.Div([ 
            html.Div(id="chart-container",className="piechart"),
            html.Div(id="chart-container2",className="barchart"),],className="bigchart"),
            html.Div([
                html.Div(id="chart-container3",className="linechart")],className='linebox'),
    ]),
    html.Img(src=dash4.get_asset_url("775275f2cf950299.gif"),className="imgg"),
    html.Button("", id='btn-nclicks-9', n_clicks=0, className="backbuttom"),
    html.Div(html.P("只要我比你晚死,就在你墳頭蹦迪!"),className="txt")
])

@callback(
    [Output("chart-container", "children"),
     Output("chart-container2", "children"),
     Output("chart-container3", "children")],
    [Input('btn-nclicks-0', 'n_clicks'),
     Input('btn-nclicks-1', 'n_clicks'),
     Input('btn-nclicks-2', 'n_clicks'),
     Input('btn-nclicks-3', 'n_clicks'),
     Input('btn-nclicks-4', 'n_clicks'),
     Input('btn-nclicks-5', 'n_clicks'),
     Input('btn-nclicks-6', 'n_clicks'),
     Input('btn-nclicks-7', 'n_clicks'),
     Input('btn-nclicks-8', 'n_clicks')],
    [State('chart-container', 'children')])

def update_chart(btn0_clicks,btn1_clicks, btn2_clicks, btn3_clicks,btn4_click,btn5_click,btn6_click,btn7_click,btn8_click, current_chart):
    ctx = callback_context

    if not ctx.triggered_id:
        button_id = "btn-nclicks-0"
    else:
        button_id = ctx.triggered_id.split(".")[0]

    if button_id == 'btn-nclicks-0':
        chart1 = [DA.total_pie()]
        chart2 = [DA.total_bar()]
        chart3 = [DA.total_line(),DA.total_list()]
    elif button_id == 'btn-nclicks-1':
        chart1 = [DA.generate_pie_chart_drug()]
        chart2 = [DA.generate_bar_chart_drug()]
        chart3 = [DA.generate_line_chart_drug()]
    elif button_id == 'btn-nclicks-2':
        chart1 = [DA.generate_pie_chart_air()]
        chart2 = [DA.generate_bar_chart_air()]
        chart3 = [DA.generate_line_chart_air()]
    elif button_id == 'btn-nclicks-3':
        chart1 = [DA.generate_pie_chart_hang()]
        chart2 = [DA.generate_bar_chart_hang()]
        chart3 = [DA.generate_line_chart_hang()]
    elif button_id == 'btn-nclicks-4':
        chart1 = [DA.generate_pie_chart_drown()]
        chart2 = [DA.generate_bar_chart_drown()]
        chart3 = [DA.generate_line_chart_drown()]
    elif button_id == 'btn-nclicks-5':
        chart1 = [DA.generate_pie_chart_gun()]
        chart2 = [DA.generate_bar_chart_gun()]
        chart3 = [DA.generate_line_chart_gun()]
    elif button_id == 'btn-nclicks-6':
        chart1 = [DA.generate_pie_chart_cut()]
        chart2 = [DA.generate_bar_chart_cut()]
        chart3 = [DA.generate_line_chart_cut()]
    elif button_id == 'btn-nclicks-7':
        chart1 = [DA.generate_pie_chart_jump()]
        chart2 = [DA.generate_bar_chart_jump()]
        chart3 =[DA.generate_line_chart_jump()]
    elif button_id == 'btn-nclicks-8':
        chart1 = [DA.generate_pie_chart_other()]
        chart2 = [DA.generate_bar_chart_other()]
        chart3 = [DA.generate_line_chart_other()]
    else:
        pass

    return chart1,chart2,chart3
@callback(
    Output('url', 'pathname'),
    [Input('btn-nclicks-9', 'n_clicks')],
    [State('url', 'pathname')]
)
def go_back(n_clicks, current_path):
    if n_clicks > 0:
        return "../../"  # 返回到首頁
    else:
        pass  # 避免更新