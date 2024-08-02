import pandas as pd
from dash import Dash, html
from sqlalchemy import create_engine

# 初始化 Dash 應用
app1 = Dash(__name__, requests_pathname_prefix='/dashboard/app1/')
app1.title = '臺灣太陽能系統評估表單'

# 設置資料庫連線
db_url = 'postgresql://tvdi_postgresql_etik_user:4jYKNZqoOCkdoHsQIdHBOiL27yixeBTM@dpg-cqhf92aju9rs738kbi8g-a.singapore-postgres.render.com/tvdi_postgresql_etik_o8g3'
engine = create_engine(db_url)

# 假設您的表格名稱是 dash_web
query = "SELECT * FROM dash_web"

# 使用 Pandas 讀取資料
data = pd.read_sql(query, engine)

# 關閉資料庫連線
engine.dispose()

# 設置 Dash 應用的佈局
app1.layout = html.Div([
    html.H1('全臺站點資料表格'),
    html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in data.columns])
        ),
        html.Tbody([
            html.Tr([html.Td(data.iloc[i][col]) for col in data.columns])
            for i in range(len(data))
        ])
    ])
])

# 啟動 Dash 應用
if __name__ == '__main__':
    app1.run_server(debug=True)
