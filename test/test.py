# 2024_06_25 - 수정 사항 

# crawling_class
# 혼자 클래스 존재하여 클래스 제거 작업
# └ 그로 인한 import 수정 작업
# 모두 def 코드문으로 정리 

# database_class
# 외부 클래스중 사용되지 않는 import 제거
# set_user_data() - 회원정보 데이터베이스 적재 def 생성
# return_user_data() - 로그인 데이터베이스 비교 def 생성

# main_page
# 외부 라이브러리 사용되지 않는 import 제거

# sub 
# 외부 클래스중 클래스 제거 작업으로 import문 변경 - crawling_class
# show_stock() - 상세 페이지 def 생성
# show_detail() => show_stock_func() - 상세 페이지 기능 def 생성
#     레이아웃 2,1,2 로 변경
#     markdown - css 통합, 가장 상위로 코드문 이동
#     stock_graph, news_list - 1 레이아웃
#         news_list - CSS 보정
#     stock_real_list_container - 2 레이아웃
#         with 변환
#     stock_predict_graph, stock_predict_list - 3 레이아웃
#         def명 변경, 디자인 보정
# show_login - 로그인 페이지 def 생성
# show_join - 회원가입 페이지 def 생성

# ai_class
# import 간결화, def 코드문 정리