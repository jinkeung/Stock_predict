import webbrowser

import streamlit as st
import pandas as pd
import numpy as np
import database_class as db
import sub
import ai_class as learn




def show_detail(selected_stock):


    df_data, df_future_data = learn.machine_learning(selected_stock)
    df_future_data['Date'] = pd.to_datetime(df_future_data['Date']).dt.date
    df_future_data['Predicted Price'] = df_future_data['Predicted Price'].round(-1).astype(int)

    # 첫 번째 블록 (차트 1과 리스트 1)
    col1, col2 = st.columns([2, 1])

    with col1:
        # 차트 1
        st.subheader(f'{selected_stock} 실제 주가')
        st.line_chart(df_data.set_index('Date')['Close'])

    with col2:
        # 리스트 1
        st.subheader('리스트 1')
        list_items1 = ['항목 1', '항목 2', '항목 3']
        selected_item1 = st.selectbox('리스트에서 선택하세요', list_items1)

    # 표 1
    st.subheader('표 1')
    st.dataframe(db.return_show_data(selected_stock))

    # 두 번째 블록 (차트 2와 리스트 2)
    col3, col4 = st.columns([2, 1])

    with col3:
        # 차트 2
        st.subheader(f'{selected_stock} 향후 30일간 예측 주가')
        st.line_chart(df_future_data.set_index('Date')['Predicted Price'])

    with col4:

        # 리스트 2
        st.subheader('표 2')
        st.dataframe(df_future_data)



import streamlit as st
import database_class as db
import sub

# 전체 페이지 설정
st.set_page_config(page_title='Stock Analysis App', layout='wide')

# 왼쪽 사이드바 - 리스트에서 종목 선택하기
st.sidebar.title('주식 종목 선택')
stock_name = db.return_stock_name()
selected_stock_list = [''] + stock_name
selected_stock = st.sidebar.selectbox('1. 주식 종목을 선택하세요', selected_stock_list)

# 선택된 항목이 공백인 경우 None으로 설정
if selected_stock == '':
    selected_stock = None

# 사이드바에 구분선 추가
st.sidebar.markdown('---')

# 오른쪽 사이드바 - 검색하여 종목 선택하기
search_stock = st.sidebar.text_input('2. 더 많은 종목 정보를 검색하세요 !')
if st.sidebar.button('검색'):
    if search_stock != '':
        selected_stock = search_stock  # 선택된 항목을 검색어로 변경
        sub.search_click(search_stock)
        show_detail(search_stock)

# 메인 컨텐츠 영역
st.title('Stock Analysis App')

# 선택된 주식 종목 출력
if selected_stock is None:
    st.write('주식 종목을 선택하거나 검색하세요.')
else:
    st.write(f'선택된 주식 종목: {selected_stock}')
    sub.list_click(selected_stock)
    show_detail(selected_stock)













