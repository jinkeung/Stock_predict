import streamlit as st
import pandas as pd
import numpy as np
import database_class as db
import sub

# 전체 페이지 설정
st.set_page_config(page_title='Stock Analysis App', layout='wide')

# 왼쪽 사이드바
st.sidebar.title('주식 종목 목록')
stock_name = db.return_stock_name()
selected_stock = st.sidebar.selectbox('주식 종목을 선택하세요', stock_name)
st.sidebar.markdown('---')
search_query = st.sidebar.text_input('더 많은 종목 정보를 검색하세요 !')
if st.sidebar.button('검색'):
    sub.search_click(search_query)

# 메인 컨텐츠 영역
st.title('Stock Analysis App')

# 첫 번째 블록 (차트 1과 리스트 1)
col1, col2 = st.columns([2, 1])

with col1:
    # 차트 1
    st.subheader('차트 1')
    df_chart1 = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['A', 'B', 'C']
    )
    st.line_chart(df_chart1)

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
    st.subheader('차트 2')
    df_chart2 = pd.DataFrame(
        np.random.randn(30, 2),
        columns=['X', 'Y']
    )
    st.line_chart(df_chart2)

with col4:
    # 리스트 2
    st.subheader('리스트 2')
    list_items2 = ['항목 A', '항목 B', '항목 C']
    selected_item2 = st.selectbox('리스트에서 선택하세요', list_items2)
