import main.database_class as db
import pytest
import main.crawling_class as craw  # 적절한 경로에 따라 변경


def test_craw():
    test_list = ["삼성전자", "현대차", "DB하이텍", "삼부토건"]
    for i in test_list:
        craw.search_craw(i)

def test_join():
    db.set_user_data("ABCDEFG","")

# pytest로 테스트 실행
if __name__ == "__main__":
    pytest.main()
