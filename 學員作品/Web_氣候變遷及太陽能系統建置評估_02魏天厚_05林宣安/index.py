import os
import dash
import traceback
from dash import dcc, html
import base64
import pandas as pd
from sqlalchemy import create_engine
import subprocess

# 確定目錄設置正確，使用相對路徑設置文件路徑
current_dir = os.getcwd()
target_dir = os.path.join(current_dir, 'dash_web')

# 設置資料庫連線
db_url = 'postgresql://tvdi_postgresql_etik_user:4jYKNZqoOCkdoHsQIdHBOiL27yixeBTM@dpg-cqhf92aju9rs738kbi8g-a.singapore-postgres.render.com/tvdi_postgresql_etik_o8g3'
engine = create_engine(db_url)

# 假設您的表格名稱是 dash_web，以及要選取的欄位
query = "SELECT * FROM dash_web"

# 使用 Pandas 讀取資料
data = pd.read_sql(query, engine)

# 關閉資料庫連線
engine.dispose()

# 顯示選定圖像的函數
def display_image(image_path, width='80%', height='auto'):
    encoded_image = base64.b64encode(open(image_path, 'rb').read()).decode('utf-8')
    return html.Img(src=f'data:image/png;base64,{encoded_image}', style={'width': width, 'height': height})

# 假設 button_texts 是一個列表，包含按鈕的文本和圖像路徑
button_texts = [
    ("統計摘要", os.path.join('data.png')),
    ("盒鬚圖", os.path.join('boxplot_no_outliers.png')),
    ("每日平均日照時數", os.path.join('line_H.png')),
    ("平均日照時數常態分佈", os.path.join('normaldistribution_H.png')),
    ("每日平均太陽輻射量", os.path.join('line_R.png')),
    ("平均日射量常態分佈", os.path.join('normaldistribution_R.png')),
    ("熱力圖", os.path.join('heatmap.png')),
    ("線性回歸", os.path.join('linear_regression.png')),
]

# 創建 Dash 應用
app = dash.Dash(__name__)

# 創建主要的 layout
app.layout = html.Div([
    html.Div([
        html.H1("太陽能系統評估計算"),
        html.Div([
            html.Div([
                html.Button(text, id=f'button-{idx}', n_clicks=0) for idx, (text, _) in enumerate(button_texts)
            ], style={'textAlign': 'center', 'marginBottom': '20px'}),
            html.Div(id='image-display', style={'textAlign': 'center'})
        ]),
        html.Button("太陽能系統評估計算", id='calc-button', n_clicks=0),
        html.Div(id='calculator-output', style={'textAlign': 'center'})
    ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'justifyContent': 'center', 'height': '100vh'})
])

# 回調函數來更新圖像
@app.callback(
    dash.dependencies.Output('image-display', 'children'),
    [dash.dependencies.Input(f'button-{idx}', 'n_clicks') for idx, _ in enumerate(button_texts)]
)
def update_image(*args):
    try:
        ctx = dash.callback_context
        if not ctx.triggered:
            button_id = 'button-0'
        else:
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id.startswith('button-'):
            idx = int(button_id.split('-')[1])
            text, path = button_texts[idx]

            # 根據按鈕文本設定圖像大小
            if text == "統計摘要":
                return display_image(path, width='100%', height='auto')
            elif text == "每日平均日照時數":
                return display_image(path, width='60%', height='auto')
            elif text == "每日平均太陽輻射量":
                return display_image(path, width='60%', height='auto')
            else:
                return display_image(path)
    except Exception as e:
        traceback.print_exc()
        return html.Div(f"圖片顯示出現錯誤: {str(e)}")

# 回調函數來更新計算器部分
@app.callback(
    dash.dependencies.Output('calculator-output', 'children'),
    [dash.dependencies.Input('calc-button', 'n_clicks')]
)
def update_calculator(n_clicks):
    if n_clicks > 0:
        try:
            # 啟動計算器應用
            subprocess.Popen(["python", "calculator.py"])
            return html.Div("計算器應用已啟動")
        except Exception as e:
            traceback.print_exc()
            return html.Div(f"啟動計算器時出錯: {str(e)}")
    return ""

if __name__ == '__main__':
    app.run_server(host='127.0.0.1', port=8056, debug=False)
