from dash import Dash
import dash_bootstrap_components as dbc
from dash import html

app = Dash(__name__,external_stylesheets=[dbc.themes.DARKLY])

app.layout = dbc.Container([
    dbc.Row(
        dbc.Col('A single column',class_name="m-5 pt-5")
    ),
    dbc.Row(
        [
            dbc.Col("one of three columns",class_name="col-3"),
            dbc.Col("one of three columns",class_name="col-6"),
            dbc.Col("onew of three columns",class_name="col-3")
        ]
    )
],fluid=True)

if __name__ == "__main__":
    app.run_server(debug=True)