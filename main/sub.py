# 외부 클래스
import database_class as db
import crawling_class as craw
import ai_class as learn 

# 외부 라이브러리
import streamlit as st 
import pandas as pd 
import plotly.graph_objects as go 

# streamlit 로그인 라이브러리

# 상세 페이지
def show_stock():
    # 메인 컨텐츠 영역
    st.write('누구님 환영합니다')
    st.title('Stock Analysis App')
    # 사이드 - 주식 컨텐츠 타이틀
    st.sidebar.title('주식 종목 찾아보기')

    # 사이드 종목 검색 / 데이터 가져오기
    input_stock_name = st.sidebar.text_input('1. 종목을 검색하세요!')

    # 초기 값 설정
    if input_stock_name == None or input_stock_name == "":
        st.write('주식 종목을 선택하거나 검색하세요.') 
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

    # 검색 버튼
    if st.sidebar.button('검색하기'): 
        if input_stock_name == None or input_stock_name == "":
            pass
        elif input_stock_name:
            # 입력받은 값 트리거
            stock_code, stock_name =craw.search_craw(input_stock_name)
            # 검색된 주식 코드 값이 존재 시
            if stock_code:
                # 입력받은 값으로 주식 코드와, 주식 이름을 넣어 db에 적재
                db.set_all_data(stock_code,stock_name)
                # db에 적재 후 그 값을 가져와 프론트에 출력
                show_stock_func(stock_name)
            # 값이 없을 경우
            else: st.write("정확한 종목명을 검색해주세요")
# 로그인 페이지
# 회원가입 페이지
def show_join():
    st.title("주식 예측 플랫폼에 오신걸 환영합니다!")
    st.write("회원가입을 진행해주세요!")
    join_container = st.container()
    with join_container:
        global Service
        gap1, gap2 = st.columns([1,1])
        gap1.empty(), gap2.empty()
        ext1, ext2, ext3 = st.columns([2,1,1])
        join = ext1
        ext2.empty(), ext3.empty()
        with join:
            
            join_id = st.text_input("아이디")
            join_pwd = st.text_input("비밀번호", type='password')
            join_pwd_chk = st.text_input("비밀번호 확인", type='password')
            join_name = st.text_input("이름")
            gap3, gap4 = st.columns([1,1])
            gap3.empty(), gap4.empty()
            if st.button("회원가입"):
                if (join_pwd and join_pwd_chk) and (join_name and join_id):
                    join_success = db.set_user_data(join_id,join_pwd,join_name)
                    if join_success == True:
                        st.success("회원가입을 축하드립니다!")
                        Service = "로그인"
                    else:
                        st.error("회원가입을 실패하셨습니다")
                else:
                    st.error("비밀번호를 정확히 입력해주세요")


    