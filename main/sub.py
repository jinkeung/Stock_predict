import database_class as db
from crawling_class import stock_craw as craw
import streamlit as st
import ai_class as learn
import pandas as pd
import plotly.graph_objects as go



def show_detail(stock_name):


    df_data, df_future_data = learn.machine_learning(stock_name)
    df_future_data['Date'] = pd.to_datetime(df_future_data['Date']).dt.date
    df_future_data['Predicted Price'] = df_future_data['Predicted Price'].round(-1).astype(int)
    graph_data_df=db.return_graph_data(stock_name)


    # 첫 번째 블록 (차트 1과 리스트 1)
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader(f'{stock_name} 실제 주가')
        candlestick=go.Candlestick(x=graph_data_df['날짜'],open=graph_data_df['시가'],
                                   high=graph_data_df['고가'],low=graph_data_df['저가'],close=graph_data_df['종가'])
        fig=go.Figure(candlestick)
        st.plotly_chart(fig)
    with col2:
        # 리스트 1
        st.subheader('최신 뉴스')
        df_news = craw.news_craw(stock_name)

        table_data = []
        for index, row in df_news.iterrows():
            link = f"<a href='{row['주소']}' target='_blank'>{row['제목']}</a>"
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
            [role="grid"] th, [role="grid"] td{
                color:black;
                text-decoration:none;
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
    stock_table = db.return_show_data(stock_name)
    st.markdown(
        """
        <style>
        #9dec169d {
            position:relative;
            top:-10px;
        }
        dvn-scroller {
            text-align:center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.dataframe(stock_table,height=400, width=2000)

    # 두 번째 블록 (차트 2와 리스트 2)
    col3, col4 = st.columns([2, 1])

    with col3:
        # 차트 2
        st.subheader(f'{stock_name} 향후 30일간 예측 주가')
        st.line_chart(df_future_data.set_index('Date')['Predicted Price'])

    with col4:

        # 리스트 2
        st.subheader('')
        st.dataframe(df_future_data)


def main_page():
    # 전체 페이지 설정 [ url 제목 ]
    st.set_page_config(page_title='Stock Analysis App', layout='wide')
    # 메인 컨텐츠 영역
    st.title('Stock Analysis App')

    # 사이드 - 리스트에서 종목 선택하기
    st.sidebar.title('주식 종목 선택')
    #사이드 - 검색하여 종목 선택하기
    input_stock_name = st.sidebar.text_input('1. 종목을 검색하세요!')

    if input_stock_name == None or input_stock_name == "":
        st.write('주식 종목을 선택하거나 검색하세요.') # 값이 없을 시 기본 출력



    if st.sidebar.button('검색하기'): # 검색 트리거 버튼
        if input_stock_name == None or input_stock_name == "":
            pass
        elif input_stock_name:
            stock_code, stock_name =craw.search_craw(input_stock_name) # 입력받은 값 트리거
            if stock_code: # 검색된 주식 코드 값이 존재 시
                # 입력받은 값으로 주식 코드와, 주식 이름을 넣어 db에 적재
                db.set_all_data(stock_code,stock_name)
                # db에 적재 후 그 값을 가져와 프론트에 출력
                show_detail(stock_name)
            # 값이 없을 경우
            else: st.write("정확한 종목명을 검색해주세요")