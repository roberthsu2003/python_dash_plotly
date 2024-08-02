import dash
from dash import Dash, dcc, html, dash_table
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import io
import base64
import matplotlib
from scipy import stats
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
import os

# 設置 matplotlib 使用的字型，選擇支持中文的字型
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# 使用 'Agg' 後端
matplotlib.use('Agg')

# 設定資料集檔案的絕對路徑
absolute_path = os.path.join(os.getcwd(), 'train_dataset.csv')

# 檢查檔案是否存在
if os.path.exists(absolute_path):
    print("檔案存在")
    df = pd.read_csv(absolute_path)
else:
    print("檔案不存在")
    df = None

# 定義移除離群值的函數
def remove_outliers(data):
    return data[(data - data.mean()).abs() < 3 * data.std()]

# 移除所有特徵的離群值
df_clean = df.apply(remove_outliers)

# 移除包含 NaN 的行
df_clean.dropna(inplace=True)

# 定義將圖像緩衝區轉換為 base64 的函數
def encode_image(buf):
    encoded = base64.b64encode(buf.read()).decode('ascii')
    buf.close()
    return encoded

# 初始化 Dash 應用程序
app2 = Dash(__name__, requests_pathname_prefix='/app2/')
app2.title = '模型評估'

# 定義應用程序的佈局
app2.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("演算法評估結果比較"), width=12)
    ], style={'textAlign': 'center',
              'backgroundColor': '#f8f9fa',
              'padding': '10px'
              }),  # 標題行
    dbc.Row(
        children=[
            dbc.Col(dcc.Dropdown(
                id='model-dropdown',
                options=[
                    {'label': '線性回歸(linear-regression)', 'value': 'linear-regression'},
                    {'label': 'K近鄰回歸模型(KNN)', 'value': 'knn'},
                    {'label': 'GridSearchCV(grid-search)', 'value': 'grid-search'},
                    {'label': '決策樹(decision-tree)', 'value': 'decision-tree'},
                    {'label': '隨機森林(random-forest)', 'value': 'random-forest'}
                ],
                placeholder='請選擇模型'
            ), width=20, style={'margin': '5px 100px 10px 0','width': '20%'}),
            dbc.Col(dcc.Input(id='threshold-input', type='number', min=0, max=0.99, step=0.01, disabled=True), width=2, style={'margin-bottom': '10px'}),
            dbc.Col(dbc.Button("查看結果", id='evaluate-button', n_clicks=0), width=4, style={'margin': '0 0 10px 10px'}),
        ],
        style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}
    ),
    dbc.Row([
        dbc.Col(html.Pre(id='evaluation-result', style={'backgroundColor': '#6EACDA', 'padding': '10px', 'border': '1px solid #dee2e6', 'font-size': '18px'}), width=6),
        dbc.Col(html.Pre(id='selected-features', style={'backgroundColor': '#E2E2B6', 'padding': '10px', 'border': '1px solid #dee2e6', 'font-size': '18px'}), width=6)
    ], style={'margin-bottom': '20px'}),  # 顯示評估結果和特徵數及名稱的區域
    dbc.Row([
        dbc.Col(html.H3("紀錄評估分數"), width=12)
    ], style={'margin-bottom': '20px'}),  # 模型評估分數標題
    dbc.Row([
        dbc.Col(dash_table.DataTable(
            id='evaluation-table',
            columns=[
                {'name': '模型名稱', 'id': 'model'},
                {'name': '閾值', 'id': 'threshold'},
                {'name': 'MSE', 'id': 'mse'},
                {'name': 'R-squared', 'id': 'r_squared'},
                {'name': '20%容忍範圍內的正確比率', 'id': 'accuracy'}
            ],
            data=[],  # 初始數據為空
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left', 'minWidth': '100px', 'width': '150px', 'maxWidth': '200px'}
        ), width=12)
    ])  # 顯示模型評估分數的數據表
])

# 儲存結果和選擇的模型
results_store = []
selected_model_store = None
last_threshold = None  # 新增變數以儲存上一次的閾值

@app2.callback(
    [Output('threshold-input', 'disabled'),
     Output('threshold-input', 'value')],
    Input('model-dropdown', 'value')
)
def enable_threshold_input(selected_model):
    # 根據所選擇的模型來啟用或禁用閾值輸入框
    if selected_model is None:
        return True, None  # 若未選擇模型，禁用閾值輸入框
    return False, last_threshold  # 若選擇了模型，啟用閾值輸入框並顯示上一次的閾值

@app2.callback(
    [Output('evaluation-result', 'children'),
     Output('selected-features', 'children'),
     Output('evaluation-table', 'data')],
    Input('evaluate-button', 'n_clicks'),
    [State('model-dropdown', 'value'),
     State('threshold-input', 'value')]
)
def manage_results(evaluate_clicks, selected_model, threshold):
    global results_store, selected_model_store, last_threshold

    invalid_thresholds = ['00', '000', '01', '0001']

    if evaluate_clicks > 0:
        if selected_model is None:
            return '請先選擇模型並輸入閾值', '查看特徵數與名稱', results_store
        if threshold is None or str(threshold) in invalid_thresholds:
            return '請重新輸入閾值', '查看特徵數與名稱', results_store

        # 根據閾值選擇特徵
        correlation_matrix = df_clean.corr().loc[:, 'PRICE']
        selected_features = correlation_matrix[correlation_matrix.abs() > threshold].index
        
        if 'PRICE' in selected_features:
            features = df_clean[selected_features].drop(columns=['PRICE'])
        else:
            features = df_clean[selected_features]

        # 檢查是否有數據
        if features.empty or 'PRICE' not in df_clean.columns:
            return '選擇的特徵中無有效數據', '查看特徵數與名稱', results_store
        
        X = features.dropna()
        y = df_clean.loc[X.index, 'PRICE']
        
        # 檢查 X 和 y 是否有效
        if X.empty or y.empty or X.shape[0] != y.shape[0]:
            return '特徵或目標變量無有效數據', '查看特徵數與名稱', results_store

        # 根據所選擇的模型進行評估
        if selected_model == 'linear-regression':
            model = LinearRegression()
        elif selected_model == 'knn':
            model = KNeighborsRegressor()
        elif selected_model == 'grid-search':
            param_grid = {'n_neighbors': range(1, 21)}
            model = GridSearchCV(KNeighborsRegressor(), param_grid, cv=5)
        elif selected_model == 'decision-tree':
            model = DecisionTreeRegressor()
        elif selected_model == 'random-forest':
            model = RandomForestRegressor()
        else:
            return '未知模型選擇', '查看特徵數與名稱', results_store

        # 訓練模型
        model.fit(X, y)
        predictions = model.predict(X)
        mse = mean_squared_error(y, predictions)
        r_squared = r2_score(y, predictions)
        
        if selected_model in ['knn', 'grid-search']:
            accuracy = "--"
        else:
            accuracy = model.score(X, y)
        
        # 確保 accuracy 是數值型別
        if accuracy == "--":
            accuracy = "--"
        else:
            accuracy = float(accuracy)

        if len(results_store) >= 5:
            results_store = []

        results_store.append({
            'model': selected_model,
            'threshold': threshold,
            'mse': mse,
            'r_squared': r_squared,
            'accuracy': accuracy
        })

        selected_model_store = selected_model
        last_threshold = threshold

        evaluation_result = f"選擇的模型: {selected_model}\n均方誤差 (MSE): {mse:.4f}\nR-squared: {r_squared:.4f}\n準確度: {accuracy:.4f}" if selected_model not in ['knn', 'grid-search'] else f"選擇的模型: {selected_model}\n均方誤差 (MSE): {mse:.4f}\nR-squared: {r_squared:.4f}\n準確度: {accuracy}"
        selected_features_text = f"選擇的特徵數: {len(selected_features)}\n特徵: {', '.join(selected_features)}"

        return evaluation_result, selected_features_text, results_store

    # 返回初始值以防止沒有點擊按鈕時
    return '', '', []


