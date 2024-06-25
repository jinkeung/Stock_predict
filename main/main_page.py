# GUI 라이브러리
import streamlit as st

# 외부 클래스
import sub 
import database_class as db 
import crawling_class as craw

# 전체 페이지 설정 [ url 제목 ]
st.set_page_config(page_title='Stock Analysis App', layout='wide')
# 메인 컨텐츠 영역
st.title('Stock Analysis App')
# 사이드 - 주식 컨텐츠 타이틀
st.sidebar.title('주식 종목 찾아보기')

# 사이드 종목 검색 / 데이터 가져오기
input_stock_name = st.sidebar.text_input('1. 종목을 검색하세요!')

# 초기 값 설정
if input_stock_name == None or input_stock_name == "":
    st.write('주식 종목을 선택하거나 검색하세요.') 

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
            sub.show_stock_func(stock_name)
        # 값이 없을 경우
        else: st.write("정확한 종목명을 검색해주세요")
