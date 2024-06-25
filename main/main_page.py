import webbrowser

import streamlit as st

import numpy as np
import database_class as db
import sub

from crawling_class import stock_craw as craw



import streamlit as st
import database_class as db
import sub

# 전체 페이지 설정
st.set_page_config(page_title='Stock Analysis App', layout='wide')
# 메인 컨텐츠 영역
st.title('Stock Analysis App')

# 사이드바1 - 리스트에서 종목 선택하기
st.sidebar.title('주식 종목 선택')
stock_name = db.return_stock_name()
selected_stock_list = [''] + stock_name
selected_stock = st.sidebar.selectbox('1. 주식 종목을 선택하세요', selected_stock_list)

# 선택된 항목이 공백인 경우 None으로 설정
if selected_stock == '':
    selected_stock = None

# 사이드바에 구분선 추가
st.sidebar.markdown('---')

#사이드바2 - 검색하여 종목 선택하기
search_stock = st.sidebar.text_input('2. 더 많은 종목 정보를 검색하세요 !')
if st.sidebar.button('검색'):
    if search_stock==None and selected_stock==None:
        st.write('주식 종목을 선택하거나 검색하세요.')
    elif search_stock!=None:
        st.write(f'검색한 주식 종목: {search_stock}')
        selected_stock=""
        search_stock_code, search_stock_name =craw.search_craw(search_stock)
        if search_stock_code!=None:
            db.set_all_data(search_stock_code,search_stock_name)
            sub.show_detail(search_stock_name)
        else: st.write("정확한 종목명을 검색해주세요")


if selected_stock is None and (search_stock is None or search_stock == ''):
    st.write('주식 종목을 선택하거나 검색하세요.')
if selected_stock:
    st.write(f'선택한 주식 종목: {selected_stock}')
    selected_stock_code = db.return_stock_code(selected_stock)
    if selected_stock_code !=None:
        db.set_all_data(selected_stock_code,selected_stock)
        sub.show_detail(selected_stock)
    else: st.write("정확한 종목명을 검색해주세요")
















