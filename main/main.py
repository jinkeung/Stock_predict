# 주 기능 streamlit 라이브러리
import streamlit as st

# 외부 라이브러리
import re
import logging
import pandas as pd 
import plotly.graph_objects as go 

# 외부 클래스
import database_class as db
import crawling_class as craw
import ai_class as learn

from session_state import get_session

# 페이지 설정
st.set_page_config(page_title='Stock Analysis App', layout='wide')

# 세션 설정
Log = logging.getLogger()
session = get_session()

Log.info("주식 예측 플랫폼이 시작되었습니다.")

# 로그인 페이지
def login():
    st.title("주식 예측 플랫폼에 오신걸 환영합니다!")
    st.write("로그인을 진행해주세요!")

    with st.container():
        login2_1, gap2_2, gap2_3 = st.columns([2,1,1])
        login = login2_1
        gap2_2.empty()
        gap2_3.empty()
        with login:
            login_id = st.text_input("아이디", key="login_id")
            login_pwd = st.text_input("비밀번호", type='password')
            login_button = st.button("로그인",key="login_button")
            join_button = st.button("회원가입",key="join_button")
            if login_button:
                login_success=db.return_user_data(login_id,login_pwd)
                if login_success:
                    st.success(f"{session.u_name}님 환영합니다")
                    st.write("주식 정보를 보러가실 수 있습니다")
                    st.rerun()
                else:
                    st.error("로그인 실패. 아이디와 비밀번호를 확인하세요. 또는 회원가입을 진행해주세요")
            if join_button:
                session.show_join_form = True
    if session.show_join_form:
        with st.form(key="회원가입"):    
            def join_process():
                    join_id = st.session_state.join_id
                    join_pwd = st.session_state.join_pwd
                    join_pwd_chk = st.session_state.join_pwd_chk
                    join_name = st.session_state.join_name
                    # id 정규표현식
                    def chk_id(join_id):
                        result = True
                        reg = r'^[A-Za-z0-9]{4,20}$'
                        if not re.search(reg, join_id):
                            st.error("아이디는 영문 대소문자, 숫자만 사용하여 4-20자 이내로 작성해주세요")
                            result = False
                        return result
                    # pwd 정규표현식
                    def chk_pwd(join_pwd):
                        result = True
                        reg = r'^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$'
                        if join_pwd == join_pwd_chk:
                            if not re.search(reg, join_pwd):
                                st.error("비밀번호는 영문, 숫자, 특수문자를 하나 이상씩 포함하여 8자 이상으로 작성해주세요")
                                result = False
                        else:
                            st.error("비밀번호가 일치하지 않습니다")
                            result = False
                        return result
                    # name 정규표현식
                    def chk_name(join_name):
                        result = True
                        reg = r'^[가-힣a-zA-Z]{1,}$'
                        if not re.search(reg, join_name):
                            st.error("이름을 작성해 주세요")
                            result = False
                        return result
                    re1 = chk_id(join_id)
                    re2 = chk_pwd(join_pwd)
                    re3 = chk_name(join_name)

                    # 정규표현식을 전부 만족하면 db 적재
                    if re1 and re2 and re3:
                        join_success = db.set_user_data(join_id, join_pwd, join_name)
                        if join_success:
                            st.success("축하합니다! 회원가입에 성공하였습니다.")
                            session.show_join_form = False  # Hide join form after successful signup
                        else:
                            st.error("이미 존재하는 아이디입니다.")
            st.title("회원가입")
            
            st.text_input("아이디", key="join_id")
            st.write("영문 대소문자, 숫자만 사용하여 4-20자 이내로 작성해주세요")
            
            st.text_input("비밀번호", type='password', key="join_pwd")
            st.write("영문, 숫자, 특수문자를 하나 이상씩 포함하여 8자 이상으로 작성해주세요")
            st.text_input("비밀번호 확인", type='password', key="join_pwd_chk")
            
            st.text_input("이름", key="join_name")
            
            st.form_submit_button(label="가입하기", on_click=join_process)

# 상세 페이지
def stock():
    st.title('Stock Analysis App [ 주식 예측 플랫폼 ]')
    id, button = st.sidebar.columns([1,1])    
    with id:
        st.write(f'{get_session().u_name}님 환영합니다')
    with button:
        logout_button = st.button("로그아웃")
        if logout_button:
            get_session().login = False
            st.rerun()
    st.sidebar.title('주식 종목 찾아보기')
    input_stock_name = st.sidebar.text_input('1. 종목을 검색하세요!')
    if not input_stock_name:
        st.write('주식 종목을 선택하거나 검색하세요.') 
    def show_stock_func(stock_name, news_df):
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
         
        # 본문 레이아웃
        stock_graph, news_list = st.columns([2, 1])
        stock_real_list_container = st.container()
        stock_predict_graph, stock_predict_list = st.columns([2, 1])

        # 주식 기본, 예측 데이터 불러오기
        graph_data_df=db.return_graph_data(stock_name)
        df_data, df_future_data = learn.machine_learning(stock_name)


        if not(graph_data_df.empty):
            try:
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

                    fig.update_layout(yaxis=dict(tickformat=','))
                    st.plotly_chart(fig)
                # 주식 뉴스 리스트
                with news_list:
                    if news_df.empty == False:
                        table_data = []
                        for index, row in news_df.iterrows():
                            link = f"<a href='{row['주소']}' target='_blank'>{row['제목']}</a>"
                            table_data.append([link])
                        link_df = pd.DataFrame(table_data, columns=['뉴스 데이터'])
                        st.write(link_df.to_html(escape=False, index=False), unsafe_allow_html=True)
                    else:
                        table_data = []
                        for index, row in news_df.iterrows():
                            link = f"<a href='{row['주소']}' target='_blank'>{row['제목']}</a>"
                            table_data.append([link])
                        link_df = pd.DataFrame(table_data, columns=['뉴스 데이터'])
                        st.write(link_df.to_html(escape=False, index=False), unsafe_allow_html=True)
                        st.write("최근 1년 내 검색된 관련뉴스가 없습니다")
                # 주식 상세 데이터
                with stock_real_list_container:
                    st.subheader('주식 상세 데이터')
                    col1,col2 = st.columns([1,1])
                    stock_real_list1 = col1
                    col2.empty()
                    stock_table = db.return_show_data(stock_name)
                    st.dataframe(stock_table,height=400, width=2000)
            except Exception as e:
                Log.error(f"주식 데이터에서 예외 발생했습니다 : {e}")
                st.experimental_rerun()
        else:
            Log.error("주식 기본 데이터가 너무 적습니다")
            st.subheader("상세 주식 데이터")
            st.write("기본 정보 제공을 위한 데이터가 너무 적습니다.")
        # 예측 데이터 출력
        if not(df_data.empty):
            try:
                df_future_data['Date'] = pd.to_datetime(df_future_data['Date']).dt.date
                df_future_data['Predicted Price'] = df_future_data['Predicted Price'].round(-1).astype(int)

                # 예측 그래프
                with stock_predict_graph:
                    st.subheader(f'{stock_name} 예측 주가 [ 30day ]')
                    st.line_chart(df_future_data.set_index('Date')['Predicted Price'])
                # 예측 데이터
                with stock_predict_list:
                    st.subheader(f'{stock_name} 예측 데이터')
                    st.dataframe(df_future_data,height=310, width=400)
            except Exception as e:
                Log.error(f"예측 데이터에서 예외가 발생되었습니다 : {e}")
                st.experimental_rerun()
        else:
            st.subheader("예측 주식 데이터")
            st.write("예측 정보 제공을 위한 데이터가 너무 적습니다.")

    # 검색 버튼
    search_button=st.sidebar.button('검색하기')
    if search_button:
        get_session().search_button=True
    if get_session().search_button==True:
        if input_stock_name == None or input_stock_name == "":
            pass
        elif input_stock_name:
            stock_code, stock_name , news_df =craw.search_craw(input_stock_name)
            # 검색된 주식 코드 값이 존재 시
            if stock_code:
                db.set_all_data(stock_code, stock_name)
                show_stock_func(stock_name,news_df)
            else:
                st.write("정확한 종목명을 검색해주세요")

# 페이지 전환 및 메인 트리거
if __name__ == "__main__":

    if get_session().login == False:
        login()
    elif get_session().login == True:
        stock()
