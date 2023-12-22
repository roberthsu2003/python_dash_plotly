import requests
import csv
import json
import pandas as pd


#-----raw data下載與整理-----#
def down_load()->None:
    '''
    功能：下載raw data下載/整理/存檔為stock.csv
    '''
    #-----下載資料-----#
    url = "https://api.finmindtrade.com/api/v4/data"
    # data_id：股票代號
    #start_date:資料起始日期
    parameter = {
    "dataset": "TaiwanStockPrice",
    "data_id": "1513",
    "start_date": "2022-01-01"
    }
    r = requests.get(url, params=parameter)
    data = r.json()
    stock_deal_info = data["data"]
    #-----把下載的json資料寫入csv檔案內-----#
    with open('stock.csv','w+',encoding='utf-8') as file:
        writer = csv.DictWriter(
        file, fieldnames=["date", "stock_id", "Trading_Volume", "Trading_money", "open", "max", "min", "close", "spread", "Trading_turnover"])
        writer.writeheader()
        for row in stock_deal_info:
            writer.writerow(row)
        #-----移除資料空白行-----#
    with open("stock.csv","r",encoding="utf-8") as file2:
        reader=csv.reader(file2)
        data = list(reader)
        for i in range(len(data) - 1, -1, -1):
            if not data[i]:
                del data[i]
        with open('stock.csv', 'w', newline='') as fp:
            writer = csv.writer(fp)
            writer.writerows(data)

#-----從raw data最後一筆開始讀取資料-----#
def read_lastest_data()->None:
    '''
    功能：從最後一筆資料開始讀取
    '''
    with open("../stock.csv", "r") as f:
        reader = csv.reader(f)
        data=list(reader)
        for row in reversed(data):
            return row

#-----抓取最新的指定筆數資料並計算移動均價及移動成交量-----#
def con_save_mov_avg()->None:
    '''
    功能：抓取最新的指定筆數資料並計算移動均價及移動成交量
    '''
    #-----抓取最新的指定筆數-----#
    data = pd.read_csv('stock.csv') #讀取row data檔案
    tail_180=data.tail(180) #數據及變數可修改為指定筆數
    date=tail_180[["date"]] #撈取指定筆數的日期欄位
    close=tail_180[['close']] #撈取指定筆數的收盤價
    volume=tail_180[['Trading_Volume']] #撈取指定筆數的成交量
    #-----計算移動均價-----#
    #-----計算5日均價值-----#
    mov5=round(tail_180['close'].rolling(window=5).mean(),ndigits=2) 
    mov5=list(mov5)
    #-----計算20日均價值-----#
    mov20=round(tail_180['close'].rolling(window=20).mean(),ndigits=2)
    mov20=list(mov20)
    #-----計算60日均價值-----#
    mov60=round(tail_180['close'].rolling(window=60).mean(),ndigits=2)
    mov60=list(mov60)
    #-----計算移動成交量-----#
    #-----計算5日平均成交量-----#
    avg_volume_5=round(tail_180['Trading_Volume'].rolling(window=5).mean())
    avg_volume_5=list(avg_volume_5)
    #-----計算20日平均成交量-----#
    avg_volume_20=round(tail_180['Trading_Volume'].rolling(window=20).mean())
    avg_volume_20=list(avg_volume_20)
    #-----計算60日平均成交量-----#
    avg_volume_60=round(tail_180['Trading_Volume'].rolling(window=60).mean())
    avg_volume_60=list(avg_volume_60)
    #-----將計算出的均值寫入csv檔-----#
    mov=pd.DataFrame()
    mov['日期']=date
    mov['收盤價']=close
    mov['5日移動均價']=mov5
    mov['20日移動均價']=mov20
    mov['60日移動均價']=mov60
    mov['當日成交量']=volume
    mov['5日平均成交量']=avg_volume_5
    mov['20日平均成交量']=avg_volume_20
    mov['60日平均成交量']=avg_volume_60
    mov.to_csv('mov.csv')
    
#-----插入5/20/60日移動均價的前值-----#
def insert_prev_mov_avg()->None:
    '''
    功能：插入前一交易日的移動均價，以利後續進行比較
    插入欄位的方式是在各日均價右邊新增欄位
    '''
    data1 = pd.read_csv('mov.csv')
    tail_180=data1.tail(180)
    #-----原本欄位-----#
    date=tail_180[["日期"]]
    close=tail_180[['收盤價']]
    mov5=tail_180[['5日移動均價']]
    mov20=tail_180[['20日移動均價']]
    mov60=tail_180[['60日移動均價']]
    volume=tail_180[['當日成交量']]
    avg_volume_5=tail_180[['5日平均成交量']]
    avg_volume_20=tail_180[['20日平均成交量']]
    avg_volume_60=tail_180[["60日平均成交量"]]
    #-----新增加的欄位-----#
    prev_mov_5=data1[['5日移動均價']]
    prev_mov_5=prev_mov_5.shift(periods=1)  #取得前一日的5日移動均價
    prev_mov_20=data1[['20日移動均價']]
    prev_mov_20=prev_mov_20.shift(periods=1) #取得前一日的20日移動均價
    prev_mov_60=data1[['60日移動均價']]
    prev_mov_60=prev_mov_60.shift(periods=1) #取得前一日的60日移動均價
    #-----將原有的欄位及新增欄位插入到mov.csv檔
    mov=pd.DataFrame()
    mov['日期']=date
    mov['收盤價']=close
    mov['5日移動均價']=mov5
    mov['prev_5日移動均價']=prev_mov_5
    mov['20日移動均價']=mov20
    mov['prev_20日移動均價']=prev_mov_20
    mov['60日移動均價']=mov60
    mov['prev_60日移動均價']=prev_mov_60
    mov['當日成交量']=volume
    mov['5日平均成交量']=avg_volume_5
    mov['20日平均成交量']=avg_volume_20
    mov['60日平均成交量']=avg_volume_60
    mov.to_csv('mov.csv')

#-----抓取收盤價為向下突破的交易日-----#
def mov_5_lower_mov20()->None:
    with open('down.csv','w',encoding='utf-8') as file:
        writer=csv.writer(file)
        with open('mov.csv','r',encoding='utf-8') as file:
            reader=csv.reader(file)
            for item in reader:
                date=item[1] #日期
                mov_5=item[3] #5日移動平均價
                prev_mov_5=item[4] #prev_5日移動均價
                mov_20=item[5] #20日移動均價
                prev_mov_20=item[6] #prev_20日移動均價
                #-----向下摜破判斷式-----#
                if mov_5<mov_20:
                    if mov_5>prev_mov_20:
                        writer.writerow(item)
                        print(item)

#-----抓取收盤價為向上突破的交易日-----#
def mov_5_uper_mov20()->None:
    with open('up.csv','w',encoding='utf-8') as file:
        writer=csv.writer(file)
        with open('mov.csv','r',encoding='utf-8') as file:
            reader=csv.reader(file)
            for item in reader:
                    date=item[1] #日期
                    mov_5=item[3] #5日移動平均價
                    prev_mov_5=item[4] #prev_5日移動均價
                    mov_20=item[5] #20日移動均價
                    prev_mov_20=item[6] #prev_20日移動均價
                    #-----向下摜破判斷式-----#
                    if mov_5>mov_20:
                        if mov_5<prev_mov_20:
                            writer.writerow(item)
                            print(item)

