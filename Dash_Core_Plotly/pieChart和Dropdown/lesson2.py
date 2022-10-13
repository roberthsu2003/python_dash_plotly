from dash import Dash, dcc, html, Input, Output
import plotly.express as px

app = Dash(__name__)

app.layout = html.Div([
    html.H4('Analysis of the restaurant sales'),
    dcc.Graph(id='graph'),
    html.P("Names:"),
    dcc.Dropdown(
        id='names',
        options = ['smoker', 'day', 'time', 'sex'],
        value='day',
        clearable=False
    ),
    html.P("Values:"),
    dcc.Dropdown(
        id = 'values',
        options = ['total_bill', 'tip', 'size'],
        value='total_bill', clearable=False
    )
])

@app.callback(
    Output("graph", "figure"),
    Input("names","value"),
    Input('values','value')
)
def generate_chart(names, values):
    df = px.data.tips()
    fig = px.pie(df, values=values, names=names, hole=.3)
    return fig

app.run_server(debug=True)
