from dash import Dash, html, dash_table, dcc, callback,Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from .assets import function
import pandas as pd
import plotly.graph_objects as go
from .assets import dash_function
import csv


#-----指定網頁路徑的名稱及套用dash_bootstrap_components設定-----#
dash2 = Dash(requests_pathname_prefix="/dash/app2/",external_stylesheets=[dbc.themes.BOOTSTRAP])

#-----頁籤的命名-----#   
dash2.title = '股價查詢網頁'

#-----導入資料來源-----#
#-----表格資料-----#
df = pd.read_csv('../select_col.csv')
#df.columns =['股票代號','交易日','開盤價','收盤價','最高價','最低價','漲跌(元)','成交股數']
df2=pd.read_csv('../mov.csv')



#-----產生K棒圖資料-----#
df2 = pd.read_csv("../stock.csv")
k_candle = go.Figure(data=[go.Candlestick(x=df2['date'],
                open=df2['open'],
                high=df2['max'],
                low=df2['min'],
                close=df2['close'])])

#-----產生均線圖資料-----#
df3 = pd.read_csv("../mov.csv")
avg_line=go.Figure()
avg_5=avg_line.add_trace(go.Scatter(x=df3['日期'],y=df3['5日移動均價'],line=dict(color='red'),name='5日移動均價',))
avg_20=avg_line.add_trace(go.Scatter(x=df3['日期'],y=df3['20日移動均價'],line=dict(color='blue'),name='20日移動均價',))

#-----產生成交量圖示-----#
df4 = pd.read_csv("../mov.csv")
trade_vol = px.bar(df, x=df4['日期'], y=df4['當日成交量'])




dash2.layout = html.Div(
    [
        dbc.Container([
            html.Div([
                html.Div([
                    html.H1("個股資料查詢")
                ],className="col text-center")
            ],
            className="row",
            style={"paddingTop":'2rem'}),
            html.Div([
                html.Div([
                    dash_table.DataTable(
                        data=df.to_dict('records'),
                        columns=[{'id':column,'name':column} for column in df.columns],
                        page_size=20,
                        style_table={'height': '250px', 'overflowY': 'auto'},
                        fixed_rows={'headers': True}
                    ),
                ],className="col text-center") # col-n是調整欄位寬度及位置
            ],
            className="row",
            style={"paddingTop":'2rem'}),
            html.Div([
                html.Button('查詢各日均價', id='show-secret'),
                html.H2(id='body-div',style={'color': '#E83015'})
            ]),
            html.Div([
                html.H1('價格走勢圖'),
                dcc.Graph(figure=k_candle)
            ]),
            html.Div([
                html.H1('5/20日均線走勢圖'),
                dcc.Graph(figure=avg_line)
            ]),
            html.Div([
                html.H1('成交量長條圖'),
                dcc.Graph(figure=trade_vol)
            ])
        ])
    ],
    className="container-lg"
    )


@callback(
    Output('body-div', 'children'),
    Input('show-secret', 'n_clicks')
)
def update_output(n_clicks):
    if n_clicks is None:
        print('done')
    else:
        with open('../mov1.csv','r',encoding='utf-8') as file:
            line = file.readlines()
            last_line=line[-1]
            
        return f'五日均價計算={last_line}'
    


    
