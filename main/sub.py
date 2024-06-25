# 외부 클래스
import database_class as db
import crawling_class as craw
import ai_class as learn 

# 외부 라이브러리
import streamlit as st 
import pandas as pd 
import plotly.graph_objects as go 

# 상세 페이지
def show_stock():
    pass

# 상세 페이지 기능
def show_stock_func(stock_name):
    
    # CSS 설정
    st.markdown(
        """
        <style>
        .glideDataEditor {
            margin-left:5px;
        }
        .dataframe {
            width: 100%;
            margin-left: 5px;
            position:relative;
            top:-20px;
        }
        a[href]{
            color:black;
            text-decoration:none;
        }
        .dataframe td, .dataframe th {
            text-align:center;
        }
        #9dec169d {
            position:relative;
            top:-20px;
        }
        table[role="grid"]{
            position:relative;
            top:-10px
            text-align:center;
        }
        dvn-scroller {
            text-align:center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # 예측 데이터 출력
    df_data, df_future_data = learn.machine_learning(stock_name)
    df_future_data['Date'] = pd.to_datetime(df_future_data['Date']).dt.date
    df_future_data['Predicted Price'] = df_future_data['Predicted Price'].round(-1).astype(int)
    graph_data_df=db.return_graph_data(stock_name)
    
    # 본문 레이아웃
    stock_graph, news_list = st.columns([2, 1])
    stock_real_list_container = st.container()
    stock_predict_graph, stock_predict_list = st.columns([2, 1])

    # 주식 실질적 그래프
    with stock_graph:
        st.subheader(f'{stock_name} 실제 주가')
        st.sidebar.markdown('---')
        
        candlestick=go.Candlestick(x=graph_data_df['날짜'],open=graph_data_df['시가'],
                                   high=graph_data_df['고가'], low=graph_data_df['저가'], close=graph_data_df['종가'])
        line=go.Scatter(x=graph_data_df["날짜"], y=graph_data_df["종가"],
                        mode="lines", name="종가")    
        graph_type=st.sidebar.radio("차트 종류를 선택하세요",("Candle_stick","Line"))
        
        if graph_type=="Candle_stick": fig=go.Figure(candlestick)
        elif graph_type=="Line": fig=go.Figure(line)
        else: st.error("그래프 생성에 문제가 발생했습니다")
        st.plotly_chart(fig)
    # 주식 뉴스 리스트
    with news_list:
        # (stock_craw.news_craw(stock_name))
        df_news = craw.news_craw(stock_name)
        table_data = []
        for index, row in df_news.iterrows():
            link = f"<a href='{row['주소']}' target='_blank'>{row['제목']}</a>"
            table_data.append([link])
        link_df = pd.DataFrame(table_data, columns=['뉴스 데이터'])
        st.write(link_df.to_html(escape=False, index=False), unsafe_allow_html=True)
    # 주식 상세 데이터
    with stock_real_list_container:
        st.subheader('주식 상세 데이터')
        col1,col2 = st.columns([1,1])
        stock_real_list1 = col1
        col2.empty()
        stock_table = db.return_show_data(stock_name)
        st.dataframe(stock_table,height=400, width=2000)
    # 예측 그래프
    with stock_predict_graph:
        st.subheader(f'{stock_name} 예측 주가 [ 30day ]')
        st.line_chart(df_future_data.set_index('Date')['Predicted Price'])
    # 예측 데이터
    with stock_predict_list:
        st.subheader(f'{stock_name} 예측 데이터')
        st.dataframe(df_future_data,height=310, width=400)

# 로그인 페이지
def show_login():
    pass

# 회원가입 페이지
def show_join():
    pass