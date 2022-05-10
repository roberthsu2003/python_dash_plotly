from dash import Dash, dcc, html, Input, Output
from plotly.express import data
import pandas as pd

df =  data.medals_long()
print(df)

app = Dash(__name__)
app.layout = html.Div([
    dcc.Dropdown(df.nation.unique(), id='pandas-dropdown-2'),
    html.Div(id='pandas-output-container-2')
])


@app.callback(
    Output('pandas-output-container-2', 'children'),
    Input('pandas-dropdown-2', 'value')
)
def update_output(value):
    return f'You have selected {value}'


if __name__ == '__main__':
    app.run_server(debug=True)
