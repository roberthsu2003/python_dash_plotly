import io
from dash import Dash,html,dcc, Input, Output
import dash_bootstrap_components as dbc
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

#convert date?????? ???str???date
covid_data["date"] = pd.to_datetime(covid_data["date"])

#???????????????none
print(covid_data.isna().sum())

#???none???cell??????0
covid_data['recovered'] = covid_data['recovered'].fillna(0)

#???????????????none
print(covid_data.isna().sum())

#??????active?????????
covid_data['active'] = covid_data['confirmed'] - covid_data['deaths'] - covid_data['recovered']

##??????????????????
covid_data1 = covid_data.groupby('date')[['confirmed','deaths','recovered','active']].sum().reset_index()

##??????????????????
covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['confirmed','deaths','recovered','active']].sum().reset_index()

#??????dash
app = Dash(__name__,
        external_stylesheets=[dbc.themes.DARKLY],
        meta_tags=[{'name':'viewport','content':'width=device-width'}]
)
server = app.server
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.Img(src=app.get_asset_url('corona-logo-1.jpg'),className="p-2",style={'width':'100px','height':'auto'})
            ,width=4),
        dbc.Col([
            html.H3("Covid-19"),
            html.H5("??????????????????")
        ],width=4,className='text-center'),
        dbc.Col([
            html.H3("????????????:"),
            html.H5(str(covid_data['date'].iloc[-1].strftime('%Y-%m-%d')),style={'color':'#EAA136'})
        ],width=4,class_name="text-end")
    ]),
    #??????3?????????
    dbc.Row([
        dbc.Col([
            html.H4("???????????????",style={'color':'#EAA136'}),
            html.H4(f'{covid_data1["confirmed"].iloc[-1]:,.0f}'),
            html.P(f'????????????:{covid_data1["confirmed"].iloc[-1] - covid_data1["confirmed"].iloc[-2]:,.0f}',className='mt-5'),
            html.P(f'????????????:{(covid_data1["confirmed"].iloc[-1] - covid_data1["confirmed"].iloc[-2]) / covid_data1["confirmed"].iloc[-1] * 100:,.4f}%')
        ],class_name="border text-center pt-3",width=12,lg=3),
        dbc.Col([
            html.H4("???????????????",style={'color':'#D30F0F'}),
            html.H4(f'{covid_data1["deaths"].iloc[-1]:,.0f}'),
            html.P(f'????????????:{covid_data1["deaths"].iloc[-1] - covid_data1["deaths"].iloc[-2]:,.0f}',className='mt-5'),
            html.P(f'????????????:{(covid_data1["deaths"].iloc[-1] - covid_data1["deaths"].iloc[-2]) / covid_data1["deaths"].iloc[-1] * 100:,.4f}%')
        ],class_name="border text-center pt-3",width=12,lg=3),
        dbc.Col([
            html.H4("??????????????????",style={'color':'#16A519'}),
            html.H4(f'{covid_data1["active"].iloc[-1]:,.0f}'),
            html.P(f'????????????:{covid_data1["active"].iloc[-1] - covid_data1["active"].iloc[-2]:,.0f}',className='mt-5'),
            html.P(f'????????????:{(covid_data1["active"].iloc[-1] - covid_data1["active"].iloc[-2]) / covid_data1["active"].iloc[-1] * 100:,.4f}%')
        ],class_name="border  text-center pt-3",width=12,lg=3)
    ],class_name="pt-5",justify='around'),
    #???????????????
    dbc.Row([
        dbc.Col([
            html.H5('????????????:',className='pt-3'),
            dcc.Dropdown(
                id='w_countries',
                multi=False,
                searchable=True,
                value='Taiwan*',
                placeholder="???????????????:",
                options=[{'label':c, 'value':c} for c in covid_data["Country/Region"].unique()],
            ),
            html.H5("????????????:"+str(covid_data['date'].iloc[-1].strftime('%Y-%m-%d')),className="pt-3 text-center"),
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

        ],class_name="border",width=12,lg=3),
        #5?????????????????????
        dbc.Col(dcc.Graph(
            id = 'pie_chart',
            config={'displayModeBar':'hover'}
        ),class_name='border',width=12,lg=4),
        dbc.Col(dcc.Graph(
            id = 'line_chart',
            config={'displayModeBar':'hover'}
        ),class_name='border',width=12,lg=5)
    ],class_name="mt-5"),
    
],class_name="pt-5 px-4")

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
                'text': '????????????',
                'y': 0.9,
                'x': 0.5,
                'xanchor':'center',
                'yanchor':'top'
        },
        font=dict(color='orange'),
        paper_bgcolor="#222",
        plot_bgcolor="#222",
        height = 100
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
                'text': '????????????',
                'y': 0.9,
                'x': 0.5,
                'xanchor':'center',
                'yanchor':'top'
        },
        font=dict(color='red'),
        paper_bgcolor="#222",
        plot_bgcolor="#222",
        height = 100
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
                'text': '???????????????',
                'y': 0.9,
                'x': 0.5,
                'xanchor':'center',
                'yanchor':'top'
        },
        font=dict(color='green'),
        paper_bgcolor="#222",
        plot_bgcolor="#222",
        height = 100
    )

    return fig

@app.callback(
    Output('pie_chart','figure'),
    [Input('w_countries','value')]
)
def update_graph(w_countries):
    ##??????????????????
    covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['confirmed','deaths','recovered','active']].sum().reset_index()
    value_confirmed = covid_data_2[covid_data_2['Country/Region']== w_countries]['confirmed'].iloc[-1] 
    value_deaths = covid_data_2[covid_data_2['Country/Region']== w_countries]['deaths'].iloc[-1]
    value_recovered = covid_data_2[covid_data_2['Country/Region']== w_countries]['recovered'].iloc[-1]
    value_acitve = covid_data_2[covid_data_2['Country/Region']== w_countries]['active'].iloc[-1]
    colors = ['orange','red', 'green']
    fig = go.Figure()
    fig.add_trace(
        go.Pie(
            labels=['??????', '??????', '?????????'],
            values = [value_confirmed, value_deaths, value_acitve],
            marker=dict(colors=colors),
            hoverinfo='label+value+percent',
            textinfo='label+value',
            rotation = 45,
            hole = .3,
            pull = [0,0.2,0]
        )
    )

    fig.update_layout(
        title={
                'text': w_countries + '????????????',
                'y': 0.93,
                'x': 0.5,
                'xanchor':'center',
                'yanchor':'top'
        },
        titlefont={
                'color':'white',
                'size':20
        },
        font=dict(
            family='sans-serif',
            color='white',
            size=12
        ),
        legend={
            'orientation':'h',
            'xanchor':'center',
            'x':0.5,
            'y':-0.2
        },
        paper_bgcolor="#222",
        plot_bgcolor="#222",
        
    )

    return fig

@app.callback(
    Output('line_chart','figure'),
    [Input('w_countries','value')]
)
def update_graph(w_countries):
    ##??????????????????
    covid_data_2 = covid_data.groupby(['date', 'Country/Region'])[['confirmed','deaths','recovered','active']].sum().reset_index()
    covid_data_3 = covid_data_2[covid_data_2['Country/Region']==w_countries][['Country/Region','date','confirmed']].reset_index()
    covid_data_3['daily confirmed'] = covid_data_3['confirmed']-covid_data_3['confirmed'].shift(1)
    covid_data_3['Rolling Ave'] = covid_data_3['daily confirmed'].rolling(window=7).mean()
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=covid_data_3['date'].tail(30),
            y=covid_data_3['daily confirmed'].tail(30),
            name = '????????????????????????',
            marker = dict(color='orange'),
            hoverinfo='text',
            hovertext=
            '<b>??????</b>:' + covid_data_3['date'].tail(30).astype(str) + '<br>' +
            '<b>???????????????</b>:' + [f'{x:,.0f}' for x in covid_data_3['daily confirmed'].tail(30)] + '<br>' +
            '<b>??????</b>:' + covid_data_3['Country/Region'].tail(30).astype(str) + '<br>'
        )
    )

    fig.add_trace(
        go.Scatter(
            x=covid_data_3['date'].tail(30),
            y=covid_data_3['Rolling Ave'].tail(30),
            name = '7???????????????',
            line = dict(color='white',width=3),
            mode='lines',
            hoverinfo='text',
            hovertext=
            '<b>??????</b>:' + covid_data_3['date'].tail(30).astype(str) + '<br>' +
            '<b>???????????????</b>:' + [f'{x:,.0f}' for x in covid_data_3['Rolling Ave'].tail(30)] + '<br>'
        )
    )

    fig.update_layout(
        title={
                'text': w_countries + '??????30????????????????????????',
                'y': 0.93,
                'x': 0.5,
                'xanchor':'center',
                'yanchor':'top'
        },
        titlefont={
                'color':'white',
                'size':20
        },
        font=dict(
            family='sans-serif',
            color='white',
            size=12
        ),
        legend={
            'orientation':'h',
            'xanchor':'center',
            'x':0.5,
            'y':-0.2
        },
        paper_bgcolor="#222",
        plot_bgcolor="#222",
        xaxis=dict(
            title='<b>??????</b>',
            color='white',
            showline=True,
            showgrid=True,
            tickformat='%y-%m-%d',
            linewidth=1,
            ticks='outside'
        ),
        yaxis=dict(
            title='<b>???????????????</b>',
            color='white',
            showline=True,
            showgrid=True,
        )
        
    )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)







