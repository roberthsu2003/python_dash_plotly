
from dash import dcc,html,Dash,Input,Output
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from datetime import datetime

meta_tags = [{'name':'viewport', 'content':'width=device-width'}]
app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP],meta_tags=meta_tags)
app.layout = dbc.Container(children=[
    dbc.Row(children=[
        dbc.Col(
            children=html.Div([
                html.Img(src=app.get_asset_url('monetization_on_FILL1_wght700_GRAD200_opsz48.png'),),
                html.B("加密貨幣及時資料",className='h2 align-middle')
            ],className='text-lg-start text-center mt-3'),
            width=12,
            lg=6
        ),
        dbc.Col(
            children=[
                html.H3(id='date_time_component',
                        className="text-lg-end text-center mt-3"),
                dcc.Interval(id="interval-component",
                             interval=1*1000,
                             n_intervals=0)
            ],
            width=12,
            lg=6
        )
    ],justify='between',class_name='pt-3'),

])

@app.callback(Output('date_time_component','children'),
             Input('interval-component','n_intervals'))
def update_date_time(n_interval):
    if n_interval == 0:
        raise PreventUpdate
    else:
        now = datetime.now()
        dt_string = now.strftime("%Y-%m_%d %H:%M:%S")
        return html.Span(dt_string)

if __name__ == "__main__":
    app.run_server(debug=True)