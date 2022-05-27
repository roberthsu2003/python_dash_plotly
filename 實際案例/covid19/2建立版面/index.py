from importlib import import_module
from pydoc import classname
from dash import Dash,html,dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd

url_confirmed = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
url_deaths = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
url_recovered = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'

confirmed = pd.read_csv(url_confirmed)
deaths = pd.read_csv(url_deaths)
recovered = pd.read_csv(url_recovered)

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

#建立dash
app = Dash(__name__,external_stylesheets=[dbc.themes.DARKLY])
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.Img(src=app.get_asset_url('corona-logo-1.jpg'),className="p-2",style={'width':'200px','height':'auto'})
            ,width=4),
        dbc.Col("title",width=4),
        dbc.Col("說明",width=4)
    ])
])
if __name__ == '__main__':
    app.run_server(debug=True)







