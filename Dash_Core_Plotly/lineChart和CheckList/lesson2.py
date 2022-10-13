from dash import Dash,html,dcc

app = Dash(__name__)
app.layout = html.Div(
    dcc.Checklist(
        ['New York City', 'Montréal', 'San Francisco'],
        ['New York City', 'Montréal']
    )
)

if __name__ == "__main__":
    app.run_server(debug=True)