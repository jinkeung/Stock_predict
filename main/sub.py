import database_class as db
from crawling_class import stock_craw as craw
import streamlit as st
import ai_class as learn
import pandas as pd



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
        st.subheader('최신 뉴스')
        # (stock_craw.news_craw(stock_name))

        df_news = craw.news_craw(selected_stock)

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
        # 차트 2
        st.subheader(f'{selected_stock} 향후 30일간 예측 주가')
        st.line_chart(df_future_data.set_index('Date')['Predicted Price'])

    with col4:

        # 리스트 2
        st.subheader('표 2')
        st.dataframe(df_future_data)