from dash import Dash, html, dcc, Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__,external_stylesheets=external_stylesheets)
app.layout = html.Div([
    dcc.RangeSlider(0, 20, 1, value=[5, 15], id='my-range-slider'),
    html.Div(id='output-container-range-slider')
])

@app.callback(
    Output('output-container-range-slider','children'),
    Input('my-range-slider','value')
)
def update_output(value):
    return "you have selected '{}'".format(value)

if __name__ == '__main__':
    app.run_server(debug=True)
