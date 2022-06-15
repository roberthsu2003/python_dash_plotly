import pandas as pd
from dash import Dash,html,dcc,Input,Output
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

sales = pd.read_csv('train2.csv')
sales['Order Date'] = pd.to_datetime(sales['Order Date'],format='%d/%m/%Y')
sales['Year'] = sales['Order Date'].dt.year
sales['Month'] = sales['Order Date'].dt.month_name()
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
                    id='sub_category',
                    value='消費者',
                    inline=False,
                    style={'width':'100px','lineHeight':'30px','marginLeft':'auto'},
                    className='h6',
                    inputClassName='me-1'
                ),

        ],width=2)
    ]),
    dbc.Row([
            dbc.Col([
                html.H5('子類別或地區',className='mb-3'),
                dcc.RadioItems(
                    ["子類別","地區"],
                    id='sub_segment',
                    value='子類別',
                    className='h6',
                    inputClassName='me-1',
                    labelClassName='ps-3'
                ),
                dcc.Graph(id='bar_chart_1', config={'displayModeBar':'hover'})
                ],width=3),
            dbc.Col([
                dcc.Graph(id='donut_chart')
            ], width=3),
            dbc.Col([
                dcc.Graph(id='line_chart')
            ], width=4),
            dbc.Col("third", width=2)
    ],className='pt-5'),
    
],class_name="py-5")

@app.callback(
    Output('bar_chart_1','figure'),
    [Input('select_years','value'),
     Input('sub_category','value'),
     Input('sub_segment','value')
    ]
)
def update_barChart(select_years,sub_category,sub_segment):
    sales1 = sales.groupby(['Year', '子類別', '部分'])['Sales'].sum().reset_index()
    sales2 = sales1[(sales1['Year'] == select_years) & (sales1['部分'] == sub_category)].sort_values(by='Sales',ascending=False).nlargest(5,columns=['Sales'])
    sales3 = sales.groupby(['Year', '地區', '部分'])['Sales'].sum().reset_index()
    sales4 = sales3[(sales3['Year'] == select_years) & (sales3['部分'] == sub_category)].sort_values(by='Sales', ascending=False)
    fig = go.Figure()
    if sub_segment == '子類別':
        fig.add_trace(
            go.Bar(
                x=sales2['Sales'],
                y=sales2['子類別'],
                text=sales2['子類別'],
                texttemplate=[f'{x:,.0f}美金' for x in sales2['Sales']],
                textposition='auto',
                orientation='h',
                marker=dict(color='#19AAE1'),
                hoverinfo='text',
                hovertext=
                '<b>年度</b>' + sales2['Year'].astype(str) + '<br>' +
                '<b>區域</b>' + sales2['部分'].astype(str) + '<br>' +
                '<b>類別</b>' + sales2['子類別'].astype(str) + '<br>' +
                '<b>銷售額</b>' + [f'{x:,.0f}美金' for x in sales2['Sales']] + '<br>'
            )
        )
        fig.update_layout(
            title={
                'text': str(select_years) + sub_category +'<br>子類別銷售金額',
                'x':0.5,
                'y':0.9,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            title_font={
                'color':'#0f5132',
                'size':20
            },
            hovermode='closest',
            paper_bgcolor="#fff",
            plot_bgcolor="#fff",
            margin_l=0,
            margin_r=0
        )
        fig.update_xaxes(
            dict(
                title='<b>金額</b>',
                ticks='outside',
                showgrid=False
            )
        )
        fig.update_yaxes(
            dict(
                title='<b>子類別</b>',
                ticks='outside',
                showgrid=False
            )
        )

        return fig
    elif(sub_segment == '地區'):
        fig.add_trace(
            go.Bar(
                x=sales4['Sales'],
                y=sales4['地區'],
                text=sales4['地區'],
                texttemplate=[f'{x:,.0f}美金' for x in sales4['Sales']],
                textposition='auto',
                orientation='h',
                marker=dict(color='#19AAE1'),
                hoverinfo='text',
                hovertext=
                '<b>年度</b>' + sales4['Year'].astype(str) + '<br>' +
                '<b>區域</b>' + sales4['部分'].astype(str) + '<br>' +
                '<b>地區</b>' + sales4['地區'].astype(str) + '<br>' +
                '<b>銷售額</b>' + [f'{x:,.0f}美金' for x in sales4['Sales']] + '<br>'
            )
        )
        fig.update_layout(
            title={
                'text': str(select_years) + sub_category + '<br>地區銷售金額',
                'x': 0,
                'y': 0.9,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            title_font={
                'color': '#0f5132',
                'size': 20
            },
            hovermode='closest',
            paper_bgcolor="#fff",
            plot_bgcolor="#fff",
            margin_l=0,
            margin_r=0
        )
        fig.update_xaxes(
            dict(
                title='<b>金額</b>',
                ticks='outside',
                showgrid=False
            )
        )
        fig.update_yaxes(
            dict(
                title='<b>地區</b>',
                ticks='outside',
                showgrid=False
            )
        )

        return fig
@app.callback(
    Output('donut_chart','figure'),
    [Input('select_years','value'),
     Input('sub_category','value')
    ]
)

def update_donut_chart(select_years, sub_category):
    sales5 = sales.groupby(['Year', '類別', '部分'])['Sales'].sum().reset_index()
    sales_furniture = sales5[(sales5['Year'] == select_years) & (sales5['部分'] == sub_category) & (sales5['類別'] == '家具')]['Sales'].sum()
    sales_office = sales5[(sales5['Year'] == select_years) & (sales5['部分'] == sub_category) & (sales5['類別'] == '辦公用品')]['Sales'].sum()
    sales_technology = sales5[(sales5['Year'] == select_years) & (sales5['部分'] == sub_category) & (sales5['類別'] == '技術')]['Sales'].sum()

    fig = go.Figure()
    colors=['#FF00FF', '#9C0C38', 'orange']
    fig.add_trace(
        go.Pie(
            labels=sales['類別'].unique(),
            values=[sales_furniture, sales_office, sales_technology],
            textinfo='label+percent',
            hoverinfo='label+value+percent',
            texttemplate='%{label} <br>%{percent}',
            textposition='auto',
            textfont=dict(
                color='white',
                size=15
            ),
            insidetextorientation='auto',
            hole=.3
        )
    )

    fig.update_layout(
        title = {
            'text': str(select_years) + ' ' +str(sub_category)+'<br>'+ '類別銷售比例',
            'y':0.95,
            'x':0.5,
            'xanchor':'center',
            'yanchor':'top'
        },
        titlefont = {
            'color':'#0f5132',
            'size':20
        },
        showlegend=False,
        margin=dict(
            l = 0,
            r = 0,
            t = 170
        ),
        height = 500,
    )

    return fig

@app.callback(
    Output('line_chart','figure'),
    [Input('select_years','value'),
     Input('sub_category','value')
    ]
)

def update_line_chart(select_years, sub_category):
    sales6 = sales.groupby(['Year', 'Month', '部分'])['Sales'].sum().reset_index()
    sales7 = sales6[(sales6['Year'] == select_years) & (sales6['部分'] == sub_category)]
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=sales7['Month'],
            y=sales7['Sales'],
            text = sales7['Sales'],
            texttemplate='$' + '%{text:,.2s}',
            textposition='bottom left',
            line=dict(
                width=3,
                color='#FF00FF'
            ),
            marker=dict(
                color='#19AAE1',
                size=10,
                symbol='circle',
                line=dict(
                    color='#19AAE1',
                    width=2
                )
            ),
            hoverinfo='text',
            hovertext=
            '<b>年度</b>:' + sales7['Year'].astype(str) + '<br>' +
            '<b>月份</b>:' + sales7['Month'].astype(str) + '<br>' +
            '<b>客戶</b>:' + sales7['部分'].astype(str) + '<br>' +
            '<b>銷售額:</b>' + [f'{x:,.0f}' for x in sales7['Sales']] + '<br>'
        )
    )

    fig.update_layout(
        title = {
            'text': str(select_years) + ' ' +str(sub_category)+'<br>'+ '類別銷售比例',
            'y':0.95,
            'x':0.5,
            'xanchor':'center',
            'yanchor':'top'
        },
        titlefont = {
            'color':'#0f5132',
            'size':20
        },
        showlegend=False,
        margin=dict(
            l = 0,
            r = 0,
            t = 170
        ),
        height = 500,
    )

    return fig
if __name__ == "__main__":
    app.run_server(debug=True)