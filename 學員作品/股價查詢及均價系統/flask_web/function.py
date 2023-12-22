import requests
import csv
import json
import pandas as pd
import matplotlib.pyplot as plt

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
    "data_id": "2317",
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
    功能：從最後一筆資料開始讀取並寫入到reverse_stock.csv
    '''
    csv_file='stock.csv'
    data=pd.read_csv(csv_file)
    data_select=data[['stock_id','date','open','max','min','close','spread','Trading_Volume']]
    data_select.to_csv('select_volume.csv',header=True,index=False)
    with open('select_col.csv','w',encoding='utf-8') as file:
        writer=csv.writer(file)
        writer.writerow(['股票代號','交易日','開盤價','收盤價','最高價','最低價','漲跌(元)','成交股數'])
        with open('select_volume.csv','r',encoding='utf-8') as file2:
            reader=csv.reader(file2)
            next(reader)
            reverse_reader=list(reader)
            for item in reversed(reverse_reader):
                writer.writerow(item)

#-----抓取最新的指定筆數資料並計算移動均價及移動成交量-----#
def con_save_mov_avg()->None:
    '''
    功能：抓取最新的指定筆數資料並計算移動均價及移動成交量
    '''
    #-----抓取最新的指定筆數-----#
    data = pd.read_csv('stock.csv') #讀取row data檔案
    tail_180=data.tail(180) #數據及變數可修改為指定筆數
    stock_id=tail_180[['stock_id']] #撈取股票代號欄位
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
    mov['股票代號']=stock_id
    mov['日期']=date
    mov['收盤價']=close
    mov['5日移動均價']=mov5
    mov['20日移動均價']=mov20
    mov['60日移動均價']=mov60
    mov['當日成交量']=volume
    mov['5日平均成交量']=avg_volume_5
    mov['20日平均成交量']=avg_volume_20
    mov['60日平均成交量']=avg_volume_60
    mov.to_csv('mov.csv',index=False)
    
#-----插入5/20/60日移動均價的前值-----#
def insert_prev_mov_avg()->None:
    '''
    功能：插入前一交易日的移動均價，以利後續進行比較
    插入欄位的方式是在各日均價右邊新增欄位
    '''
    data1 = pd.read_csv('mov.csv')
    tail_180=data1.tail(180)
    #-----原本欄位-----#
    stock_id=tail_180[['股票代號']]
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
    prev_mov_5=data1[['5日移動均價']] #選擇5日移動均價欄位
    prev_mov_5=prev_mov_5.shift(periods=1)  #取得前一日的5日移動均價
    prev_mov_20=data1[['20日移動均價']] #選擇20日移動均價欄位
    prev_mov_20=prev_mov_20.shift(periods=1) #取得前一日的20日移動均價
    prev_mov_60=data1[['60日移動均價']] #選擇60日移動均價欄位
    prev_mov_60=prev_mov_60.shift(periods=1) #取得前一日的60日移動均價
    #-----將原有的欄位及新增欄位插入到mov.csv檔
    mov=pd.DataFrame()
    mov['股票代號']=stock_id #0
    mov['日期']=date #1
    mov['收盤價']=close #2
    mov['5日移動均價']=mov5 #3
    mov['5日移動均價'].fillna(0,inplace=True) #將欄位數值出現Nan補為0.00
    mov['prev_5日移動均價']=prev_mov_5 #4
    mov['prev_5日移動均價'].fillna(0,inplace=True) #將欄位數值出現Nan補為0.00
    mov['20日移動均價']=mov20 #5
    mov['20日移動均價'].fillna(0,inplace=True) #將欄位數值出現Nan補為0.00
    mov['prev_20日移動均價']=prev_mov_20 #6
    mov['prev_20日移動均價'].fillna(0,inplace=True) #將欄位數值出現Nan補為0.00
    mov['60日移動均價']=mov60 #7
    mov['60日移動均價'].fillna(0,inplace=True) #將欄位數值出現Nan補為0.00
    mov['prev_60日移動均價']=prev_mov_60 #8
    mov['prev_60日移動均價'].fillna(0,inplace=True) #將欄位數值出現Nan補為0.00
    mov['當日成交量']=volume #9
    mov['5日平均成交量']=avg_volume_5 #10
    mov['5日平均成交量'].fillna(0,inplace=True) #將欄位數值出現Nan補為0.00
    mov['20日平均成交量']=avg_volume_20 #11
    mov['20日平均成交量'].fillna(0,inplace=True) #將欄位數值出現Nan補為0.00
    mov['60日平均成交量']=avg_volume_60 #12
    mov['60日平均成交量'].fillna(0,inplace=True) #將欄位數值出現Nan補為0.00
    mov.to_csv('mov2.csv',index=False)

#-----抓取收盤價為向上突破的交易日，並且存檔為up.csv-----#
def analysis_avg_up():
    with open('up.csv','w',encoding='utf-8')as f:
         up_writer=csv.writer(f)
         up_writer.writerow(['股票代號','日期','收盤價','5日移動均價','prev_5日移動均價','20日移動均價','prev_20日移動均價','60日移動均價','prev_60日移動均價','當日成交量','5日平均成交量','20日平均成交量','60日平均成交量'])
         with open('mov2.csv','r',encoding='utf-8') as file:
            reader=csv.reader(file)
            next(reader) #跳過表頭欄位
            for item in reader:
                mov_5=item[3]
                mov_5=float(mov_5)
                prev_mov_5=item[4]
                prev_mov_5=float(prev_mov_5)
                mov_20=item[5]
                mov_20=float(mov_20)
                prev_mov_20=item[6]
                prev_mov_20=float(prev_mov_20)
                #-----篩選向上穿過20日均價線的交易日-----#
                if mov_5>mov_20: #如果當5日均價大於20日均價
                    if prev_mov_5<prev_mov_20: #又前一5日均價小於20日均價
                        up_writer.writerow(item)
    with open("up.csv","r",encoding="utf-8") as file2:
        reader=csv.reader(file2)
        data = list(reader)
        for i in range(len(data) - 1, -1, -1):
            if not data[i]:
                del data[i]
        with open('up.csv', 'w', newline='',encoding='utf-8') as fp:
            writer = csv.writer(fp)
            writer.writerows(data)
    


#-----抓取收盤價為向下突破的交易日，並且存檔為down.csv-----#
def analysis_avg_down():
    with open('down.csv','w',encoding='utf-8')as f:
        down_writer=csv.writer(f)
        down_writer.writerow(['股票代號','日期','收盤價','5日移動均價','prev_5日移動均價','20日移動均價','prev_20日移動均價','60日移動均價','prev_60日移動均價','當日成交量','5日平均成交量','20日平均成交量','60日平均成交量'])
        with open('mov2.csv','r',encoding='utf-8') as file:
            reader=csv.reader(file)
            next(reader) #跳過表頭欄位
            for item in reader:
                mov_5=item[3]
                mov_5=float(mov_5)
                prev_mov_5=item[4]
                prev_mov_5=float(prev_mov_5)
                mov_20=item[5]
                mov_20=float(mov_20)
                prev_mov_20=item[6]
                prev_mov_20=float(prev_mov_20)
                #-----篩選向下穿過20日均價線的交易日-----#
                if mov_5<mov_20: #如果當5日均價小於20日均價
                    if prev_mov_5>prev_mov_20: #又前一5日均價大於20日均價
                        #print(item)
                        down_writer.writerow(item)
    with open("down.csv","r",encoding="utf-8") as file2:
        reader=csv.reader(file2)
        data = list(reader)
        for i in range(len(data) - 1, -1, -1):
            if not data[i]:
                del data[i]
        with open('down.csv', 'w', newline='',encoding='utf-8') as fp:
            writer = csv.writer(fp)
            writer.writerows(data)
