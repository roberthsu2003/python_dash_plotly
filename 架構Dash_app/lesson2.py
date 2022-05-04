import dash
from dash import html
from dash import dcc
from dash.dependencies import Output,Input

app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Dropdown(id='color_dropdown',
                 options=[{'label':'blue','value':'blue'},
                  {'label':'green','value':'green'},
                  {'label':'yellow','value':'yellow'}
                  ]),
    html.Div(id='color_output')
])
@app.callback(Output('color_output','children'),
              Input('color_dropdown','value'))
def display_selected_color(color):
    if color is None:
        color = 'nothing'
    return '您選擇了:' + color

if __name__ == '__main__':
    app.run_server(debug=True)
