import streamlit as st # GUI 라이브러리
# 다른 클래스를 접근하기 위함
import sub 
import database_class as db 
from crawling_class import stock_craw as craw
import ai_class as learn

import pandas as pd
import plotly.graph_objects as go

# 전체 페이지 설정 [ url 제목 ]
st.set_page_config(page_title='Stock Analysis App', layout='wide')
# 메인 컨텐츠 영역
st.title('Stock Analysis App')
# 사이드 - 리스트에서 종목 선택하기
st.sidebar.title('주식 종목 선택')
#사이드 - 검색하여 종목 선택하기

def grap(graph_type):
    df_data, df_future_data = learn.machine_learning(stock_name)
    df_future_data['Date'] = pd.to_datetime(df_future_data['Date']).dt.date
    df_future_data['Predicted Price'] = df_future_data['Predicted Price'].round(-1).astype(int)
    graph_data_df=db.return_graph_data(stock_name)


    # 첫 번째 블록 (차트 1과 리스트 1)
    col1, col2 = st.columns([2, 1])
    with col1:
        # 사이드 에 구분선 추가
        st.sidebar.markdown('---')
        candlestick=go.Candlestick(x=graph_data_df['날짜'],open=graph_data_df['시가'],
                                   high=graph_data_df['고가'],low=graph_data_df['저가'],close=graph_data_df['종가'])
        line=go.Scatter(x=graph_data_df["날짜"],y=graph_data_df["종가"], mode="lines",name="종가")
        # 차트 1
        st.subheader(f'{stock_name} 실제 주가')
        if graph_type=="Candle_stick":
            fig=go.Figure(candlestick)
        elif graph_type=="Line":
            fig=go.Figure(line)
        else:
            st.error("ERROR")

        st.plotly_chart(fig)
input_stock_name = st.sidebar.text_input('1. 종목을 검색하세요!')
graph_type=st.sidebar.radio("차트 종류를 선택하세요",("Candle_stick","Line"))
if input_stock_name == None or input_stock_name == "":
    st.write('주식 종목을 선택하거나 검색하세요.') 
if st.sidebar.button('검색하기'): # 검색 트리거 버튼
    if input_stock_name == None or input_stock_name == "":
         pass
    elif input_stock_name:
        stock_code, stock_name =craw.search_craw(input_stock_name) # 입력받은 값 트리거
        if stock_code: # 검색된 주식 코드 값이 존재 시
            # 입력받은 값으로 주식 코드와, 주식 이름을 넣어 db에 적재
            db.set_all_data(stock_code,stock_name)
            # db에 적재 후 그 값을 가져와 프론트에 출력
            sub.show_detail(stock_name)
        # 값이 없을 경우
        else: st.write("정확한 종목명을 검색해주세요")
