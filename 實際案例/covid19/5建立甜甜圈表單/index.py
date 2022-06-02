import io
from importlib import import_module
from pydoc import classname
from dash import Dash,html,dcc, Input, Output
import dash_bootstrap_components as dbc
from numpy import number
import plotly.graph_objects as go
import pandas as pd
import requests

#requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'
url_confirmed = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
url_deaths = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
url_recovered = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'

url_confirmed_res = requests.get(url_confirmed)
url_deaths_res = requests.get(url_deaths)
url_recovered_res  = requests.get(url_recovered )

confirmed = pd.read_csv(io.BytesIO(url_confirmed_res.content))
deaths = pd.read_csv(io.BytesIO(url_deaths_res.content))
recovered = pd.read_csv(io.BytesIO(url_deaths_res.content))

#unpivote data
date1 = confirmed.columns[4:]
total_confirmed = confirmed.melt(
    id_vars=["Province/State","Country/Region","Lat","Long"],
    value_vars=date1,
    var_name='date',
    value_name='confirmed'
    )
total_confirmed.tail()

date2 = deaths.columns[4:]
total_deaths = deaths.melt(
    id_vars=["Province/State","Country/Region","Lat","Long"],
    value_vars=date2,
    var_name='date',
    value_name='deaths'
    )
total_deaths.head()

date3 = recovered.columns[4:]
total_recovered = recovered.melt(
    id_vars=["Province/State","Country/Region","Lat","Long"],
    value_vars=date3,
    var_name='date',
    value_name='recovered'
    )
total_recovered.head()

#merging dataFrame
covid_data = total_confirmed.merge(
    right=total_deaths,
    how='left',
    on=["Province/State","Country/Region","Lat","Long","date"]
)

covid_data = covid_data.merge(
    right=total_recovered,
    how='left',
    on=["Province/State","Country/Region","Lat","Long","date"]
)

#convert date欄位 從str到date
covid_data["date"] = pd.to_datetime(covid_data["date"])

#檢查是不是none
print(covid_data.isna().sum())

#是none的cell變為0
covid_data['recovered'] = covid_data['recovered'].fillna(0)

#檢查是不是none
print(covid_data.isna().sum())

#建立active的欄位
covid_data['active'] = covid_data['confirmed'] - covid_data['deaths'] - covid_data['recovered']

##取得全球總數
covid_data1 = covid_data.groupby('date')[['confirmed','deaths','recovered','active']].sum().reset_index()

##各國每日總數
covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['confirmed','deaths','recovered','active']].sum().reset_index()

#建立dash
app = Dash(__name__,external_stylesheets=[dbc.themes.DARKLY])
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.Img(src=app.get_asset_url('corona-logo-1.jpg'),className="p-2",style={'width':'100px','height':'auto'})
            ,width=4),
        dbc.Col([
            html.H3("Covid-19"),
            html.H5("全球案例追蹤")
        ],width=4,className='text-center'),
        dbc.Col([
            html.H3("最新日期:"),
            html.H5(str(covid_data['date'].iloc[-1].strftime('%Y-%m-%d')),style={'color':'#EAA136'})
        ],width=4,class_name="text-end")
    ]),
    #建立3欄版面
    dbc.Row([
        dbc.Col([
            html.H4("全球染疾數",style={'color':'#EAA136'}),
            html.H4(f'{covid_data1["confirmed"].iloc[-1]:,.0f}'),
            html.P(f'增加人數:{covid_data1["confirmed"].iloc[-1] - covid_data1["confirmed"].iloc[-2]:,.0f}',className='mt-5'),
            html.P(f'增加比例:{(covid_data1["confirmed"].iloc[-1] - covid_data1["confirmed"].iloc[-2]) / covid_data1["confirmed"].iloc[-1] * 100:,.4f}%')
        ],class_name="border mx-3 text-center pt-3"),
        dbc.Col([
            html.H4("全球死亡數",style={'color':'#D30F0F'}),
            html.H4(f'{covid_data1["deaths"].iloc[-1]:,.0f}'),
            html.P(f'增加人數:{covid_data1["deaths"].iloc[-1] - covid_data1["deaths"].iloc[-2]:,.0f}',className='mt-5'),
            html.P(f'增加比例:{(covid_data1["deaths"].iloc[-1] - covid_data1["deaths"].iloc[-2]) / covid_data1["deaths"].iloc[-1] * 100:,.4f}%')
        ],class_name="border mx-3 text-center pt-3"),
        dbc.Col([
            html.H4("全球無症狀數",style={'color':'#16A519'}),
            html.H4(f'{covid_data1["active"].iloc[-1]:,.0f}'),
            html.P(f'增加人數:{covid_data1["active"].iloc[-1] - covid_data1["active"].iloc[-2]:,.0f}',className='mt-5'),
            html.P(f'增加比例:{(covid_data1["active"].iloc[-1] - covid_data1["active"].iloc[-2]) / covid_data1["active"].iloc[-1] * 100:,.4f}%')
        ],class_name="border mx-3 text-center pt-3")
    ],class_name="pt-5"),
    #建立下拉式
    dbc.Row([
        dbc.Col([
            html.H5('選擇國家:'),
            dcc.Dropdown(
                id='w_countries',
                multi=False,
                searchable=True,
                value='Taiwan*',
                placeholder="請選擇國家:",
                options=[{'label':c, 'value':c} for c in covid_data["Country/Region"].unique()],
            ),
            html.H5("最近日期:"+str(covid_data['date'].iloc[-1].strftime('%Y-%m-%d')),className="pt-3 text-center"),
            dcc.Graph(
                id = 'confirmed',
                config={'displayModeBar':False},
                className="mt-3"
            ),
            dcc.Graph(
                id = 'deaths',
                config={'displayModeBar':False},
                className="mt-3"
            ),
            dcc.Graph(
                id = 'active',
                config={'displayModeBar':False},
                className="mt-3"
            )            

        ],class_name="col-3 border"),
        dbc.Col("建立bar Chart",class_name='col-4 border'),
        dbc.Col("建立整合的Line和Bar Chart",class_name='col-5 border')
    ]),
    
],class_name="pt-5")

@app.callback(
    Output('confirmed','figure'),
    [Input('w_countries','value')]
)
def update_confirmed(w_countries):
    value_confirmed = covid_data_2[covid_data_2['Country/Region']== w_countries]['confirmed'].iloc[-1] - covid_data_2[covid_data_2['Country/Region']== w_countries]['confirmed'].iloc[-2]
    delta_confirmed = covid_data_2[covid_data_2['Country/Region']== w_countries]['confirmed'].iloc[-2] - covid_data_2[covid_data_2['Country/Region']== w_countries]['confirmed'].iloc[-3]
    fig = go.Figure()
    fig.add_trace(
        go.Indicator(
            mode = 'number+delta',
            value = value_confirmed,
            delta = {
                'reference':delta_confirmed,
                'position':'right',
                'valueformat':'g',
                'relative':False,
                'font':{'size':15}
            },
            number = {
                'valueformat': ',',
                'font':{'size':20}
            },
            domain={
                'x':[0,1],
                'y':[0,1]
            }
        )
    )

    fig.update_layout(
        title={
                'text': '新確診',
                'y': 1,
                'x': 0.5,
                'xanchor':'center',
                'yanchor':'top'
        },
        font=dict(color='orange'),
        paper_bgcolor="#222",
        plot_bgcolor="#222",
        height = 50
    )

    return fig
    
@app.callback(
    Output('deaths','figure'),
    [Input('w_countries','value')]
)
def update_deathed(w_countries):
    value_deaths = covid_data_2[covid_data_2['Country/Region']== w_countries]['deaths'].iloc[-1] - covid_data_2[covid_data_2['Country/Region']== w_countries]['deaths'].iloc[-2]
    delta_deaths = covid_data_2[covid_data_2['Country/Region']== w_countries]['deaths'].iloc[-2] - covid_data_2[covid_data_2['Country/Region']== w_countries]['deaths'].iloc[-3]
    fig = go.Figure()
    fig.add_trace(
        go.Indicator(
            mode = 'number+delta',
            value = value_deaths,
            delta = {
                'reference':delta_deaths,
                'position':'right',
                'valueformat':'g',
                'relative':False,
                'font':{'size':15}
            },
            number = {
                'valueformat': ',',
                'font':{'size':20}
            },
            domain={
                'x':[0,1],
                'y':[0,1]
            }
        )
    )

    fig.update_layout(
        title={
                'text': '最新死亡',
                'y': 1,
                'x': 0.5,
                'xanchor':'center',
                'yanchor':'top'
        },
        font=dict(color='orange'),
        paper_bgcolor="#222",
        plot_bgcolor="#222",
        height = 50
    )

    return fig

@app.callback(
    Output('active','figure'),
    [Input('w_countries','value')]
)
def update_recovered(w_countries):
    value_active = covid_data_2[covid_data_2['Country/Region']== w_countries]['active'].iloc[-1] - covid_data_2[covid_data_2['Country/Region']== w_countries]['active'].iloc[-2]
    delta_active = covid_data_2[covid_data_2['Country/Region']== w_countries]['active'].iloc[-2] - covid_data_2[covid_data_2['Country/Region']== w_countries]['active'].iloc[-3]
    fig = go.Figure()
    fig.add_trace(
        go.Indicator(
            mode = 'number+delta',
            value = value_active,
            delta = {
                'reference':delta_active,
                'position':'right',
                'valueformat':'g',
                'relative':False,
                'font':{'size':15}
            },
            number = {
                'valueformat': ',',
                'font':{'size':20}
            },
            domain={
                'x':[0,1],
                'y':[0,1]
            }
        )
    )

    fig.update_layout(
        title={
                'text': '最新無症狀',
                'y': 1,
                'x': 0.5,
                'xanchor':'center',
                'yanchor':'top'
        },
        font=dict(color='orange'),
        paper_bgcolor="#222",
        plot_bgcolor="#222",
        height = 50
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)







