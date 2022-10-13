from dash import Dash, dcc, html, Input, Output
import plotly.express as px

app = Dash(__name__)

app.layout = html.Div([
    html.H4('Stock price analysis'),
    dcc.Graph(id='time-series-chart'),
    html.P("Select stock:"),
    dcc.Dropdown(
        id='ticker',
        options=["AMZN", "FB", "NFLX"],
        value="AMZN",
        clearable=False
    )
])

@app.callback(
    Output('time-series-chart','figure'),
    Input('ticker','value')
)
def display_time_series(ticker):
    df = px.data.stocks()
    fig = px.line(df,x='date', y=ticker)
    return fig

app.run_server(debug=True)