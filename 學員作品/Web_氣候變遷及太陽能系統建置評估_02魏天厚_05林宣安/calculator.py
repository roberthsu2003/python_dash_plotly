import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
from sqlalchemy import create_engine
import os

# 連接到 SQLite 資料庫
DATABASE_URL = "postgresql://tvdi_postgresql_etik_user:4jYKNZqoOCkdoHsQIdHBOiL27yixeBTM@dpg-cqhf92aju9rs738kbi8g-a.singapore-postgres.render.com/tvdi_postgresql_etik_o8g3"  
engine = create_engine(DATABASE_URL)

# 讀取 SQL 資料
def load_data():
    query = "SELECT * FROM dash_web"
    df = pd.read_sql(query, engine)
    return df

# 讀取數據
dash_web_df = load_data()

# 定義太陽能系統相關常數
WATT_PER_PANEL = 400  # 每塊太陽能板的瓦數
PANEL_PRICE_RANGE = (250, 360)  # 每塊太陽能板的價格區間（美元）
USD_TO_TWD = 30  # 美元兌新台幣匯率
DAILY_ENERGY_THRESHOLD = 11  # 每日能量需求閾值（度）
SYSTEM_EFFICIENCY = 0.8  # 太陽能系統效率
AREA_PER_PANEL = 1.7  # 每塊太陽能板所需的面積（平方公尺）

# 其他設備價格範圍（美元）
ROOF_MOUNT_PRICE_RANGE = (1000, 3000)
GROUND_MOUNT_PRICE_RANGE = (2000, 4000)
STRING_INVERTER_PRICE_RANGE = (1000, 2500)
MICROINVERTER_PRICE_RANGE = (3000, 5000)
BATTERY_PRICE_RANGE = (4000, 7000)  # 鋰離子電池
CHARGE_CONTROLLER_PRICE_RANGE = (100, 500)
DISCONNECT_SWITCH_PRICE_RANGE = (50, 200)
LABOR_COST_RANGE = (3000, 7000)

# 定義根據樓地板面積計算每日預估發電量的函數
def calculate_daily_energy(floor_area_tsubo, esh):
    floor_area_m2 = floor_area_tsubo * 3.305785
    num_panels = floor_area_m2 / AREA_PER_PANEL
    total_watt = num_panels * WATT_PER_PANEL
    daily_energy = total_watt * esh * SYSTEM_EFFICIENCY / 1000  # 轉換成度
    return daily_energy

# 定義根據樓地板面積預估安裝價格的函數
def estimate_installation_cost(floor_area_tsubo, roof_mount=True):
    floor_area_m2 = floor_area_tsubo * 3.305785
    num_panels = floor_area_m2 / AREA_PER_PANEL
    panel_cost = num_panels * (sum(PANEL_PRICE_RANGE) / 2)
    
    mount_cost = sum(ROOF_MOUNT_PRICE_RANGE) / 2 if roof_mount else sum(GROUND_MOUNT_PRICE_RANGE) / 2
    inverter_cost = sum(STRING_INVERTER_PRICE_RANGE) / 2
    battery_cost = sum(BATTERY_PRICE_RANGE) / 2
    controller_cost = sum(CHARGE_CONTROLLER_PRICE_RANGE) / 2
    switch_cost = sum(DISCONNECT_SWITCH_PRICE_RANGE) / 2
    labor_cost = sum(LABOR_COST_RANGE) / 2
    
    total_cost_usd = panel_cost + mount_cost + inverter_cost + battery_cost + controller_cost + switch_cost + labor_cost
    total_cost_twd = total_cost_usd * USD_TO_TWD
    
    return total_cost_twd

# 定義建議是否安裝的函數
def suggest_installation(floor_area_tsubo, esh, roof_mount=True):
    daily_energy = calculate_daily_energy(floor_area_tsubo, esh)
    installation_cost = estimate_installation_cost(floor_area_tsubo, roof_mount)
    suggestion = "建議安裝" if daily_energy > DAILY_ENERGY_THRESHOLD else "不建議安裝"
    return suggestion, daily_energy, installation_cost

# 初始化 Dash 應用
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 應用佈局設定
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("太陽能系統計算器"),
            html.Label("選擇區域:"),
            dcc.Dropdown(
                id='region-dropdown',
                options=[{'label': region, 'value': region} for region in dash_web_df['行政區'].unique()],
                value=dash_web_df['行政區'].unique()[0]
            ),
            html.Label("樓地板面積 (坪):"),
            dcc.Input(
                id='floor-area-input',
                type='number',
                value=50  # 預設值
            ),
            html.Label("是否安裝屋頂架設?"),
            dcc.RadioItems(
                id='roof-mount-radio',
                options=[
                    {'label': '是', 'value': True},
                    {'label': '否', 'value': False}
                ],
                value=True
            ),
            html.Button('提交', id='submit-button', n_clicks=0),
            html.Div(id='result-output')
        ], width=6)
    ])
], fluid=True)

# 設定回調函數
@app.callback(
    Output('result-output', 'children'),
    Input('submit-button', 'n_clicks'),
    State('region-dropdown', 'value'),
    State('floor-area-input', 'value'),
    State('roof-mount-radio', 'value')
)
def update_output(n_clicks, region, floor_area_tsubo, roof_mount):
    if n_clicks > 0:
        try:
            floor_area_tsubo = float(floor_area_tsubo)
            esh = dash_web_df[dash_web_df['行政區'] == region]['ESH'].mean()
            
            if pd.isna(esh):
                return "資料錯誤: 無法找到該區域的ESH資料"
            
            suggestion, daily_energy, installation_cost = suggest_installation(floor_area_tsubo, esh, roof_mount)
            return (
                f"{suggestion}\n"
                f"每日預估發電量: {daily_energy:.2f} 度\n"
                f"預估安裝成本: {installation_cost:.2f} 新台幣"
            )
        except ValueError:
            return "輸入錯誤: 請輸入有效的樓地板面積"
    return ""

# 運行應用
if __name__ == '__main__':
    app.run_server(debug=True)
