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

    
    with col2:
        # 리스트 1
        st.subheader('최신 뉴스')
        # (stock_craw.news_craw(stock_name))

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
        st.subheader('표 2')
        st.dataframe(df_future_data)