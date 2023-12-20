from dash import Dash, html,dash_table,Input,Output,callback,dcc,State
import pandas as pd
import dash_bootstrap_components as dbc
from . import datasource
import pandas as pd

dash2 = Dash(requests_pathname_prefix="/dash/app2/",external_stylesheets=[dbc.themes.BOOTSTRAP])
dash2.title = "台北市youbike及時資料"
current_data = datasource.lastest_datetime_data()
current_df = pd.DataFrame(current_data,columns=['站點名稱','更新時間','行政區','地址','總數','可借','可還'])
current_df = current_df.reset_index()
current_df['站點名稱'] = current_df['站點名稱'].map(lambda name:name[11:])

dash2.layout = html.Div(    [
        dbc.Container([
            html.Div([
                html.Div([
                    html.H1("台北市youbike及時資料")
                ],className="col text-center")
            ],
            className="row",
            style={"paddingTop":'2rem'}),
            html.Div([
                html.Div([
                    html.Div([
                                dbc.Label("站點名稱"),
                                dbc.Input(id='input_value',
                                          placeholder="請輸入站點名稱", type="text"),                                
                    ])
        
                ],className="col"),
                html.Div([
                    html.Button('確定', id='submit-val',className="btn btn-primary")
                    ],className="col"),                
            ],
            className="row row-cols-auto align-items-end",
            style={"paddingTop":'2rem'}),
            html.Div([
                html.Div([
                    dash_table.DataTable(
                        id='main_table',
                        page_size=20,
                        style_table={'height': '300px', 'overflowY': 'auto'},
                        fixed_rows={'headers': True},
                        style_cell_conditional=[
                                {   'if': {'column_id': 'index'},
                                 'width': '5%'
                                },
                                {   'if': {'column_id': '站點名稱'},
                                 'width': '25%'},
                                {   'if': {'column_id': '總數'},
                                 'width': '5%'},
                                {   'if': {'column_id': '可借'},
                                 'width': '5%'},
                                {   'if': {'column_id': '可還'},
                                 'width': '5%'},
                        ],
                        row_selectable="single",
                        selected_rows=[]
                    ),
                ],className="col text-center")
            ],
            className="row",
            style={"paddingTop":'0.5rem'}),
            html.Div([
                html.Div(children="",className="col",id='showMessage')
            ],
            className="row",
            style={"paddingTop":'2rem'})

        ])
    ],
    className="container-lg"
    )

@callback(
        [Output('main_table','data'),Output('main_table','columns'),Output('main_table','selected_rows')],
        [Input('submit-val','n_clicks')],
        [State('input_value','value')]
)
def clickBtn(n_clicks:None | int,inputValue:str):
    global current_df
    if n_clicks is not None:
        #一定先檢查有沒有按button
        searchData:list[tuple] = datasource.search_sitename(inputValue)
        current_df = pd.DataFrame(searchData,columns=['站點名稱','更新時間','行政區','地址','總數','可借','可還'])
        current_df = current_df.reset_index()
        current_df['站點名稱'] = current_df['站點名稱'].map(lambda name:name[11:])
        print("按確定")
        return current_df.to_dict('records'),[{'id':column,'name':column} for column in current_df.columns],[]

    #n_clicks is None
    #代表第一次啟動
    print("第一次啟動")
    current_data = datasource.lastest_datetime_data()
    current_df = pd.DataFrame(current_data,columns=['站點名稱','更新時間','行政區','地址','總數','可借','可還'])
    current_df = current_df.reset_index()
    current_df['站點名稱'] = current_df['站點名稱'].map(lambda name:name[11:])
    return current_df.to_dict('records'),[{'id':column,'name':column} for column in current_df.columns],[]

@callback(
      Output('showMessage','children'),
      Input('main_table','selected_rows')  
)
def selectedRow(selected_rows:list[int]):
    #取得一個站點,series
    if len(selected_rows) != 0:
        oneSite:pd.DataFrame = current_df.iloc[[selected_rows[0]]]        
        oneTable:dash_table.DataTable =  dash_table.DataTable(oneSite.to_dict('records'), [{"name": i, "id": i} for i in oneSite.columns])
        return oneTable
    
    return None
