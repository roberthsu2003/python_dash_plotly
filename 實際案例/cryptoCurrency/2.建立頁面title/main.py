
from dash import dcc,html,Dash,Input,Output
import dash_bootstrap_components as dbc
meta_tags = [{'name':'viewport', 'content':'width=device-width'}]
app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP],meta_tags=meta_tags)
app.layout = dbc.Container(children=[
    dbc.Row(children=[
        dbc.Col(
            children=html.Div([
                html.Img(src=app.get_asset_url('monetization_on_FILL1_wght700_GRAD200_opsz48.png'),),
                html.B("加密貨幣及時資料",className='h2 align-middle')
            ]),
            width=12,
            lg=6
        ),
        dbc.Col(
            children=html.H3('2021-11-25 22:45:15',
                             className="text-end"),
            width=12,
            lg=6
        )
    ],justify='between',class_name='pt-3')
])

if __name__ == "__main__":
    app.run_server(debug=True)