from sklearn.tree import DecisionTreeRegressor,DecisionTreeClassifier
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score,accuracy_score,precision_score, recall_score, f1_score, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt #繪圖
import plotly.graph_objects as go
import seaborn as sns

def Decision_tree_Regressor(test_size,data,feature):
    
    tdf = pd.DataFrame()
    tdf['Target'] = data['Close']

    x = data[feature].values  # 排除第一列（日期）和最后两列（Target和Close）
    y = tdf['Target'].values  # 使用 'Target' 作为目标变量

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=39830)

    dec = DecisionTreeRegressor(random_state=39830)
    dec.fit(x_train, y_train)

    # 在测试集上评估模型
    y_pred = dec.predict(x_test)
    mse = round(mean_squared_error(y_test, y_pred),4)
    r2 = round(r2_score(y_test, y_pred),4)

    x_last_predict = data.iloc[-1][feature].values.reshape(1, -1)
    y_last_predict = dec.predict((x_last_predict))

    #誤差 1%
    tolerance_percentage = 0.01 
    # 計算容忍度閾值
    tolerance_threshold = tolerance_percentage * np.abs(y_test)
    # 計算絕對誤差
    absolute_errors = np.abs(y_pred - y_test)
    # 計算在容忍度範圍內的正確比率
    correct_within_tolerance = np.mean(absolute_errors <= tolerance_threshold)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=y_test, 
        y=y_pred, 
        mode='markers', 
        name='Predicted vs Actual',
        marker=dict(color='blue')
    ))

    fig.add_trace(go.Scatter(
        x=[min(y_test), max(y_test)], 
        y=[min(y_test), max(y_test)], 
        mode='lines', 
        name='45 Degree Line',
        line=dict(color='red', dash='dash')
    ))

    fig.update_layout(
        title='Scatter Plot of Predicted vs Actual Values',
        xaxis_title='實際值',
        yaxis_title='預測值',
        showlegend=True
    )

    return mse,r2,round(y_last_predict[0],4),tolerance_percentage,correct_within_tolerance,fig

def Linear_regression(test_size,data,feature):
    tdf = pd.DataFrame()
    tdf['Target'] = data['Close']

    x = data[feature].values  # 排除第一列（日期）和最后两列（Target和Close）
    y = tdf['Target'].values  # 使用 'Target' 作为目标变量

    x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=test_size,random_state=39830)
    std_x = StandardScaler()
    x_train = std_x.fit_transform(x_train)
    x_test = std_x.transform(x_test)
    std_y = StandardScaler()
    y_train = std_y.fit_transform(y_train.reshape(-1, 1))
    y_test = std_y.transform(y_test.reshape(-1, 1))
    lr = LinearRegression()
    lr.fit(x_train, y_train)
    # print('權重值：{}'.format(lr.coef_))
    # print('偏置值：{}'.format(lr.intercept_))

    y_predict = std_y.inverse_transform(lr.predict(x_test))
    y_test=std_y.inverse_transform(y_test)

    mse = round(mean_squared_error(y_test, y_predict),4)
    r2 = round(r2_score(y_test, y_predict),4)

    x_last_predict = data.iloc[-1][feature].values.reshape(1, -1)
    y_last_predict = lr.predict((x_last_predict))

    #誤差 1%
    tolerance_percentage = 0.01 
    # 計算容忍度閾值
    tolerance_threshold = tolerance_percentage * np.abs(y_test)
    # 計算絕對誤差
    absolute_errors = np.abs(y_predict - y_test)
    # 計算在容忍度範圍內的正確比率
    correct_within_tolerance = np.mean(absolute_errors <= tolerance_threshold)

    fig = go.Figure()

    # Add scatter plot trace
    fig.add_trace(go.Scatter(
        x=y_test.flatten(),  # Flatten y_test for plotly
        y=y_predict.flatten(),  # Flatten y_predict for plotly
        mode='markers',
        marker=dict(color='blue'),
        name='Predicted vs Actual'
    ))

    # Add 45-degree line
    fig.add_trace(go.Scatter(
        x=[min(y_test.flatten()), max(y_test.flatten())],
        y=[min(y_test.flatten()), max(y_test.flatten())],
        mode='lines',
        line=dict(color='red', dash='dash'),
        name='45 Degree Line'
    ))

    # Update layout
    fig.update_layout(
        title='Scatter Plot of Predicted vs Actual Values',
        xaxis_title='實際值',
        yaxis_title='預測值',
        showlegend=True
    )


    return mse,r2,round(y_last_predict[0][0],4),tolerance_percentage,correct_within_tolerance,fig

def Decision_tree_Classifier(test_size, data, feature):
    tdf = pd.DataFrame()
    tdf['Target'] = np.where(data['Close'].shift(-1) > data['Close'], 'Buy', 'Sell')

    x = data[feature].values
    y = tdf['Target'].values

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=39830)

    dec = DecisionTreeClassifier(random_state=39830)
    dec.fit(x_train, y_train)

    x_last_predict = data.iloc[-1][feature].values.reshape(1, -1)
    y_pred = dec.predict(x_last_predict)
    y_test_pred = dec.predict(x_test)
    score = dec.score(x_test, y_test)

    # Calculate metrics
    accuracy = accuracy_score(y_test, y_test_pred)
    precision = precision_score(y_test, y_test_pred, average='weighted', labels=dec.classes_)
    recall = recall_score(y_test, y_test_pred, average='weighted', labels=dec.classes_)
    f1 = f1_score(y_test, y_test_pred, average='weighted', labels=dec.classes_)

    conf_matrix = confusion_matrix(y_test, y_test_pred, labels=dec.classes_)

    # Plot confusion matrix using plotly
    fig = go.Figure(data=go.Heatmap(
        z=conf_matrix,
        x=dec.classes_,
        y=dec.classes_,
        colorscale='Reds',
        colorbar=dict(title='Count')
    ))

    fig.update_layout(
        title='Confusion Matrix',
        xaxis_title='預測值',
        yaxis_title='實際值',
        xaxis=dict(tickvals=list(range(len(dec.classes_))), ticktext=dec.classes_),
        yaxis=dict(tickvals=list(range(len(dec.classes_))), ticktext=dec.classes_)
    )

    return score, y_pred[0], f1, fig

def Logisticregression(test_size, data, feature):
    tdf = pd.DataFrame()
    tdf['Target'] = np.where(data['Close'].diff() > 0, 'Buy', 'Sell')

    x = data[feature].values
    y = tdf['Target'].values

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=39830)
    transfer = StandardScaler()
    x_train = transfer.fit_transform(x_train)
    x_test = transfer.transform(x_test)

    estimator = LogisticRegression()
    estimator.fit(x_train, y_train)
    y_test_pred = estimator.predict(x_test)
    score = estimator.score(x_test, y_test)

    x_last_predict = data.iloc[-1][feature].values.reshape(1, -1)
    y_pred = estimator.predict(x_last_predict)

    # Calculate metrics
    accuracy = accuracy_score(y_test, y_test_pred)
    precision = precision_score(y_test, y_test_pred, average='weighted', labels=estimator.classes_)
    recall = recall_score(y_test, y_test_pred, average='weighted', labels=estimator.classes_)
    f1 = f1_score(y_test, y_test_pred, average='weighted', labels=estimator.classes_)

    conf_matrix = confusion_matrix(y_test, y_test_pred, labels=estimator.classes_)

    # Plot confusion matrix using plotly.graph_objects
    fig = go.Figure(data=go.Heatmap(
        z=conf_matrix,
        x=estimator.classes_,
        y=estimator.classes_,
        colorscale='Reds',
        colorbar=dict(title='Count')
    ))

    fig.update_layout(
        title='Confusion Matrix',
        xaxis_title='預測值',
        yaxis_title='實際值',
        xaxis=dict(tickvals=list(range(len(estimator.classes_))), ticktext=estimator.classes_),
        yaxis=dict(tickvals=list(range(len(estimator.classes_))), ticktext=estimator.classes_)
    )

    return score, y_pred[0], f1, fig

