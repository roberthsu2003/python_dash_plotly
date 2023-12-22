from dash import Dash, html,dash_table
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from .assets import function
import pandas as pd


#-----指定網頁路徑的名稱及套用dash_bootstrap_components設定-----#
dash2 = Dash(requests_pathname_prefix="/dash/app2/",external_stylesheets=[dbc.themes.BOOTSTRAP])

#-----頁籤的命名-----#   
dash2.title='DASH的示範網頁'

#-----導入資料來源-----#

df = pd.read_csv('../select_col.csv')
#df.columns =['股票代號','交易日','開盤價','收盤價','最高價','最低價','漲跌(元)','成交股數']



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
        ])
    ],
    className="container-lg"
    )