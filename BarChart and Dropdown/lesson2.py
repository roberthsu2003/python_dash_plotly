from dash import Dash,dcc,html

dcc.Dropdown(
    ['New York City', 'Montreal', 'San Francisco'],
    ['Montreal', 'San Francisco'],
    multi=True
)

app = Dash(__name__)
app.layout = html.Div(
    dcc.Dropdown(
    ['New York City', 'Montreal', 'San Francisco'],
    ['Montreal', 'San Francisco'],
    multi=True
)
)
if __name__ == '__main__':
    app.run_server(debug=True)