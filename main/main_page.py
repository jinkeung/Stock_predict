import streamlit as st
import pandas as pd
import numpy as np
import database_class as db
from crawling_class import stock_craw 
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
    st.subheader('최신 뉴스')
    # (stock_craw.news_craw(stock_name))
    data = {
    '이름': ['뉴스1', '뉴스2', '뉴스3','뉴스4', '뉴스5', '뉴스6'],
    '링크': ['https://www.naver.com', 'https://www.daum.net', 'https://www.google.com','https://www.naver.com', 'https://www.daum.net', 'https://www.google.com']
    }
    df = pd.DataFrame(data)
    
    table_data = []
    for index, row in df.iterrows():
        link = f"<a href='{row['링크']}' target='_blank'>{row['이름']}</a>"
        table_data.append([link])
    st.markdown(
    """
    <style>
    .dataframe {
        width: 100%;
        margin-left: 5px;
        position:relative;
        top:-15px;
    }
    .dataframe td, .dataframe th {
        text-align:center;
    }
    </style>
    """,
    unsafe_allow_html=True
    )
    link_df = pd.DataFrame(table_data, columns=['뉴스 데이터'])
    st.write(link_df.to_html(escape=False, index=False), unsafe_allow_html=True)

st.subheader('주식 상세 데이터')
stock_table = pd.DataFrame(db.return_show_data(selected_stock))
st.markdown(
    """
    <style>
    #9dec169d {
        position:relative;
        top:-10px;
    }
    </style>
    """,
    unsafe_allow_html=True
    )
st.write(stock_table.to_html(escape=False, index=False), unsafe_allow_html=True)

# 두 번째 블록 (차트 2와 리스트 2)
col3, col4 = st.columns([2, 1])

with col3:
    st.subheader('주식 예측 그래프')
    df_chart2 = pd.DataFrame(
        np.random.randn(30, 2),
        columns=['X', 'Y']
    )
    st.line_chart(df_chart2)

with col4:
    # 리스트 2
    st.subheader('주식 예측 데이터')
    list_items2 = ['항목 A', '항목 B', '항목 C']
    selected_item2 = st.selectbox('리스트에서 선택하세요', list_items2)
