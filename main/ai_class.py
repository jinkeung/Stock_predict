import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pandas as pd
import database_class as db
def machine_learning(stock_name):

    data_df=db.return_train_data(stock_name)
    train_data = data_df['Close'].values

    X=list()
    y=list()
    time = 60  # 과거 데이터 범위 설정

    # 입력 데이터(X)와 타겟 데이터(y) 생성
    for i in range(len(train_data) - time - 30):
        X.append(train_data[i:i + time])
        y.append(train_data[i + time])

    X=np.array(X)
    y=np.array(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

    # 선형 회귀 모델 학습
    model = LinearRegression()
    model.fit(X_train, y_train)

    # 30일 예측
    future_data=list()
    last_data=train_data[-time:].reshape(1, -1)
    for i in range(30):
        predict=model.predict(last_data)[0]
        future_data.append(predict)
        last_data = np.append(last_data[:, 1:], predict).reshape(1, -1)

    # 향후 30일간의 예측 값을 데이터프레임으로 정리
    last_date = pd.to_datetime(data_df['Date'].iloc[-1])  # 가장 최근 날짜
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=30, freq='B')
    future_data_df = pd.DataFrame({'Date': future_dates, 'Predicted Price': future_data})




    return data_df, future_data_df