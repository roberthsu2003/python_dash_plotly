import dash
from dash import html
from dash import dcc
from dash.dependencies import Output,Input
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
import sqlite3
import plotly.express as px

# 引入資料庫資料
conn = sqlite3.connect("./pokemon_database.db")
df = pd.read_sql_query("SELECT img_num,name,sp,expertise,level,help_fruit,help_ingredient_1,help_ingredient_num_1,help_ingredient_num_2,help_ingredient_num_3,help_time,help_max,skill_main,power_up,power_down FROM pokemon", conn)
df.loc[0].to_list()

# 表格
columns=[
    {'name':'編號','id':'img_num'},
    {'name':'名稱','id':'name'},
    {'name':'SP值','id':'sp'},
    {'name':'專長','id':'expertise'},
    {'name':'等級','id':'level'},
    {'name':'樹果','id':'help_fruit'},
    {'name':'食材','id':'help_ingredient_1'},
    {'name':'加成1','id':'help_ingredient_num_1'},
    {'name':'加成2','id':'help_ingredient_num_2'},
    {'name':'加成3','id':'help_ingredient_num_3'},
    {'name':'幫忙時間','id':'help_time'},
    {'name':'持有上限','id':'help_max'},
    {'name':'主技能','id':'skill_main'},
    {'name':'性格↑','id':'power_up'},
    {'name':'性格↓','id':'power_down'},
]
table=dash_table.DataTable(
    id='table',
    columns=columns,
    data=df.to_dict("records"),
    page_size=5,
    row_selectable='single',
    filter_action='native',
    style_cell={
        'textAlign':'center',
        'background-color': 'rgba(255, 255, 255, 0.3)',
    },
)

def rule(selected_rows):
    if selected_rows:
        pokemon_data = df.iloc[selected_rows[0]]
        name = pokemon_data["name"]
        tags = pokemon_data[["expertise", "help_fruit", "skill_main"]].tolist()
        abls = pokemon_data[["level", "help_max", "help_ingredient_num_1", "help_ingredient_num_2", "help_ingredient_num_3"]].tolist() 
        img_path = f"./assets/img/display/{pokemon_data['img_num']}.png"
        return JumboItem(name, tags, abls, img_path)      
    else:
        return ""

# 圖片 & 圈圈
def JumboItem(name,tags,abls,img):
    hex_area={
        'r':abls,
        'theta':["等級","持有上限","食材加成1","食材加成2","食材加成3"],
    }
    fig=px.line_polar(
        hex_area,
        r="r",
        theta="theta",
        line_close=True,
        range_r=[0,40],
        markers='.',
        start_angle=0,
        width=400,
        height=400,
    )
    fig.update_traces(fill="toself")
    fig.update_layout(paper_bgcolor='rgba(0, 0, 0, 0)',font_size=16)
    return dbc.Row([
        dbc.Col(
            [
                html.Img(src=img,
                         height='300px',
                         width='300px',
                         ),
                html.H1(name.upper()),
                html.Span([
                        dbc.Row(
    [
        dbc.Col(html.H3("專長"), width=4),
        dbc.Col(dbc.Badge(tags[0], color="primary", className="mr-1"), width=8),
    ],
    style={"margin-left":40 ,'float':'left'},
),
dbc.Row(
    [
        dbc.Col(html.H3("樹果"), width=4),
        dbc.Col(dbc.Badge(tags[1], color="primary", className="mr-1"), width=8),
    ],
    style={"margin-left": 45,'float':'left'},
),
dbc.Row(
    [
        dbc.Col(html.H3("主技能"), width=4),
        dbc.Col(dbc.Badge(tags[2], color="primary", className="mr-1"), width=8),
    ],
),
                    ])
            ],
            width=6,
            align='center',
        ),
        dbc.Col(
            [
                dcc.Graph(figure=fig)
            ],
            width=6,
            style={'marginTop':'100px'}
        )
    ],style={'display':'flex',
             'justify-content': 'space-around','align-items':'center',
             'textAlign':'center',
             'marginBottom':'10px',
             'background-color': 'rgba(0, 0, 0, 0)'}
    )

# logo & 影片
logo = html.A(html.Img(src="./assets/img/logo.png", height="100px", width="auto"), href="/logo-page")
video = html.Div([
    html.Iframe(
        src="./assets/video.mp4",
        title="YouTube video player",
        width="500",
        height="380",
    )
], style={'text-align': 'center'})

# 整體-logo & 影片
index_layout = html.Div([
    html.Div(logo, style={'text-align': 'center','margin':'50px 0'}),
    html.Div(video, style={'text-align': 'center'})
], style={'height': '100vh',
          'display': 'flex',
          'flex-direction': 'column', 
          'align-items': 'center'})

# 整體-圖片 & 圈圈
logo_page_layout = html.Div([
    html.Div(logo, style={'text-align': 'center','margin-top':'50px'}),
    html.Div(id="target"),
    dcc.Input(id='search-bar', placeholder='請輸入神奇寶貝名稱',style={'margin':'10px 20px',
    'color':'black'}),
    dbc.Container([table],style={'margin':'0 20px'})
])

app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(
    Output('target', 'children'),
    [Input('table', 'selected_rows')]
)
def update_details(selected_rows):
    return rule(selected_rows)

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return index_layout
    elif pathname == '/logo-page':
        return logo_page_layout
    else:
        return '404: Page not found'

@app.callback(
    Output('table', 'data'),
    Input('search-bar', 'value')
)
def filter_table(search_value):
    if search_value:
        filtered_data = df[df['name'].str.contains(search_value.lower())].to_dict('records')
    else:
        filtered_data = df.to_dict('records')
    return filtered_data

if __name__ == '__main__':
    app.run_server(debug=True)