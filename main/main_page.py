import streamlit as st # GUI 라이브러리
# 다른 클래스를 접근하기 위함
import sub 
import database_class as db 
from crawling_class import stock_craw as craw

# 전체 페이지 설정 [ url 제목 ]
st.set_page_config(page_title='Stock Analysis App', layout='wide')
# 메인 컨텐츠 영역
st.title('Stock Analysis App')
# 사이드 - 리스트에서 종목 선택하기
st.sidebar.title('주식 종목 선택')
stock_name_list =[''] + db.return_stock_name() # db 10개의 기본 리스트 가져오기
selected_stock = st.sidebar.selectbox('1. 주식 종목을 선택하세요', stock_name_list) # 하나 선택하는 변수
# selected_stock 공백 시 None값 주입
if selected_stock == '':
    selected_stock = None
# 사이드 에 구분선 추가
st.sidebar.markdown('---')
#사이드 - 검색하여 종목 선택하기
search_stock = st.sidebar.text_input('2. 더 많은 종목 정보를 검색하세요 !')
if st.sidebar.button('검색하기'): # 검색 트리거 버튼
    if (search_stock == None) and (selected_stock == None):
        st.write('주식 종목을 선택하거나 검색하세요.') # 값이 없을 시 기본 출력
    elif search_stock:
        st.write(f'검색한 주식 종목: {search_stock}')
        selected_stock=''
        search_stock_code, search_stock_name =craw.search_craw(search_stock) # 입력받은 값 트리거
        if search_stock_code: # 검색된 주식 코드 값이 존재 시
            # 입력받은 값으로 주식 코드와, 주식 이름을 넣어 db에 적재
            db.set_all_data(search_stock_code,search_stock_name)
            # db에 적재 후 그 값을 가져와 프론트에 출력
            sub.show_detail(search_stock_name)
        # 값이 없을 경우
        else: st.write("정확한 종목명을 검색해주세요")
# 주식 종목을 선택했거
if (selected_stock == None) and ((search_stock == None) or (search_stock == '')):
    st.write('주식 종목을 선택하거나 검색하세요.')
if selected_stock:
    st.write(f'선택한 주식 종목: {selected_stock}')
    selected_stock_code = db.return_stock_code(selected_stock)
    if selected_stock_code:
        db.set_all_data(selected_stock_code,selected_stock)
        sub.show_detail(selected_stock)
    else: st.write("정확한 종목명을 검색해주세요")
