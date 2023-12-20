from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

dash1 = Dash(requests_pathname_prefix="/dash/app1/",external_stylesheets=[dbc.themes.BOOTSTRAP])

dash1.title = "台灣和日本平均壽命"

dash1.layout = html.Div([
    html.H4('Life expentancy progression of countries per continents'),
    dcc.Graph(id="graph"),
    dcc.Checklist(
        id="checklist",
        options=["Asia", "Europe", "Africa","Americas","Oceania"],
        value=["Americas", "Oceania"],
        inline=True
    ),
])

@dash1.callback(
    Output("graph", "figure"), 
    Input("checklist", "value"))
def update_line_chart(continents):
    df = px.data.gapminder() # replace with your own data source
    mask = df.continent.isin(continents)
    fig = px.line(df[mask], 
        x="year", y="lifeExp", color='country')
    return fig