from dash import Dash, html, dash_table, callback, Input, Output, dcc, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc
from . import cpbl_datasource
import base64
import os

dash5 = Dash(requests_pathname_prefix="/dash/fubon/", external_stylesheets=[dbc.themes.BOOTSTRAP])

#連結外部css檔
external_stylesheets=['assets/header.css']

dash5.title='富邦悍將 中華職棒投手資料查詢系統-Chinese Professional Baseball League Pitchers'

current_data = cpbl_datasource.fubon_data()
current_df = pd.DataFrame(current_data,
                          columns=['年份','所屬球隊', '球員編號', '球員姓名', '先發次數', '中繼次數', '勝場數', '敗場數', '三振數', '自責分'])

#layout
dash5.layout = html.Div(
    [
        dbc.Container([
            html.Div([
                html.Div([
                    html.Img(src=[cpbl_datasource.team_logo('fubon_index')],width=1200),
                    html.Br(),
                    ],className="", style={'justify-content':'center', 'width':'100%',
                    'margin-left':'2rem'})
            ],
            className="row",
            style={"paddingTop":'2rem'}),
            #搜尋功能
            html.Div([
                html.Div([
                    html.Div([
                            dbc.Input(
                                placeholder="請輸入球員姓名查詢", 
                                type="text",
                                id='input_value',
                                ),
                            ],style={'justify-content':'center'})
                ],className="",style={'text-align':'center', 'width':'800px', 'margin':'1rem'}),
                
                html.Div([
                    html.Button(children='查詢', 
                                id='btn',
                                className="btn btn-primary",)
                        ],className="",style={'text-align':'center','padding':'1rem'}),
            ],
            className="search-btn",
            style={'justify-content':'center', 'display':'flex', 'padding':'1rem', 'margin':'2rem'}),
            
            html.Div([
                html.A(id='rakuten',className='team_logo',href='/dash/rakuten', children=[
                    html.Img(src=[cpbl_datasource.team_logo('monkeys'),],width='150px', height='150px'),
                    ],style={'text-decoration': 'none',}),html.Br(),
                
                html.A(id='brothers',className='team_logo',href='/dash/brothers', children=[
                    html.Img(src=[cpbl_datasource.team_logo('brothers')], width='160px', height='160px'),
                 ],style={'text-decoration': 'none','margin-left':'2rem'}),html.Br(),  
                
                html.A(id='lions',className='team_logo',href='/dash/lions', children=[
                    html.Img(src=[cpbl_datasource.team_logo('lions')], width='160px', height='160px'),
                 ],style={'text-decoration': 'none','margin-left':'2rem'}),html.Br(),  
                
                html.A(id='fubon',className='team_logo',href='/dash/fubon', children=[
                    html.Img(src=[cpbl_datasource.team_logo('fubon')], width='160px', height='160px'),
                 ],style={'text-decoration': 'none','margin-left':'2rem'}),html.Br(),  
                
                html.A(id='dragons',className='team_logo',href='/dash/dragons', children=[
                    html.Img(src=[cpbl_datasource.team_logo('dragons')], width='160px', height='160px'),
                 ],style={'text-decoration': 'none','margin-left':'2rem'}),html.Br(), 
                
                html.A(id='hawks',className='team_logo',href='/dash/app1', children=[
                    html.Img(src=[cpbl_datasource.team_logo('hawks')], width='160px', height='160px'),
                 ],style={'text-decoration': 'none','margin-left':'2rem'}),html.Br(),

                html.A(id='home',className='team_logo',href='/dash/app1', children=[
                    html.Img(src=[cpbl_datasource.team_logo('cpbl')], width='160px', height='160px'),
                 ],style={'text-decoration': 'none','margin-left':'2rem'}),html.Br(),  
                        
            ],className='team_box', style={'display':'flex', 'justify-content':'center'}),

            html.Div([
                html.H3(['球員列表']),
                html.Div([
                    dash_table.DataTable(
                        id='main_table',
                        page_size=10,
                        style_header={'background-color':'#577C8A', 'text-align':'center', 'fontWeight': 'bold', 'color':'white'},
                        style_table={'width':'90%', 'overflowY': 'auto', 'margin':'5%'},
                        fixed_rows={'headers': True},
                        row_selectable='single',
                        selected_rows=[],
                        style_cell_conditional=[
                                {'textAlign': 'center'},
                                {   'if': {'column': 'selected_rows'}, 'width': '5px'},
                                {   'if': {'column_id': '年份'},'width': '8%'},
                                {   'if': {'column_id': '所屬球隊'},'width': '8%'},
                                {   'if': {'column_id': '球員編號'},'width': '8%'},
                                {   'if': {'column_id': '球員姓名'},'width': '8%'},
                                {   'if': {'column_id': '出場數'},'width': '10%'},
                                {   'if': {'column_id': '先發次數'},'width': '10%'},
                                {   'if': {'column_id': '中繼次數'},'width': '10%'},
                                {   'if': {'column_id': '勝場數'},'width': '10%'},
                                {   'if': {'column_id': '敗場數'},'width': '10%'},
                                {   'if': {'column_id': '三振數'},'width': '10%'},
                                {   'if': {'column_id': '自責分'},'width': '10%'},

                        ],

                    ),
                ],className="col text-center")
            ],
            className="row",
            style={"paddingTop":'0.5rem'}),

            
            html.H3(['球員詳細資料']),
            html.Div([
                html.Div([
                    html.Div([
                        html.Img(id='photo',className="",style={'width':'200px', 'height':'270px','margin': '0', 'padding':'0' , 'text-align':'justify'}),
                        ],className="col"),
                    html.Div(
                        className="col",id='showMessage'),
                    html.Div([
                        dcc.Graph(id='game_pie')],
                        className='col',
                        style={'padding':'0.5rem'}),
                ],className="row align-items-center",style={'margin': '2rem', 'text-align':'center'})],
            className="container text-center",style={'width':'100%','margin-left': '0', 'text-align':'center'}),
            
            html.Div([
                html.Div([
                    dcc.Graph(id='info')],
                    className='col',
                    style={'margin':'2rem'}),

                    html.Div([
                    dcc.Graph(id='game_out', figure=go.Figure())],
                    className='col',
                    style={'margin-left':'8rem', 'padding':'3rem'}),
            ], className='row',style={'display':'flex','justify-content':'space-between'}),

            html.Div(['© Copyright 2023 by Rachel Yeh'],
            style={'width':'1200px','height':'100px', 'background-color':'#0F2540', 'color':'white','textAlign': 'center','leight-height':'100px' ,'margin':'auto', 'padding':'2rem'})
        ])        
    ],
    className="container-lg")

#按下查詢按鈕，啟動查詢＆回傳資料  
@dash5.callback(
    [Output('main_table','data'), Output('main_table', 'columns'), Output('main_table', 'selected_rows')],
    [Input('btn','n_clicks')],
    [State('input_value','value')],
)

def search_clickBtn(n_clicks:None | int, inputValue:str):
    global current_df
    if n_clicks is not None:
        #呼叫datasource的搜尋方法，傳出list[tuple]
        searchData:list[tuple] = cpbl_datasource.search_sitename(inputValue)
        current_df = pd.DataFrame(searchData,columns=['年份', '所屬球隊', '球員編號', '球員姓名', '先發次數', '中繼次數', '勝場數', '敗場數', '三振數', '自責分'])
        #print(searchData)
        print('按確定')
        return current_df.to_dict('records'),[{'id':column,'name':column} for column in current_df],[]
    
    
    #當clickBtn is None -> 「確定」按鈕沒被按下，網頁剛啟動時
    else:
        print('第一次啟動')
        current_data = cpbl_datasource.fubon_data()
        current_df = pd.DataFrame(current_data,columns=['年份', '所屬球隊', '球員編號', '球員姓名',  '先發次數', '中繼次數', '勝場數', '敗場數', '三振數', '自責分'])

        return current_df.to_dict('records'), [{'id':column,'name':column} for column in current_df.columns],[]   


#============下方顯示球員資料欄位=================
@dash5.callback(
    Output('showMessage','children'),
    Input('main_table','selected_rows')
)

#抓出選擇的欄位內容
def selectedRow(selected_rows:list[int]): #傳入list[裡面放int]
        global current_df
        #def可以取得py檔的文件變數
        if len(selected_rows) != 0:
              #宣告變數後面加上資料型別(type hint)
            idSite:pd.DataFrame = current_df.iloc[[selected_rows[0]]]
            player_id = int(idSite['球員編號'].iloc[0])
            rows = cpbl_datasource.search_player_by_id(player_id)
            print(f'回來了{rows}')
              
            oneSite_df:pd.DataFrame = pd.DataFrame(rows,columns=['所屬球隊', '球員姓名', '背號', '投打習慣', '身高體重', '生日', '奪三振率', '防禦率'])

            df_transposed = oneSite_df.transpose()
            df_display = pd.DataFrame({
            '球員資料': df_transposed.index,
            '內容': df_transposed.iloc[:, 0].values})

            oneTable:dash_table.DataTable = dash_table.DataTable(
            data=df_display.to_dict('records'),
            style_table={'margin': 0,'height':'100%'},style_header={'fontWeight': 'bold'},
            style_cell_conditional=[
            {'if': {'column_id': '球員資料'}, 'width': '2%','height':'100%', 'text-align': 'center', 'font-weight': 'bold', },
            {'if': {'column_id': '內容'}, 'width': '3%', 'height': '100%', 'text-align': 'center'},])
            
            return oneTable
        

#===================點擊球員資料後顯示圓餅圖======================
@dash5.callback(
    Output('game_pie','figure'),
    Input('main_table','selected_rows')
)

#更新先發中繼圓餅圖
def game_pie(selected_rows:list[int]):
    global current_df
    default_fig = go.Figure()
    if len(selected_rows) != 0:
        idSite:pd.DataFrame = current_df.iloc[[selected_rows[0]]]
        player_id = int(idSite['球員編號'].iloc[0])
        rows = cpbl_datasource.search_player_game_pie(player_id)
        
        games_df:pd.DataFrame = pd.DataFrame(rows,columns=['球員編號','所屬球隊','球員姓名', '出場數','先發次數','中繼次數','勝場數','敗場數','救援成功','中繼成功','有效局數','面對打者數','被安打數','被全壘打數','保送數','三振數','自責分','奪三振率','防禦率'])
        
        # 創建一個空的 DataFrame
        new_df = pd.DataFrame(columns=['出場類型', '出場數'])

        # 添加二維資料
        data = {'先發': [games_df['先發次數'].iloc[0]], '中繼': [games_df['中繼次數'].iloc[0]]}


        # 將二維資料轉換成 DataFrame 並添加到新的 DataFrame
        for category, values in data.items():
            category_df = pd.DataFrame({'出場類型': [category], '出場數': values})
            new_df = pd.concat([new_df, category_df], ignore_index=True)
        
        #設定圓餅圖顏色
        colors = ['#577C8A', '#0F2540']

        game_pie = px.pie(
            new_df, values='出場數', 
            names='出場類型', 
            title='先發&中繼佔比',
            hover_data=['出場數'],
            color_discrete_sequence=colors)
        
        return game_pie
    return default_fig
        
# 更新圖表
@dash5.callback(
    Output('info', 'figure'),
    Input('main_table', 'selected_rows'),
)
def update_bar(selected_rows: list[int]):
    global current_df
    default_fig = go.Figure()
    if len(selected_rows) != 0:
        idSite: pd.DataFrame = current_df.iloc[[selected_rows[0]]]
        player_id = int(idSite['球員編號'].iloc[0])

        rows = cpbl_datasource.search_player_by_id(player_id)
        oneSite_df: pd.DataFrame = pd.DataFrame(rows,
                                                columns=['所屬球隊', '球員姓名', '背號', '投打習慣', '身高體重', '生日', '奪三振率', '防禦率'])

        k9_era = cpbl_datasource.avg_k9_rea()
        k9_era_df = pd.DataFrame(k9_era,
                                 columns=['所屬球隊', '球員姓名', '背號', '投打習慣', '身高體重', '生日', '奪三振率', '防禦率'])

        average_k9 = k9_era_df['奪三振率'].mean()
        average_era = k9_era_df['防禦率'].mean()

        player_k9 = oneSite_df['奪三振率'].iloc[0]
        palyer_era = oneSite_df['防禦率'].iloc[0]
        player_name = oneSite_df['球員姓名'].iloc[0]

        #將資料整理成可以畫圖的陣列
        labels = ['奪三振率', '防禦率']
        fig = go.Figure(data = [
          go.Bar(name='聯盟平均', 
                 x=labels, 
                 y=[average_k9,average_era],     
                 marker_color='#577C8A'),
          go.Bar(name=player_name, 
                 x=labels, 
                 y=[player_k9,palyer_era],
                 marker_color='#0F2540')   
        ])
        print('第一個',average_k9,player_k9)
        print('第二個',average_era,palyer_era)

        fig.update_layout(
            barmode='group', 
            title = '奪三振率及防禦率')

        return fig
    return default_fig


#===============顯示照片========================
@dash5.callback(
    Output('photo', 'src'),
    Input('main_table','selected_rows')
)

def update_photo(selected_rows:list[int]):
    global current_df
        #def可以取得py檔的文件變數
    if len(selected_rows) != 0:
            idSite:pd.DataFrame = current_df.iloc[[selected_rows[0]]]
            player_id = int(idSite['球員編號'].iloc[0])
            
            rows = cpbl_datasource.search_player_by_id(player_id)
            names = rows[0][1]
            # 設定圖片檔案的路徑
            
            img_folder = os.path.join(os.getcwd(),'dash_file' ,'assets', 'img')
            
            # 使用絕對路徑
            imgfile = f'{names}.jpg'

            # 組合路徑
            img_path = os.path.join(img_folder, imgfile)
                                  

            # 讀取圖片檔案，轉換成 base64 編碼
            with open(img_path, "rb") as img_file:
                img_data = base64.b64encode(img_file.read())
                img_data = img_data.decode()
                img_data = "{}{}".format("data:image/jpg;base64, ", img_data)
        
            return img_data
        
#===============對戰分析========================
@dash5.callback(
    Output('game_out', 'figure'),
    Input('main_table','selected_rows')
)

def game_out(selected_rows:list[int]):
    global current_df
    # 預設的圖表
    default_fig = go.Figure()
    if selected_rows:
            #宣告變數後面加上資料型別(type hint)
            idSite:pd.DataFrame = current_df.iloc[[selected_rows[0]]]
            player_id = int(idSite['球員編號'].iloc[0])
            
            #抓出所需資料
            rows = cpbl_datasource.search_player_game_pie(player_id)
            
            games_df:pd.DataFrame = pd.DataFrame(rows,columns=['球員編號','所屬球隊','球員姓名', '出場數','先發次數','中繼次數','勝場數','敗場數','救援成功','中繼成功','有效局數','面對打者數','被安打數','被全壘打數','保送數','三振數','自責分','奪三振率','防禦率'])
            
            data ={
                '被安打數':games_df['被安打數'].iloc[0],
                '保送數':games_df['保送數'].iloc[0],
                '出局數':games_df['面對打者數'].iloc[0] - games_df['被安打數'].iloc[0] - games_df['保送數'].iloc[0],
                '接殺&滾地球出局':games_df['面對打者數'].iloc[0] - games_df['被安打數'].iloc[0] - games_df['保送數'].iloc[0]-games_df['三振數'].iloc[0],
                '三振數':games_df['三振數'].iloc[0],
                '全壘打數':games_df['被全壘打數'].iloc[0],
                '安打數':games_df['被安打數'].iloc[0] - games_df['被全壘打數'].iloc[0],  
            }
            
            # 設置 hovertemplate
            hovertemplate = '<b>%{label}</b><br>數量: %{value}<extra></extra>'

            # 建立層次結構
            hierarchy = {
                'type': 'sunburst',
                'labels': list(data.keys()),
                'parents': ['', '', '', '出局數', '出局數', '被安打數', '被安打數'],
                'values': list(data.values()),
            }

            # 建立 Sunburst 圖
            fig = go.Figure(go.Sunburst(
                labels=hierarchy['labels'],
                parents=hierarchy['parents'],
                values=hierarchy['values'],
                branchvalues='total',
                hovertemplate=hovertemplate,
                marker=dict(
                colors=['#C73E3A', '#4A225D', '#0F2540', '#113285','#577C8A','#D0104C']),
            ))

            fig.update_layout(margin=dict(t=10, b=10, r=10, l=10),
                              font=dict(size=14),
                              width=300,)
            

            return fig   
    return default_fig
