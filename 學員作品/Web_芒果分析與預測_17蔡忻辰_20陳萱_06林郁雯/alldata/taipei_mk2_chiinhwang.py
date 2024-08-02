import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error, mean_absolute_error
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.graphics.gofplots import qqplot
import os

# 清整後的 "台北二" 市場資料
def chiinhwang_taipei_mk2(market):

    # 資料路徑
    # file_path = '../mangodata/MangoIrwin.csv'
    # 使用絕對路徑
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, '..', 'mangodata', 'MangoChiinHwang.csv')
    # 讀取CSV資料    
    data = pd.read_csv(file_path)

    # 將資料轉換為DataFrame
    df = pd.DataFrame(data)
    
    # 篩選出 "台北二" 市場的所有資料並使用 .loc 進行操作
    df_taipei = df.loc[df['市場'] == market].copy()

    # 將'日期'轉換為datetime格式
    df_taipei['日期'] = pd.to_datetime(df_taipei['日期'])
    # 從'日期'中提取年, 月, 日
    df_taipei['年份']= df_taipei['日期'].dt.year
    df_taipei['月份']= df_taipei['日期'].dt.month
    df_taipei['日']= df_taipei['日期'].dt.day

    # 移除交易量中的逗號，並轉換為數值型態
    df_taipei['交易量(公斤)'] = df_taipei['交易量(公斤)'].str.replace(',', '').astype(float)

    # 檢查日期欄位是否有重複值，並移除重複日期
    df_taipei = df_taipei.drop_duplicates(subset=['日期'])

    # 按年份分組並收集日期資料到字典中
    year_datas = {}
    for year, group in df_taipei.groupby('年份'):
        year_datas[year] = {
            # 將datetime轉換為字串列表
            '日期': group['日期'].dt.strftime('%Y/%m/%d').tolist(),
            '市場': group['市場'].tolist(),
            '產品': group['產品'].tolist(),
            '上價': group['上價'].tolist(),
            '中價': group['中價'].tolist(),
            '下價': group['下價'].tolist(),
            '平均價(元/公斤)': group['平均價(元/公斤)'].tolist(),
            '交易量(公斤)': group['交易量(公斤)'].tolist()    
        }

    # 創建空的DataFrame來存儲結果
    df_taipei_mk2 = pd.DataFrame()

    # 迴圈處理每個年份的資料
    for year, year_data in year_datas.items():
        # 將資料轉換為DataFrame並將日期轉換為datetime格式
        df_year_data = pd.DataFrame(year_data)
        df_year_data['日期'] = pd.to_datetime(df_year_data['日期'])
        
        # 日期範圍（4月到9月）
        start_date = f'{year}-04-01'
        end_date = f'{year}-08-31'
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # 將日期設置為索引
        df_year_data.set_index('日期', inplace=True)

        # 重新索引以包含所有日期
        df_year_data = df_year_data.reindex(date_range)
        
        # 或者使用平均值插補
        df_year_data['平均價(元/公斤)'] = df_year_data['平均價(元/公斤)'].interpolate(method='linear')
        df_year_data['上價'] = df_year_data['上價'].interpolate(method='linear')
        df_year_data['中價'] = df_year_data['中價'].interpolate(method='linear')
        df_year_data['下價'] = df_year_data['下價'].interpolate(method='linear')
        df_year_data['交易量(公斤)'] = df_year_data['交易量(公斤)'].interpolate(method='linear')

        # 使用前向填充和後向填充來處理剩餘的缺失值
        df_year_data['平均價(元/公斤)'] = df_year_data['平均價(元/公斤)'].ffill().bfill()
        df_year_data['上價'] = df_year_data['上價'].ffill().bfill()
        df_year_data['中價'] = df_year_data['中價'].ffill().bfill()
        df_year_data['下價'] = df_year_data['下價'].ffill().bfill()
        df_year_data['交易量(公斤)'] = df_year_data['交易量(公斤)'].ffill().bfill()

        # 將交易量(公斤)轉換為整數
        df_year_data['交易量(公斤)'] = df_year_data['交易量(公斤)'].astype(int)


        # 填充市場和產品欄位
        market_value = year_data['市場'][0] if '市場' in year_data else '未知市場'
        product_value = year_data['產品'][0] if '產品' in year_data else '未知產品'
        df_year_data['市場'] = market_value
        df_year_data['產品'] = product_value

        # 重置索引並添加年份列
        df_year_data.reset_index(inplace=True)
        
        # 將索引顯示到日期欄位
        df_year_data.rename(columns={'index': '日期'}, inplace=True)
        
        # 將處理好的數據添加到結果DataFrame中
        df_taipei_mk2 = pd.concat([df_taipei_mk2, df_year_data], ignore_index=True)
    return df_taipei_mk2

# 盒鬚圖, 資料分布狀況, 偏態＆峰度, 常態分佈圖
def chiinhwang_anal_mk2_data(df_taipei_mk2, output_dir='assets'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 調整欄位順序
    df = df_taipei_mk2[['日期', '上價', '中價', '下價', '平均價(元/公斤)', '交易量(公斤)']]

    # 全部資料分布狀況
    all_descr = df.describe()

    price = df_taipei_mk2['平均價(元/公斤)']

    # 特徵欄位: 平均價(元/公斤)
    anal_data = pd.DataFrame(price, columns=['平均價(元/公斤)'])

    # 價位分布狀況
    descr = anal_data.describe()

    # 求出四分位距(IQR)=Q3-Q1與上邊界(天花板)和下邊界(地板)
    Q1=anal_data['平均價(元/公斤)'].quantile(0.25)
    Q3=anal_data['平均價(元/公斤)'].quantile(0.75)
    IQR=Q3-Q1
    Upper=Q3+1.5*IQR
    Lower=Q1-1.5*IQR

    # 設置支持中文的字體(macbook => Arial Unicode MS)
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False

    # 箱行圖
    plt.figure(figsize=(3, 5))
    plt.boxplot(anal_data['平均價(元/公斤)'], showmeans=True)
    plt.title('平均價(元/公斤)')
    box_plot = os.path.join(output_dir, 'chiinhwang_box_plot_2.png')
    plt.savefig(box_plot)
    plt.close()

    # skewness and kurtosis 偏態和峰度
    skew = f"偏態(Skewness):{anal_data['平均價(元/公斤)'].skew():.2f}"
    kurt = f"峰度(Kurtosis):{anal_data['平均價(元/公斤)'].kurt():.2f}"

    n=1.5
    #IQR = Q3-Q1
    IQR = np.percentile(anal_data['平均價(元/公斤)'],75) - np.percentile(anal_data['平均價(元/公斤)'],25)
    #outlier = Q3 + n*IQR
    outlier=anal_data[anal_data['平均價(元/公斤)'] < np.percentile(anal_data['平均價(元/公斤)'],75)+n*IQR]
    #outlier = Q1 - n*IQR
    outlier=anal_data[anal_data['平均價(元/公斤)'] > np.percentile(anal_data['平均價(元/公斤)'],25)-n*IQR]

    # 常態分布
    plt.figure()
    sns.histplot(anal_data['平均價(元/公斤)'], kde=True, element='step', stat="density", kde_kws=dict(cut=3), alpha=.4, edgecolor=(1, 1, 1, .4))
    plt.ylabel('密度')
    plt.xlabel('平均價(元/公斤)')
    distribution_plot= os.path.join(output_dir, 'chiinhwang_distribution_plot_2.png')
    plt.savefig(distribution_plot)
    plt.close()

    return  all_descr, box_plot, skew, kurt, distribution_plot

# 自相關圖 (ACF) & 偏自相關圖 (PACF), SARIMA模型視覺化
# 繪製結果（分開展示訓練和測試數據), 殘差隨時間變化和 Q-Q 圖
# 準備進行SARIMA建模的資料
def chiinhwang_time_series2(df_taipei_mk2, output_dir='assets'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
   
   # 目標值
    y = df_taipei_mk2['平均價(元/公斤)']

    # 分割資料為訓練集和測試集
    train_size = int(len(y) * 0.8)
    train, test = y.iloc[:train_size], y.iloc[train_size:]

    # 自相關圖 (ACF) 和 偏自相關圖 (PACF)
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plot_acf(y, ax=plt.gca(), lags=40)
    plt.title('自相關 (ACF)')

    plt.subplot(1, 2, 2)
    plot_pacf(y, ax=plt.gca(), lags=40)
    plt.title('偏自相關 (PACF)')

    acf_pacf_plot = os.path.join(output_dir, 'chiinhwang_acf_pacf_plot_2.png')
    plt.tight_layout()
    plt.savefig(acf_pacf_plot)
    plt.close()

    # 建立和訓練SARIMA模型
    # 注意這裡設置了季節性順序為(1, 1, 1, 150)因為季節性是每年6個月（4到8月）
    model = SARIMAX(train, order=(1, 1, 1), seasonal_order=(1, 1, 1, 150))
    model_fit = model.fit(method='powell', maxiter=200, disp=False)

    # 預測
    y_pred_train = model_fit.predict(start=train.index[0], end=train.index[-1], dynamic=False)
    y_pred_test = model_fit.predict(start=test.index[0], end=test.index[-1], dynamic=False)

    # 計算評估指標
    mse_train = mean_squared_error(train, y_pred_train)
    rmse_train = np.sqrt(mse_train)
    mae_train = mean_absolute_error(train, y_pred_train)

    mse_test = mean_squared_error(test, y_pred_test)
    rmse_test = np.sqrt(mse_test)
    mae_test = mean_absolute_error(test, y_pred_test)

    # 四捨五入到小數點後四位
    mse_train_rounded = round(mse_train, 4)
    rmse_train_rounded = round(rmse_train, 4)
    mae_train_rounded = round(mae_train, 4)

    mse_test_rounded = round(mse_test, 4)
    rmse_test_rounded = round(rmse_test, 4)
    mae_test_rounded = round(mae_test, 4)

    Training_MSE = f"Training MSE: {mse_train_rounded}"
    Training_RMSE = f"Training RMSE: {rmse_train_rounded}" 
    Training_MAE = f"Training MAE: {mae_train_rounded}"
    Testing_MSE = f"Testing MSE: {mse_test_rounded}"
    Testing_RMSE = f"Testing RMSE: {rmse_test_rounded}"
    Testing_MAE = f"Testing MAE: {mae_test_rounded}"

    # SARIMA 模型結果視覺化
    plt.figure(figsize=(12, 6))
    plt.plot(train.index, train, label='Training data')
    plt.plot(test.index, test, label='Testing data')
    plt.plot(train.index, y_pred_train, color='red', linestyle='--', label='Training prediction')
    plt.plot(test.index, y_pred_test, color='green', linestyle='--', label='Testing prediction')
    plt.xlabel('Time')
    plt.ylabel('平均價(元/公斤)')
    plt.title('SARIMA模型的時間序列分析和預測')
    plt.legend()
    sarima_model_plot = os.path.join(output_dir, 'chiinhwang_sarima_model_analysis_2.png')
    plt.savefig(sarima_model_plot)
    plt.close()

    # 繪製結果（分開展示訓練和測試數據）
    plt.figure(figsize=(14, 7))

    # 繪製實際數據和訓練預測
    plt.subplot(2, 1, 1)
    plt.plot(train.index, train, label='Train Data')
    plt.plot(train.index, y_pred_train, label='Train Predictions', linestyle='--')
    plt.legend()
    plt.title('Train Data and Predictions')

    # 繪製測試數據和測試預測
    plt.subplot(2, 1, 2)
    plt.plot(test.index, test, label='Test Data')
    plt.plot(test.index, y_pred_test, label='Test Predictions', linestyle='--')
    plt.legend()
    plt.title('Test Data and Predictions')
    plt.tight_layout()
    combined_train_test_plot = os.path.join(output_dir, 'chiinhwang_train_test_plot_2.png')
    plt.savefig(combined_train_test_plot)
    plt.close()

    # 計算訓練集的殘差
    residuals = train - y_pred_train  

    # 殘差隨時間變化和 Q-Q 圖
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.plot(residuals)
    plt.title('Residuals over Time')

    plt.subplot(1, 2, 2)
    qqplot(residuals, line='s', ax=plt.gca())
    plt.title('Q-Q Plot')

    residuals_plot = os.path.join(output_dir, 'chiinhwang_residuals_qq_plot_2.png')
    plt.tight_layout()
    plt.savefig(residuals_plot)
    plt.close()

    return acf_pacf_plot, Training_MSE, Training_RMSE, Training_MAE, Testing_MSE, Testing_RMSE, Testing_MAE, sarima_model_plot, combined_train_test_plot, residuals_plot
