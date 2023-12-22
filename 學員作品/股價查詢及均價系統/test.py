import pandas as pd

csv=pd.read_csv('mov.csv')
df_csv=csv.loc[:, ["股票代號", "日期", "收盤價", '5日移動均價']]
df_csv_tail=df_csv.tail(1)
z=df_csv_tail['股票代號']
print(z)