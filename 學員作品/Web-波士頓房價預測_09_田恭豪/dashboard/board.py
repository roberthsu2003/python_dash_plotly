import dash
from dash import dcc, html, dash_table
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import io
import base64
import matplotlib
from scipy import stats
import numpy as np
import os

# 使用 'Agg' 後端來處理圖片渲染
matplotlib.use('Agg')

app1 = dash.Dash(__name__, requests_pathname_prefix='/app1/', external_stylesheets=[dbc.themes.BOOTSTRAP])
app1.title = '特徵數據'

# 設定資料集檔案的絕對路徑
absolute_path = os.path.join(os.getcwd(), 'train_dataset.csv')

# 檢查檔案是否存在
if os.path.exists(absolute_path):
    print("檔案存在")
    df = pd.read_csv(absolute_path)
else:
    print("檔案不存在")
    df = None

# Function to remove outliers
def remove_outliers(data):
    return data[(data - data.mean()).abs() < 3 * data.std()]

# Clean all features by removing outliers
df_cleaned = df.copy()
for column in df.columns:
    df_cleaned[column] = remove_outliers(df_cleaned[column])

# Function to create figure for the given feature with various transformations
def create_figure(feature, transformation):
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    if feature == 'CHAS':
        sns.countplot(x=feature, data=df, ax=axes[0])
        axes[0].set_title(f'{feature} 頻率分佈圖')
        axes[0].set_xlabel(feature)
        axes[0].set_ylabel('Count')
        
        sns.histplot(df[feature], kde=True, ax=axes[1])
        axes[1].set_title(f'{feature} 分佈圖 (原始數據)')
        axes[1].set_xlabel(feature)
        axes[1].set_ylabel('Count')
    else:
        data = df[feature].copy()
        data = remove_outliers(data)

        sns.histplot(df[feature], kde=True, ax=axes[0])
        axes[0].set_title(f'{feature} 分佈圖 (原始數據)')
        axes[0].set_xlabel(feature)
        axes[0].set_ylabel('Count')

        if transformation == '對數轉換':
            if (data > 0).all():
                transformed_data = np.log(data)
                title = f'{feature} 分佈圖 (對數轉換)'
                xlabel = f'Log({feature})'
            else:
                transformed_data = data
                title = f'{feature} 分佈圖 (對數轉換)'
                xlabel = '資料中包含非正數'
        elif transformation == '平方根轉換':
            if (data >= 0).all():
                transformed_data = np.sqrt(data)
                title = f'{feature} 分佈圖 (平方根轉換)'
                xlabel = f'Sqrt({feature})'
            else:
                transformed_data = data
                title = f'{feature} 分佈圖 (平方根轉換)'
                xlabel = '資料中包含負數'
        elif transformation == '立方根轉換':
            transformed_data = np.cbrt(data)
            title = f'{feature} 分佈圖 (立方根轉換)'
            xlabel = f'Cbrt({feature})'
        elif transformation == '次方轉換':
            if data.skew() < 0:
                power = 0.25
                transformed_data = np.power(data, power)
                title = f'{feature} 分佈圖 (次方轉換)'
                xlabel = f'Power({feature}, {power})'
            else:
                transformed_data = data
                title = f'{feature} 分佈圖 (次方轉換)'
                xlabel = '資料無左偏'
        elif transformation == 'Box-Cox 轉換':
            if (data > 0).all():
                transformed_data, _ = stats.boxcox(data)
                title = f'{feature} 分佈圖 (Box-Cox 轉換)'
                xlabel = f'Box-Cox({feature})'
            else:
                transformed_data = data
                title = f'{feature} 分佈圖 (Box-Cox 轉換)'
                xlabel = '資料中包含非正數'
        else:
            transformed_data = data
            title = '未選擇修正方法'
            xlabel = '選擇修正方法'

        sns.histplot(transformed_data, kde=True, ax=axes[1])
        axes[1].set_title(title)
        axes[1].set_xlabel(xlabel)
        axes[1].set_ylabel('Count')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return buf

def encode_image(buf):
    encoded = base64.b64encode(buf.read()).decode('ascii')
    buf.close()
    return encoded

# Define the layout of the app
app1.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("特徵常態分佈圖"), width=12),
    ], style={'textAlign': 'center', 'backgroundColor': '#f8f9fa', 'padding': '20px'}),

    dbc.Row([
        dbc.Col(
            html.Button("查看資料分布狀況", id="collapse-button", n_clicks=0),
            width={'size': 6},
            style={'textAlign': 'center', 'padding': '10px'}
        )
    ], style={'display': 'flex', 'justify-content': 'center'}),

    dbc.Row([
        dbc.Col(
            dbc.Collapse(
                id='collapse',
                is_open=False,
                children=[
                    dash_table.DataTable(
                        id='data-describe',
                        columns=[{'name': '統計量', 'id': 'statistics'}] + [{'name': i, 'id': i} for i in df_cleaned.describe().columns],
                        data=[{'statistics': stat, **row} for stat, row in zip(['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max'], df_cleaned.describe().reset_index().to_dict('records'))],
                        style_table={'overflowX': 'auto'},
                        style_cell={'textAlign': 'left', 'minWidth': '100px', 'width': '150px', 'maxWidth': '200px'}
                    )
                ]
            ),
            width=12
        )
    ]),

    dbc.Row([
        dbc.Col(
            html.Div([
                html.Label("選擇特徵"),
                dcc.Dropdown(
                    id='feature-dropdown',
                    options=[{'label': col, 'value': col} for col in df.columns if col != 'PRICE'],
                    value=df.columns[0]
                ),
            ]),
            width=4,
            style={'textAlign': 'center'}
        ),
        dbc.Col(
            html.Div([
                html.Label("選擇修正方法"),
                dcc.Dropdown(
                    id='transformation-dropdown',
                    options=[
                        {'label': '對數轉換 (資料不能有0或負數)', 'value': '對數轉換'},
                        {'label': '平方根轉換 (資料不能是負數)', 'value': '平方根轉換'},
                        {'label': '立方根轉換', 'value': '立方根轉換'},
                        {'label': '次方轉換 (只能處理左偏)', 'value': '次方轉換'},
                        {'label': 'Box-Cox 轉換', 'value': 'Box-Cox 轉換'}
                    ],
                    value='對數轉換'
                ),
            ]),
            width=4,
            style={'textAlign': 'center'}
        )
    ], style={'display': 'flex', 'justify-content': 'center'}),

    dbc.Row([
        dbc.Col(html.Img(id='feature-image'), width=12)
    ])
], fluid=True)

@app1.callback(
    Output('feature-image', 'src'),
    [Input('feature-dropdown', 'value'),
     Input('transformation-dropdown', 'value')]
)
def update_image(selected_feature, selected_transformation):
    try:
        buf = create_figure(selected_feature, selected_transformation)
        encoded_image = encode_image(buf)
        return 'data:image/png;base64,{}'.format(encoded_image)
    except Exception as e:
        print(f"Error: {e}")
        return "data:image/png;base64,"

@app1.callback(
    Output('collapse', 'is_open'),
    [Input('collapse-button', 'n_clicks')],
    [dash.dependencies.State('collapse', 'is_open')]
)
def toggle_collapse(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open
