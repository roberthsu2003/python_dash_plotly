# 改自能及時從FinLab API下載的stock3.py（由Tom開發）
# 有解決日期顯示問題；已整合進階功能分析"主力買超比例"至主頁、刪除原顯示之買賣超資訊比較圖表；
# 已整合進階功能分析"顯示主力買超前15名"
# 以.csv方式存儲資料，取代.pkl方式；空間節約成效：從440MB節約為150MB
# 後續可考慮微調版面配置；

from dotenv import load_dotenv
import dash
from dash import dcc, html, Input, Output, dash_table
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import finlab
from finlab import data
import os
import gzip
import shutil

# 初始化環境
load_dotenv()
finlab.login(os.getenv('FINLAB_API_KEY'))

# 定義存儲路徑
DATA_DIR = "./data"
os.makedirs(DATA_DIR, exist_ok=True)

# 全局變量
close_price = pd.DataFrame()

# 加載數據函數
def load_data():
    try:
        # 定義存儲數據的函數
        def get_and_save_data(api_key, filename):
            filepath = os.path.join(DATA_DIR, filename)
            if os.path.exists(filepath):  # 若本地已存在數據檔案，則直接加載
                print(f"Loading {filename} from local CSV file.")
                return pd.read_csv(filepath, index_col=0, parse_dates=True)
            else:  # 否則從 API 下載並保存為 CSV
                print(f"Downloading {filename} from API (all available data).")
                df = data.get(api_key)  # 下載所有可用數據，無時間限制
                df.to_csv(filepath)  # 保存為 CSV
                return df

        # 分別處理每個數據集
        foreign = get_and_save_data(
            'institutional_investors_trading_summary:外陸資買賣超股數(不含外資自營商)', 
            "foreign_trading.csv"
        )
        foreign_dealer = get_and_save_data(
            'institutional_investors_trading_summary:外資自營商買賣超股數', 
            "foreign_dealer_trading.csv"
        )
        investment_trust = get_and_save_data(
            'institutional_investors_trading_summary:投信買賣超股數', 
            "investment_trust_trading.csv"
        )
        dealer = get_and_save_data(
            'institutional_investors_trading_summary:自營商買賣超股數(自行買賣)', 
            "dealer_trading.csv"
        )

        # 合併外資與外資自營商數據
        foreign_total = foreign.fillna(0) + foreign_dealer.fillna(0)

        # 處理收盤價數據
        global close_price
        close_price = get_and_save_data("price:收盤價", "close_price.csv")

        # 返回處理後的數據字典
        return {
            "foreign_trading": foreign_total,
            "investment_trust_trading": investment_trust.fillna(0),
            "dealer_trading": dealer.fillna(0),
        }
    except Exception as e:
        print(f"Error loading data: {e}")
        return {}


# Load stock list from Excel
def get_stock_list_from_excel():
    try:
        df = pd.read_excel("./data/tw_stock_topics.xlsx")
        return [f"{row['stock_no']} {row['stock_name']}" for _, row in df.iterrows()]
    except Exception as e:
        print(f"Error reading stock list: {e}")
        return []

stock_list = get_stock_list_from_excel()

# Dash App
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Stock Analysis Dashboard"

# Main page layout
main_page_layout = html.Div([
    html.Div([
        html.H2("國內外投信股票買賣查詢系統", style={"textAlign": "center"}),

        html.Label("選擇股票："),
        dcc.Dropdown(
            id='stock-dropdown',
            options=[{"label": stock, "value": stock.split()[0]} for stock in stock_list],
            value="2330",  # 預設選擇台積電
        ),

        html.Button("顯示主力買超前15名", id="show-top15-button", n_clicks=0, style={"marginTop": "20px"}),
    ], style={"width": "30%", "display": "inline-block", "verticalAlign": "top", "padding": "20px"}),

    html.Div([
        html.H3("三大法人買賣超資訊", style={"textAlign": "center"}),
        dash_table.DataTable(
            id='stock-table',
            columns=[
                {"name": "月份", "id": "Month"},
                {"name": "外資買賣超", "id": "Foreign"},
                {"name": "投信買賣超", "id": "Investment Trust"},
                {"name": "自營商買賣超", "id": "Dealer"}
            ],
            style_table={"overflowX": "auto", "overflowY": "auto", "height": "300px"},
            style_cell={"textAlign": "center"},
        ),

        html.H3("最近20日主力買超比例", style={"textAlign": "center"}),
        dcc.Graph(id="main-force-plot", style={"height": "400px"})
    ], style={"width": "65%", "display": "inline-block", "padding": "20px"})
])

# Top 15 page layout
top15_page_layout = html.Div([
    html.H2("主力買超前15名", style={"textAlign": "center"}),
    dcc.Link("返回主頁", href="/", style={"textAlign": "center", "display": "block", "margin": "20px"}),
    dash_table.DataTable(
        id='top15-table',
        columns=[
            {"name": "排名", "id": "Rank"},
            {"name": "股票代號", "id": "Stock"},
            {"name": "外資買超", "id": "Foreign"},
            {"name": "投信買賣超", "id": "Investment Trust"},
            {"name": "自營商買賣超", "id": "Dealer"},
            {"name": "總買超", "id": "Total"}
        ],
        style_table={"overflowX": "auto", "overflowY": "auto", "height": "400px"},
        style_cell={"textAlign": "center"},
    )
])

# App layout
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content")
])

# Callback to handle page routing
@app.callback(
    Output("url", "pathname"),
    [Input("show-top15-button", "n_clicks")]
)
def update_url(n_clicks):
    if n_clicks > 0:
        return "/top15"
    return "/"

# Callback to render page content
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def display_page(pathname):
    if pathname == "/top15":
        return top15_page_layout
    return main_page_layout

# Callback to populate top 15 table
@app.callback(
    Output("top15-table", "data"),
    [Input("url", "pathname")]
)
def get_top_15_data(pathname):
    if pathname != "/top15":
        return []

    try:
        all_stocks_data = []
        data_dict = load_data()  # Dynamically load data with limited date range

        for stock in stock_list:
            stock_code = stock.split()[0]
            try:
                foreign = data_dict["foreign_trading"].get(stock_code, pd.Series()).tail(20).sum()
                trust = data_dict["investment_trust_trading"].get(stock_code, pd.Series()).tail(20).sum()
                dealer = data_dict["dealer_trading"].get(stock_code, pd.Series()).tail(20).sum()

                all_stocks_data.append({
                    "Stock": stock_code,
                    "Foreign": foreign,
                    "Investment Trust": trust,
                    "Dealer": dealer,
                    "Total": foreign + trust + dealer
                })
            except Exception as e:
                print(f"Error processing stock {stock_code}: {e}")
                continue

        # Convert to DataFrame and deduplicate
        all_stocks_data_df = pd.DataFrame(all_stocks_data)

        if all_stocks_data_df.empty:
            print("Error: No stock data available for top 15.")
            return []

        unique_stocks = (all_stocks_data_df
                         .sort_values("Total", ascending=False)
                         .drop_duplicates(subset="Stock", keep="first"))
        top_15 = unique_stocks.nlargest(15, "Total")
        top_15["Rank"] = range(1, len(top_15) + 1)

        print(f"Top 15 data: {top_15}")  # Debugging
        return top_15.to_dict("records")
    except Exception as e:
        print(f"Error fetching top 15 data: {e}")
        return []

# Callback to display main page data
@app.callback(
    [Output("stock-table", "data"), Output("main-force-plot", "figure")],
    [Input("stock-dropdown", "value")]
)
def display_stock_data(stock_code):
    if not stock_code:
        return [], go.Figure()

    try:
        data_dict = load_data()
        # 三大法人買賣超資訊
        monthly_data = pd.DataFrame({
            "Foreign": data_dict["foreign_trading"][stock_code],
            "Investment Trust": data_dict["investment_trust_trading"][stock_code],
            "Dealer": data_dict["dealer_trading"][stock_code],
        }).fillna(0)

        monthly_data = monthly_data.resample("M").sum()
        monthly_data["Month"] = monthly_data.index.strftime("%Y-%m")
        monthly_data = monthly_data.iloc[::-1]  # 資料反向排序，最新資料在上
        table_data = monthly_data.reset_index().to_dict("records")

        # 最近20日主力買超比例
        volume = data.get("price:成交股數")[stock_code].tail(20)
        daily_data = pd.DataFrame({
            "Foreign": data_dict["foreign_trading"][stock_code].tail(20),
            "Investment Trust": data_dict["investment_trust_trading"][stock_code].tail(20),
            "Dealer": data_dict["dealer_trading"][stock_code].tail(20),
        }).fillna(0)

        daily_data["Total"] = daily_data["Foreign"] + daily_data["Investment Trust"] + daily_data["Dealer"]
        daily_data["Main Force Ratio"] = daily_data["Total"] / volume * 100

        fig = go.Figure()
        fig.add_trace(go.Bar(x=daily_data.index, y=daily_data["Main Force Ratio"], name="主力買超比例"))
        fig.update_layout(
            title="最近20日主力買超比例",
            xaxis_title="日期",
            yaxis_title="買超比例 (%)"
        )

        return table_data, fig

    except Exception as e:
        print(f"Error processing stock data: {e}")
        return [], go.Figure()

if __name__ == "__main__":
    app.run_server(debug=True)
