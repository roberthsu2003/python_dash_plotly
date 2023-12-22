import requests
import csv
import json
import pandas as pd
import matplotlib.pyplot as plt

#-----指定股票代號檔案來源-----#
def tuple_number():
    with open('number.csv', "r",encoding='utf-8') as f:
        reader=csv.reader(f)
        for row in reader:
            x=tuple(row[0] for row in reader)
            return x

#-----raw data下載與整理-----#
def down_load():
    x=tuple_number()
    for row in x:
        url = "https://api.finmindtrade.com/api/v4/data"
        parameter = {
        "dataset": "TaiwanStockPrice",
        "data_id": f"{row}",
        "start_date": "2020-01-01"
        }
        r = requests.get(url, params=parameter)
        data = r.json()
        stock_deal_info = data["data"]
        print(stock_deal_info)
        with open(f'./stock_row_data/{row}.csv','w+',encoding='utf-8') as file:
            writer = csv.DictWriter(
        file, fieldnames=["date", "stock_id", "Trading_Volume", "Trading_money", "open", "max", "min", "close", "spread", "Trading_turnover"])
            writer.writeheader()
            for row in stock_deal_info:
                writer.writerow(row)
    x=tuple_number()
    for row in x:
        with open(f'./stock_row_data/{row}.csv',"r",encoding="utf-8") as file2:
            reader=csv.reader(file2)
            data = list(reader)
            for i in range(len(data) - 1, -1, -1):
                if not data[i]:
                    del data[i]
            with open(f'./stock_row_data/{row}.csv', 'w', newline='') as fp:
                writer = csv.writer(fp)
                writer.writerows(data)

#-----從raw data最後一筆開始讀取資料-----#
def read_lastest_data()->None:
    '''
    功能：從最後一筆資料開始讀取----這邊要改為產出reverse_stock.csv
    '''
    with open("stock.csv", "r") as f:
        reader = csv.reader(f)
        data=list(reader)
        for row in reversed(data):
            print(row)

#-----抓取最新的指定筆數資料並計算移動均價及移動成交量-----#
def con_save_mov_avg()->None:
    '''
    功能：抓取最新的指定筆數資料並計算移動均價及移動成交量
    修改抓取筆數擴大為960筆
    '''
    #-----抓取最新的指定筆數-----#
    x=tuple_number()
    for row in x:
        data = pd.read_csv(f'./stock_row_data/{row}.csv') #讀取row data檔案
        tail_960=data.tail(960) #數據及變數可修改為指定筆數
        stock_id=tail_960[['stock_id']] #撈取股票代號欄位
        date=tail_960[["date"]] #撈取指定筆數的日期欄位
        close=tail_960[['close']] #撈取指定筆數的收盤價
        volume=tail_960[['Trading_Volume']] #撈取指定筆數的成交量
        #-----計算移動均價-----#
        #-----計算5日均價值-----#
        mov5=round(tail_960['close'].rolling(window=5).mean(),ndigits=2) 
        mov5=list(mov5)
        #-----計算20日均價值-----#
        mov20=round(tail_960['close'].rolling(window=20).mean(),ndigits=2)
        mov20=list(mov20)
        #-----計算60日均價值-----#
        mov60=round(tail_960['close'].rolling(window=60).mean(),ndigits=2)
        mov60=list(mov60)
        #-----計算移動成交量-----#
        #-----計算5日平均成交量-----#
        avg_volume_5=round(tail_960['Trading_Volume'].rolling(window=5).mean())
        avg_volume_5=list(avg_volume_5)
        #-----計算20日平均成交量-----#
        avg_volume_20=round(tail_960['Trading_Volume'].rolling(window=20).mean())
        avg_volume_20=list(avg_volume_20)
        #-----計算60日平均成交量-----#
        avg_volume_60=round(tail_960['Trading_Volume'].rolling(window=60).mean())
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
        mov.to_csv(f'mov_{row}.csv',index=False)
    
#-----插入5/20/60日移動均價的前值-----#
def insert_prev_mov_avg()->None:
    '''
    功能：插入前一交易日的移動均價，以利後續進行比較
    插入欄位的方式是在各日均價右邊新增欄位
    '''
    x=tuple_number()
    for row in x:
        data1 = pd.read_csv(f'mov_{row}.csv')
        tail_960=data1.tail(960)
        #-----原本欄位-----#
        stock_id=tail_960[['股票代號']]
        date=tail_960[["日期"]]
        close=tail_960[['收盤價']]
        mov5=tail_960[['5日移動均價']]
        mov20=tail_960[['20日移動均價']]
        mov60=tail_960[['60日移動均價']]
        volume=tail_960[['當日成交量']]
        avg_volume_5=tail_960[['5日平均成交量']]
        avg_volume_20=tail_960[['20日平均成交量']]
        avg_volume_60=tail_960[["60日平均成交量"]]
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
        mov.to_csv(f'mov_{row}.csv',index=False)

#-----將計算完成均價均量的檔案合併在mov檔-----#
def marge_mov_file():
    x=tuple_number()
    for row in x:
        mov=pd.read_csv(f'mov_{row}.csv')
        mov.to_csv('mov.csv', mode="a", index=False,header=None)
    df=pd.read_csv('mov.csv')
    df = df.drop_duplicates()
    df.to_csv('mov.csv',index=False)


#-----抓取收盤價為向上突破的交易日，並且存檔為up.csv-----#
def analysis_avg_up():
    with open('up.csv','w',encoding='utf-8')as f:
        up_writer=csv.writer(f)
        up_writer.writerow(['股票代號','日期','收盤價','5日移動均價','prev_5日移動均價','20日移動均價','prev_20日移動均價','60日移動均價','prev_60日移動均價','當日成交量','5日平均成交量','20日平均成交量','60日平均成交量'])
        with open('up_after20.csv','w',encoding='utf-8') as up_after20:
            up_after20=csv.writer(up_after20)
            up_after20.writerow(['股票代號','日期','收盤價','5日移動均價','prev_5日移動均價','20日移動均價','prev_20日移動均價','60日移動均價','prev_60日移動均價','當日成交量','5日平均成交量','20日平均成交量','60日平均成交量'])
            with open('mov.csv','r',encoding='utf-8') as file:
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
                    volume=item[9]
                    volume_avg_5=item[10]
                    #-----篩選向上穿過20日均價線的交易日-----#
                    if mov_5>mov_20: #如果當5日均價大於20日均價
                        if prev_mov_5<prev_mov_20: #又前一5日均價小於20日均價
                        #if volume>volume_avg_5:#且當日成交量大於等於5日均量-->完成特徵值的篩選條件
                            x=reader.line_num #取得該行的索引值
                            up_writer.writerow(item) #將特徵值寫入up.csv
                            with open('mov.csv','r',encoding='utf-8') as file2:
                                reader2=csv.reader(file2)
                                for row in reader:
                                    if reader.line_num ==x+20: #抓取從特徵值往後數第二筆資料
                                        up_after20.writerow(row)
                                        break
                                

#-----抓取收盤價為向下突破的交易日，並且存檔為down.csv-----#
def analysis_avg_down():
    with open('down.csv','w',encoding='utf-8')as f:
        down_writer=csv.writer(f)
        down_writer.writerow(['股票代號','日期','收盤價','5日移動均價','prev_5日移動均價','20日移動均價','prev_20日移動均價','60日移動均價','prev_60日移動均價','當日成交量','5日平均成交量','20日平均成交量','60日平均成交量'])
        with open('down_after20.csv','w',encoding='utf-8') as up_after20:
            down_after20=csv.writer(up_after20)
            down_after20.writerow(['股票代號','日期','收盤價','5日移動均價','prev_5日移動均價','20日移動均價','prev_20日移動均價','60日移動均價','prev_60日移動均價','當日成交量','5日平均成交量','20日平均成交量','60日平均成交量'])
            with open('mov.csv','r',encoding='utf-8') as file:
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
                    volume=item[9]
                    volume_avg_5=item[10]
                    #-----篩選向下穿過20日均價線的交易日-----#
                    if mov_5<mov_20: #如果當5日均價小於20日均價
                        if prev_mov_5>prev_mov_20: #又前一5日均價大於20日均價
                            #if volume>volume_avg_5:#且當日成交量大於等於5日均量-->完成特徵值的篩選條件
                            x=reader.line_num #取得該行的索引值
                            down_writer.writerow(item) #將特徵值寫入up.csv
                            with open('mov.csv','r',encoding='utf-8') as file2:
                                reader2=csv.reader(file2)
                                for row in reader:
                                    if reader.line_num ==x+20: #抓取從特徵值往後數第二筆資料
                                        down_after20.writerow(row)
                                        break

#-----移除csv檔的空白行-----#
def remove_blank_lines():
    #-----整理向上突破的特徵值檔案-----#
    with open("up.csv","r",encoding="utf-8") as file2:
            reader=csv.reader(file2)
            data = list(reader)
            for i in range(len(data) - 1, -1, -1):
                if not data[i]:
                    del data[i]
            with open('up.csv', 'w', newline='',encoding='utf-8') as fp:
                writer = csv.writer(fp)
                writer.writerows(data)
    #-----整理向下穿過的特徵值檔案-----#
    with open("down.csv","r",encoding="utf-8") as file2:
            reader=csv.reader(file2)
            data = list(reader)
            for i in range(len(data) - 1, -1, -1):
                if not data[i]:
                    del data[i]
            with open('down.csv', 'w', newline='',encoding='utf-8') as fp:
                writer = csv.writer(fp)
                writer.writerows(data)
    #-----整理向上突破的特徵值比對檔案-----#
    with open("up_after20.csv","r",encoding="utf-8") as file2:
            reader=csv.reader(file2)
            data = list(reader)
            for i in range(len(data) - 1, -1, -1):
                if not data[i]:
                    del data[i]
            with open('up_after20.csv', 'w', newline='',encoding='utf-8') as fp:
                writer = csv.writer(fp)
                writer.writerows(data)
    #-----整理向下穿過的特徵值比對檔案-----#
    with open("down_after20.csv","r",encoding="utf-8") as file2:
            reader=csv.reader(file2)
            data = list(reader)
            for i in range(len(data) - 1, -1, -1):
                if not data[i]:
                    del data[i]
            with open('down_after20.csv', 'w', newline='',encoding='utf-8') as fp:
                writer = csv.writer(fp)
                writer.writerows(data)

#-----整理up/down特徵值與比較值為在同一個檔案，並計算出漲跌幅-----#
def count_up_down_Quote_change():
    #-----向上特徵值計算-----#
    up=pd.read_csv('up.csv')
    stock_id=up['股票代號'] #抓取股票代號
    up=up['收盤價'] #抓取特徵值收盤價
    up_after20=pd.read_csv('up_after20.csv')
    up_after20=up_after20['收盤價'] #抓取比較值收盤價 
    up_spread=up_after20-up #計算比較值與特徵值之間的價差
    up_spread=list(round(up_spread,2)) #計算後的價差整理到小數點後2位並list出來
    up_spread_percent=(up_after20-up)/up*100 #計算差價與比較值的漲跌幅
    up_spread_percent=list(round(up_spread_percent,2)) #計算後的漲跌幅整理到小數第二位並list出來
    #-----整理計算數據並存入csv檔-----#
    data=pd.DataFrame()
    data['股票代號']=stock_id
    data['特徵值']=up
    data['20日後比較值']=up_after20
    data['價差']=up_spread
    data['比較後漲跌百分比']=up_spread_percent
    data.to_csv('up_data.csv',index=False)
    #-----向下特徵值計算-----#
    down=pd.read_csv('down.csv')
    stock_id=down['股票代號'] #抓取股票代號
    down=down['收盤價'] #抓取特徵值收盤價
    down_after20=pd.read_csv('down_after20.csv')
    down_after20=down_after20['收盤價'] #抓取比較值收盤價 
    down_spread=down_after20-down #計算比較值與特徵值之間的價差
    down_spread=list(round(down_spread,2)) #計算後的價差整理到小數點後2位並list出來
    down_spread_percent=(down_after20-down)/up*100 #計算差價與比較值的漲跌幅
    down_spread_percent=round(down_spread_percent,2) #計算後的漲跌幅整理到小數第二位並list出來
    #-----整理計算數據並存入csv檔-----#
    data2=pd.DataFrame()
    data2['股票代號']=stock_id
    data2['特徵值']=down
    data2['20日後比較值']=down_after20
    data2['價差']=down_spread
    data2['比較後漲跌百分比']=down_spread_percent
    data2.to_csv('down_data.csv',index=False)   