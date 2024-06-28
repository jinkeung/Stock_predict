import main.database_class as db
import pytest
import main.crawling_class as craw  # 적절한 경로에 따라 변경


# 크롤링 통해 종목코드, 이름, 뉴스데이터 가져오기
def test_craw(test_list):

    code_list=[]
    name_list=[]
    news_df_list=[]
    for i in test_list:
        stock_code, stock_name, news_df= craw.search_craw(i)
        code_list.append(stock_code)
        name_list.append(stock_name)
        news_df_list.append(news_df)

    return code_list, name_list

#가져온 종목코드, 이름으로 5년치 데이터 db에 적재
def test_set_data(code_list,name_list):
    for i,j in zip(code_list,name_list):
        db.set_all_data(i,j)


test_list=['SK이노베이션', '이수페타시스', '삼성전자', '금양', '에이치브이엠', '대한해운', '에코프로비엠', 'HLB', '하이젠알앤엠', '시노펙스', '삼성SDI', 'POSCO홀딩스', '알테오젠', 'SKC', 'NAVER', 'SK하이닉스', '현대차', '에코프로', '두산에너빌리티', 'HMM', '삼성공조', '대원전선', 'LG디스플레이', '한국가스공사', '포스코인터내셔널', '대한전선', '흥아해운', 'LS', '데브시스터즈', 'SK']
test_code_li, test_name_li=test_craw(test_list)
test_set_data(test_code_li,test_name_li)


#회원가입
def test_join():
    db.set_user_data("join_id","join_pwd","join_name")

#가입한 데이터로 매칭
def test_login():
    login_success=db.return_user_data("join_id","join_pwd")
    assert login_success==True

# pytest로 테스트 실행
if __name__ == "__main__":
    pytest.main()
