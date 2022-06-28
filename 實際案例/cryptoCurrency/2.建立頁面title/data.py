from urllib.request import Request, urlopen
import ssl
import pandas as pd
import time
from datetime import datetime
import csv

ssl._create_default_https_context = ssl._create_unverified_context
heads = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
while True:
    url = "https://goldprice.org/cryptocurrency-price"
    import_request = Request(url, headers=heads)
    web_page_data = urlopen(import_request).read()
    df=pd.read_html(web_page_data)
    dataFrame = df[0]
    dataFrame.drop(columns=['Circulating Supply', 'Volume (24h)', 'Price Chart (7d)'],inplace=True)
    dataFrame.rename(columns={'Change (24h)':'Change (24h) %'},inplace=True)
    dataFrame['Market Cap.'] = list(map(lambda x:x[1:],dataFrame['Market Cap.'].values))
    dataFrame['Price'] = list(map(lambda x:x[1:],dataFrame['Price'].values))
    dataFrame['Change (24h) %'] = list(map(lambda x:x[:-1],dataFrame['Change (24h) %'].values))
    dataFrame['Market Cap.'] = dataFrame['Market Cap.'].str.replace(',','')
    dataFrame['Price'] = dataFrame['Price'].str.replace(',','')
    dataFrame['Market Cap.'] = dataFrame['Market Cap.'].astype('int64')
    dataFrame['Price'] = dataFrame['Price'].astype('float').round(2)
    dataFrame['Change (24h) %'] = dataFrame['Change (24h) %'].astype('float').round(2)
    dataFrame = dataFrame[['Rank', 'CryptoCurrency','Price','Change (24h) %','Market Cap.']]
    time.sleep(5)

    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

    bitcoin_rank = dataFrame[dataFrame['CryptoCurrency'] == 'Bitcoin']['Rank'].iloc[0]
    bitcoin_currency = dataFrame[dataFrame['CryptoCurrency'] == 'Bitcoin']['CryptoCurrency'].iloc[0]
    bitcoin_price = dataFrame[dataFrame['CryptoCurrency'] == 'Bitcoin']['Price'].iloc[0]
    bitcoin_change = dataFrame[dataFrame['CryptoCurrency'] == 'Bitcoin']['Change (24h) %'].iloc[0]
    bitcoin_market_cap = dataFrame[dataFrame['CryptoCurrency'] == 'Bitcoin']['Market Cap.'].iloc[0]

    with open('bitcoin_data.csv','a') as file:
        writter = csv.writer(file)
        writter.writerow([dt_string,bitcoin_rank, bitcoin_currency, bitcoin_price, bitcoin_change, bitcoin_market_cap])

    print(dt_string,bitcoin_rank, bitcoin_currency, bitcoin_price, bitcoin_change, bitcoin_market_cap)