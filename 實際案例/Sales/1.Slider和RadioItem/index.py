import pandas as pd
from dash import Dash,html,dcc
import plotly.express as px
import dash_bootstrap_components as dbc

sales = pd.read_csv('train2.csv')
sales['Order Date'] = pd.to_datetime(sales['Order Date'],format='%d/%m/%Y')
sales['Year'] = sales['Order Date'].dt.year
segment = sales['部分'].unique()

app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            dbc.Alert('銷售統計表',id='title',class_name='text-center h3 w-75'),
            width=4
        ),
        dbc.Col([html.H5(
            "選取銷售年度:"
        ),
        dcc.Slider(
            id = 'select_years',
            min = sales['Year'].min(),
            max = sales['Year'].max(),
            step=None,
            value = 2018,
            marks = {yr:{'label':str(yr),'style':{'fontSize':'1.2rem'}} for yr in range(sales['Year'].min(),sales['Year'].max()+1)},
            tooltip={'placement':'top', 'always_visible':True},
            included=False
        )
        ],width=6),
        dbc.Col([
                html.H5('消費者類型:',className='text-end'),
                dcc.RadioItems(
                    segment,
                    value='消費者',
                    inline=False,
                    style={'width':'100px','lineHeight':'30px','marginLeft':'auto'},
                    className='h6'
                )
        ],width=2)
    ])
],class_name="py-5")

if __name__ == "__main__":
    app.run_server(debug=True)