import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
from alldata.taipei_mk1_irwin import irwin_taipei_mk1, irwin_anal_mk1_data, irwin_time_series1
from alldata.taipei_mk2_irwin import irwin_anal_mk2_data, irwin_time_series2
from alldata.taipei_mk1_chiinhwang import chiinhwang_taipei_mk1, chiinhwang_anal_mk1_data, chiinhwang_time_series1
from alldata.taipei_mk2_chiinhwang import chiinhwang_anal_mk2_data, chiinhwang_time_series2

# 生成 Dash 應用程式
app = dash.Dash(__name__)

# 定義應用程式佈局
app.layout = html.Div([
    
    html.H1('台北市場的芒果分析與預測'),

    # 芒果種類下拉選單
    html.Div(id='mango-variety-container', children=[
        html.Label('芒果種類'),
        dcc.Dropdown(
            id='mango-variety-dropdown',
            options=[
                {'label': '請選擇種類', 'value': '請選擇種類'},
                {'label': '愛文', 'value': '愛文'},
                {'label': '金煌', 'value': '金煌'}
            ],
            # 預設值
            value='請選擇種類'  
        )
    ], style={'margin-bottom': '20px'}),

    # 下拉選單選擇市場
    html.Div(id='market-variety-container', children=[
        html.Label('選擇市場'),
        dcc.Dropdown(
        id='market-dropdown',
            options=[
                {'label': '請選擇市場', 'value': '請選擇市場'},
                {'label': '台北一', 'value': '台北一'},
                {'label': '台北二', 'value': '台北二'}
            ],
            # 預設值
            value='請選擇市場'
        )
    ]),

    # 主要資料表格顯示
    html.Div([
        html.H2('主要資料表格'),
        dash_table.DataTable(
            id='table',
            columns=[],
            data=[],
            style_table={'overflowX': 'auto'},
            # 設置每頁顯示10行
            page_size=10,  
        ),
    ]),

    # 全部資料分布狀況表格顯示
    html.Div([
        html.H2('全部資料分布狀況'),
        dash_table.DataTable(
            id='descr-table',
            columns=[],
            data=[],
                # style_table={'overflowX': 'auto'},
                # # 設置每頁顯示10行
                # page_size=10,  # 設置每頁顯示10行
        ),
    ]),

    # 盒鬚圖圖片 顯示
    html.Div([
        html.H2('盒鬚圖'),
        html.Img(id='box-plot', src=''),
    ]),

    # skew 和 kurt
    html.Div([
        html.H2('偏態和峰度'),
        html.Div(id='skew-kurt-label'),
    ]),

    # 常態分佈圖圖片 顯示
    html.Div([
        html.H2('常態分佈圖'),
        html.Img(id='distribution-plot', src=''),
    ]),
    
    # 自相關圖 (ACF) & 偏自相關圖 (PACF) 顯示
    html.Div([
        html.H2('自相關圖 (ACF) & 偏自相關圖 (PACF)'),
        html.Img(id='acf-pacf-plot', src=''),
    ]),

    # MSE, RMSE, MAE 值
    html.Div([
        html.H2('回歸誤差指標'),
        html.Div(id='rmas-calculate'),
    ]),

    # 殘差隨時間變化圖 和 Q-Q 圖 顯示
    html.Div([
        html.H2('殘差隨時間變化圖 和 Q-Q 圖'),
        html.Img(id='residual-qq-plot', src=''),
    ]),
    
    # SARIMA 模型結果 顯示
    html.Div([
        html.H2('SARIMA 模型結果'),
        html.Img(id='sarima-plot', src=''),
    ]),

    # 分開顯示訓練和測試數據
    html.Div([
        html.H2('分開顯示訓練和測試數據'),
        html.Img(id='train-test-plot', src=''),
    ]),

])

# 定義回調函數來更新表格
@app.callback([
    Output('table', 'columns'),
    Output('table', 'data'),
    Output('descr-table', 'columns'),
    Output('descr-table', 'data'),
    Output('box-plot', 'src'),
    Output('skew-kurt-label', 'children'),
    Output('distribution-plot', 'src'),
    Output('acf-pacf-plot', 'src'),
    Output('rmas-calculate', 'children'),
    Output('residual-qq-plot', 'src'),
    Output('sarima-plot', 'src'),
    Output('train-test-plot', 'src')],
    [Input('mango-variety-dropdown', 'value'),
     Input('market-dropdown', 'value')]
)

def update_table(selected_mango, selected_market):
    
    if selected_mango == '請選擇種類' or selected_market == '請選擇市場':
        # 使用無資料狀態進行測試
        columns = []
        data = []
        descr_columns = []
        descr_data = []
        # 返回無資料狀態，其他圖片和計算結果可以返回空值
        return columns, data, descr_columns, descr_data, '', '', '', '', '', '', '', ''

    if selected_mango == '金煌':
        df_taipei_mk = chiinhwang_taipei_mk1(selected_market)
        if selected_market == '台北一':
            # 使用 anal_mk1_data 函數來獲取分析數據
            all_descr, box_plot, skew, kurt, distribution_plot = chiinhwang_anal_mk1_data(df_taipei_mk)
            acf_pacf_plot, Training_MSE, Training_RMSE, Training_MAE, Testing_MSE, Testing_RMSE, Testing_MAE, sarima_model_plot, combined_train_test_plot, residuals_plot = chiinhwang_time_series1(df_taipei_mk)
        else:
            all_descr, box_plot, skew, kurt, distribution_plot = chiinhwang_anal_mk2_data(df_taipei_mk)
            acf_pacf_plot, Training_MSE, Training_RMSE, Training_MAE, Testing_MSE, Testing_RMSE, Testing_MAE, sarima_model_plot, combined_train_test_plot, residuals_plot = chiinhwang_time_series2(df_taipei_mk)
    else:
        # 使用 taipei_mk1 函數來獲取 DataFrame
        df_taipei_mk = irwin_taipei_mk1(selected_market)
        
        if selected_market == '台北一':
            # 使用 anal_mk1_data 函數來獲取分析數據
            all_descr, box_plot, skew, kurt, distribution_plot = irwin_anal_mk1_data(df_taipei_mk)
            acf_pacf_plot, Training_MSE, Training_RMSE, Training_MAE, Testing_MSE, Testing_RMSE, Testing_MAE, sarima_model_plot, combined_train_test_plot, residuals_plot = irwin_time_series1(df_taipei_mk)
        else:
            all_descr, box_plot, skew, kurt, distribution_plot = irwin_anal_mk2_data(df_taipei_mk)
            acf_pacf_plot, Training_MSE, Training_RMSE, Training_MAE, Testing_MSE, Testing_RMSE, Testing_MAE, sarima_model_plot, combined_train_test_plot, residuals_plot = irwin_time_series2(df_taipei_mk)
    
    # 更新 DataTable 的 columns 和 data
    columns = [{"name": i, "id": i} for i in df_taipei_mk.columns]
    data = df_taipei_mk.to_dict('records')

    # 重設索引並將其作為一個新欄位添加到DataTable
    descr_reset = all_descr.reset_index()
    
    # 更新全部資料分布狀況表格的 columns 和 data
    descr_columns = [{"name": i, "id": i} for i in descr_reset.columns]
    descr_data = descr_reset.reset_index().to_dict('records')

    # 盒鬚圖
    # 根據選擇的市場設置圖片路徑
    if selected_mango == '金煌':
        if selected_market == '台北一':
            box_plot_src = '/assets/chiinhwang_box_plot_1.png'
        elif selected_market == '台北二':
            box_plot_src = '/assets/chiinhwang_box_plot_2.png'
        else:
            box_plot_src = ''
    else:
        if selected_market == '台北一':
            box_plot_src = '/assets/irwin_box_plot_1.png'
        elif selected_market == '台北二':
            box_plot_src = '/assets/irwin_box_plot_2.png'
        else:
            box_plot_src = ''

    # skew 和 kurt
    skew_kurt_label = html.Div([
        html.Label(f'{skew}'),
        html.Br(),
        html.Label(f'{kurt}')
    ])

    # 常態分佈圖
    # 根據選擇的市場設置圖片路徑
    if selected_mango == '金煌':
        if selected_market == '台北一':
            distribution_plot_src = '/assets/chiinhwang_distribution_plot_1.png'
        elif selected_market == '台北二':
            distribution_plot_src = '/assets/chiinhwang_distribution_plot_2.png'
        else:
            distribution_plot_src = ''
    else:
        if selected_market == '台北一':
            distribution_plot_src = '/assets/irwin_distribution_plot_1.png'
        elif selected_market == '台北二':
            distribution_plot_src = '/assets/irwin_distribution_plot_2.png'
        else:
            distribution_plot_src = ''
    
    # 自相關圖 (ACF) & 偏自相關圖 (PACF)
    
    if selected_mango == '金煌':
        if selected_market == '台北一':
            acf_pacf_plot_src = '/assets/chiinhwang_acf_pacf_plot_1.png'
        elif selected_market == '台北二':
            acf_pacf_plot_src = '/assets/chiinhwang_acf_pacf_plot_2.png'
        else:
            acf_pacf_plot_src = ''
    else:
        if selected_market == '台北一':
            acf_pacf_plot_src = '/assets/irwin_acf_pacf_plot_1.png'
        elif selected_market == '台北二':
            acf_pacf_plot_src = '/assets/irwin_acf_pacf_plot_2.png'
        else:
            acf_pacf_plot_src = ''
    
    # MSE, RMSE, MAE 值
    rmas_calculate = html.Div([
        html.Label(f'{Training_MSE}'),
        html.Br(),
        html.Label(f'{Training_RMSE}'),
        html.Br(),
        html.Label(f'{Training_MAE}'),
        html.Br(),
        html.Label(f'{Testing_MSE}'),
        html.Br(),
        html.Label(f'{Testing_RMSE}'),
        html.Br(),
        html.Label(f'{Testing_MAE}')
    ])
    
    # 殘差隨時間變化圖 和 Q-Q 圖
    if selected_mango == '金煌':
        if selected_market == '台北一':
            residual_qq_plot_src = '/assets/chiinhwang_residuals_qq_plot_1.png'
        elif selected_market == '台北二':
            residual_qq_plot_src = '/assets/chiinhwang_residuals_qq_plot_2.png'
        else:
            residual_qq_plot_src = ''
    else:
        if selected_market == '台北一':
            residual_qq_plot_src = '/assets/irwin_residuals_qq_plot_1.png'
        elif selected_market == '台北二':
            residual_qq_plot_src = '/assets/irwin_residuals_qq_plot_2.png'
        else:
            residual_qq_plot_src = ''

    # SARIMA 模型結果
    if selected_mango == '金煌':
        if selected_market == '台北一':
            sarima_plot_src = '/assets/chiinhwang_sarima_model_analysis_1.png'
        elif selected_market == '台北二':
            sarima_plot_src = '/assets/chiinhwang_sarima_model_analysis_2.png'
        else:
            sarima_plot_src = ''
    else:
        if selected_market == '台北一':
            sarima_plot_src = '/assets/irwin_sarima_model_analysis_1.png'
        elif selected_market == '台北二':
            sarima_plot_src = '/assets/irwin_sarima_model_analysis_2.png'
        else:
            sarima_plot_src = ''
    
    # 分開顯示訓練和測試數據
    if selected_mango == '金煌':
        if selected_market == '台北一':
            train_test_plot = '/assets/chiinhwang_train_test_plot_1.png'
        elif selected_market == '台北二':
            train_test_plot = '/assets/chiinhwang_train_test_plot_2.png'
        else:
            train_test_plot = ''
    else:
        if selected_market == '台北一':
            train_test_plot = '/assets/irwin_train_test_plot_1.png'
        elif selected_market == '台北二':
            train_test_plot = '/assets/irwin_train_test_plot_2.png'
        else:
            train_test_plot = ''

    return columns, data, descr_columns, descr_data, box_plot_src, skew_kurt_label, distribution_plot_src, acf_pacf_plot_src,rmas_calculate, residual_qq_plot_src, sarima_plot_src, train_test_plot

# 運行應用程式
if __name__ == '__main__':
    app.run_server(debug=False)
