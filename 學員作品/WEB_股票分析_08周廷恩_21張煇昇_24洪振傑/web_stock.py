import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objs as go
from datetime import timedelta
import numpy as np
import train_model

app1 = dash.Dash(__name__,requests_pathname_prefix='/tech/')

# 讀取數據並提取日期範圍
data = pd.read_csv('2330.csv')
data['Date'] = pd.to_datetime(data['Date'])
min_date = data['Date'].min()
max_date = data['Date'].max()

def generate_date_options(start_date, end_date):
    years = range(start_date.year, end_date.year + 1)
    months = range(1, 13)
    days = range(1, 32)  # 默認最多31天

    year_options = [{'label': str(year), 'value': year} for year in years]
    month_options = [{'label': f'{month:02}', 'value': month} for month in months]
    day_options = [{'label': f'{day:02}', 'value': day} for day in days]

    return year_options, month_options, day_options

year_options, month_options, day_options = generate_date_options(min_date, max_date)

app1.layout = html.Div(
    style={'width': '80%', 'margin': 'auto', 'border': '2px solid black'},
    children=[
        html.Div(
            children=html.H1("預測台股"),
            style={'textAlign': 'center', 'padding': '10px'}
        ),
        html.Div(
            style={'border': '2px solid green', 'padding': '10px', 'margin': '10px 0'},
            children=[
                html.Label('股票代碼:', style={'margin-right': '10px'}),
                dcc.Input(id='stock-code', type='text', value='2330', style={'margin-right': '20px'})
            ]
        ),
        html.Div(
            style={'border': '2px solid blue', 'padding': '10px', 'margin': '10px 0'},
            children=[
                html.Div(
                    style={'display': 'flex', 'justify-content': 'space-between', 'margin-bottom': '10px'},
                    children=[
                        html.Div(
                            style={'display': 'flex', 'align-items': 'center', 'width': '100%'},
                            children=[
                                html.Label('開始年:', style={'margin-right': '10px'}),
                                dcc.Dropdown(
                                    id='start-year-dropdown',
                                    options=year_options,
                                    value=min_date.year,
                                    clearable=False,
                                    style={'width': '100px', 'margin-right': '10px'}
                                ),
                                html.Label('開始月:', style={'margin-right': '10px'}),
                                dcc.Dropdown(
                                    id='start-month-dropdown',
                                    options=month_options,
                                    value=min_date.month,
                                    clearable=False,
                                    style={'width': '100px', 'margin-right': '10px'}
                                ),
                                html.Label('開始日:', style={'margin-right': '10px'}),
                                dcc.Dropdown(
                                    id='start-day-dropdown',
                                    options=day_options,
                                    value=min_date.day,
                                    clearable=False,
                                    style={'width': '100px'}
                                ),
                            ]
                        )
                    ]
                ),
                html.Div(
                    style={'display': 'flex', 'justify-content': 'space-between'},
                    children=[
                        html.Div(
                            style={'display': 'flex', 'align-items': 'center', 'width': '100%'},
                            children=[
                                html.Label('結束年:', style={'margin-right': '10px'}),
                                dcc.Dropdown(
                                    id='end-year-dropdown',
                                    options=year_options,
                                    value=max_date.year,
                                    clearable=False,
                                    style={'width': '100px', 'margin-right': '10px'}
                                ),
                                html.Label('結束月:', style={'margin-right': '10px'}),
                                dcc.Dropdown(
                                    id='end-month-dropdown',
                                    options=month_options,
                                    value=max_date.month,
                                    clearable=False,
                                    style={'width': '100px', 'margin-right': '10px'}
                                ),
                                html.Label('結束日:', style={'margin-right': '10px'}),
                                dcc.Dropdown(
                                    id='end-day-dropdown',
                                    options=day_options,
                                    value=max_date.day,
                                    clearable=False,
                                    style={'width': '100px'}
                                ),
                            ]
                        )
                    ]
                )
            ]
        ),
        html.Div(
            style={'display': 'flex', 'justify-content': 'space-around', 'border': '2px solid yellow', 'padding': '10px', 'margin': '10px 0'},
            children=[
                html.Div(
                    children=[dcc.Graph(id='k-line-chart', style={'height': '400px', 'width': '100%'})],
                    style={'width': '45%', 'border': '2px solid orange', 'padding': '10px'}
                ),
                html.Div(
                    children=[dcc.Graph(id='macd-chart', style={'height': '400px', 'width': '100%'})],
                    style={'width': '45%', 'border': '2px solid orange', 'padding': '10px'}
                )
            ]
        ),
        html.Div(
            style={'border': '2px solid brown', 'padding': '10px', 'margin': '10px 0'},
            children=[
                html.Div(
                    style={'display': 'flex', 'justify-content': 'space-around', 'padding': '10px'},
                    children=[
                        html.Div(
                            html.Label('熱力圖:', style={'margin-right': '10px'}),
                        )
                    ]
                ),
                html.Div(
                    children=[dcc.Graph(id='heatmap-chart')],
                    style={'border': '2px solid brown', 'padding': '10px'}
                )
            ]
        ),
        # Analysis Section
        html.Div(
            style={'border': '2px solid brown', 'padding': '10px', 'margin': '10px 0'},
            children=[
                html.Div(
                    style={'display': 'flex', 'justify-content': 'space-around', 'padding': '10px'},
                    children=[
                        html.Div(
                            children=[
                                dcc.RadioItems(
                                    id='analysis-radio',
                                    options=[
                                        {'label': '分類', 'value': 'classification'},
                                        {'label': '回歸', 'value': 'regression'}
                                    ],
                                    value='classification',
                                    labelStyle={'display': 'inline-block', 'margin-right': '10px'}
                                ),
                                dcc.Dropdown(
                                    id='feature-dropdown',
                                    value='決策樹(C)',
                                    clearable=False,
                                )
                            ]
                        )
                    ]
                ),
                html.Div(id='model-info', style={ 'padding': '10px', 'width': '80%', 'margin-left': '10px'}),
                html.Div(
                    children=[
                        dcc.Graph(id='analysis-chart', style={'width': '70%'})
                    ],
                    style={'border': '2px solid brown', 'padding': '10px'}
                )
            ]
        )
    ]
)

@app1.callback(
    Output('feature-dropdown', 'options'),
    Input('analysis-radio', 'value')
)
def update_feature_dropdown(selected_analysis):
    if selected_analysis == 'regression':
        regression_model=['決策樹(R)','Linear_regression']
        return [{'label': f'{i}', 'value': f'{i}'} for i in regression_model]
    else:  # classification
        classification_model=['決策樹(C)','Logisticregression']
        return [{'label': f'{i}', 'value': f'{i}'} for i in classification_model]


@app1.callback(
    Output('k-line-chart', 'figure'),
    Output('macd-chart', 'figure'),
    Output('heatmap-chart', 'figure'),
    Input('stock-code', 'value'),
    Input('start-year-dropdown', 'value'),
    Input('start-month-dropdown', 'value'),
    Input('start-day-dropdown', 'value'),
    Input('end-year-dropdown', 'value'),
    Input('end-month-dropdown', 'value'),
    Input('end-day-dropdown', 'value'),
)
def update_charts(stock_code, start_year, start_month, start_day, end_year, end_month, end_day):
    start_date = pd.Timestamp(year=start_year, month=start_month, day=start_day)
    end_date = pd.Timestamp(year=end_year, month=end_month, day=end_day)
    
    data = pd.read_csv(f"{stock_code}.csv")
    data['Date'] = pd.to_datetime(data['Date'])
    data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
    
    fig_candlestick = create_candlestick_chart(data)
    fig_macd = create_macd_chart(data)
    fig_heatmap = create_heatmap_chart(data)
    
    return fig_candlestick, fig_macd, fig_heatmap

def create_candlestick_chart(data):
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=data['Date'],
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name='Candlestick'
    ))
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=data['upperband'],
        mode='lines',
        name='Upper Band',
        line=dict(color='blue', width=1, dash='dash')
    ))
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=data['ma'],
        mode='lines',
        name='Price (MA)',
        line=dict(color='black', width=1)
    ))
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=data['lowerband'],
        mode='lines',
        name='Lower Band',
        line=dict(color='red', width=1, dash='dash')
    ))
    fig.update_layout(
        title='K線圖與折線圖',
        xaxis_title='日期',
        yaxis_title='價格',
        xaxis_rangeslider_visible=False,
        autosize=True
    )
    return fig

def create_macd_chart(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=data['MACD'],
        mode='lines',
        name='MACD',
        line=dict(color='red')
    ))
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=data['Signal_Line'],
        mode='lines',
        name='Signal Line',
        line=dict(color='yellow')
    ))
    fig.add_trace(go.Bar(
        x=data['Date'],
        y=data['MACD_Histogram'],
        name='MACD Histogram',
        marker=dict(color=['red' if val >= 0 else 'green' for val in data['MACD_Histogram']]),
        opacity=0.7
    ))
    fig.update_layout(
        title='MACD 圖',
        xaxis_title='日期',
        yaxis_title='MACD',
        autosize=True
    )
    return fig

def create_heatmap_chart(data):
    # 示例數據和生成方式，替換為實際的數據處理
    corr_matrix = data.iloc[:, 1:].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='Viridis'
    ))
    
    fig.update_layout(
        title='熱力圖',
        xaxis_title='特徵',
        yaxis_title='特徵',
        autosize=True,
        xaxis=dict(
            showgrid=True,  # 顯示網格線
            gridcolor='black',  # 網格線顏色
            gridwidth=0.5  # 網格線寬度
        ),
        yaxis=dict(
            showgrid=True,  # 顯示網格線
            gridcolor='black',  # 網格線顏色
            gridwidth=0.5  # 網格線寬度
        )
    )
    
    return fig

@app1.callback(
    [Output('analysis-chart', 'figure'),
     Output('model-info', 'children')],
    Input('feature-dropdown', 'value')
)
def update_analysis_chart(selected_model):
    feature = ['Open', 'High', 'Low', 'Adj Close', 'EMA12']
    
    try:
        if selected_model == "決策樹(R)":
            mse, r2, y_predict, tolerance_percentage, correct_within_tolerance, fig = train_model.Decision_tree_Regressor(test_size=0.3, data=data, feature=feature)
            info = f"均方誤差: {mse:.4f}\nR^2 分數: {r2:.4f}\n容忍百分比: {tolerance_percentage:.2%}\n容忍內正確率: {correct_within_tolerance:.2f}%"
        elif selected_model == "Linear_regression":
            mse, r2, y_predict, tolerance_percentage, correct_within_tolerance, fig = train_model.Linear_regression(test_size=0.3, data=data, feature=feature)
            info = f"均方誤差: {mse:.4f}\nR^2 分數: {r2:.4f}\n容忍百分比: {tolerance_percentage:.2%}\n容忍內正確率: {correct_within_tolerance:.2f}%"
        elif selected_model == "決策樹(C)":
            score, y_predict, f1, fig = train_model.Decision_tree_Classifier(test_size=0.3, data=data, feature=feature)
            info = f"準確率分數: {score:.4f}\nF1 分數: {f1:.4f}"
        elif selected_model == "Logisticregression":
            score, y_predict, f1, fig = train_model.Logisticregression(test_size=0.3, data=data, feature=feature)
            info = f"準確率分數: {score:.4f}\nF1 分數: {f1:.4f}"
        else:
            fig = go.Figure()
            fig.update_layout(
                title='請選擇模型',
                xaxis_title='',
                yaxis_title='',
                autosize=True
            )
            info = "請選擇有效的模型"
        
        return fig, html.Div(info, style={'white-space': 'pre-line', 'font-family': 'monospace'})
    except Exception as e:
        print(f"錯誤: {e}")
        fig = go.Figure()
        fig.update_layout(
            title='錯誤',
            xaxis_title='',
            yaxis_title='',
            autosize=True
        )
        info = f"發生錯誤: {e}"
        return fig, html.Div(info, style={'white-space': 'pre-line', 'font-family': 'monospace'})

if __name__ == '__main__':
    app1.run_server(debug=True)
