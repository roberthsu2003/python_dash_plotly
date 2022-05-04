import dash
from dash import html
from dash import dcc


app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Dropdown([{'label':'blue','value':'blue'},
                  {'label':'green','value':'green'},
                  {'label':'yellow','value':'yellow'}
                  ]),
    html.Div()
])

if __name__ == '__main__':
    app.run_server(debug=True)
