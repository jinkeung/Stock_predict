import yfinance as yf
import numpy as np
import pandas as pd

ticker = 'AAPL'  # 예시로 Apple 주식 데이터를 사용합니다
start_date = '2022-06-01'
end_date = '2024-06-01'
data = yf.download("035420.KS", start=start_date, end=end_date)

print(data)
data.to_excel("stock_predict.xlsx")