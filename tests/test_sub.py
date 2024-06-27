import main.database_class as db
import main.crawling_class as craw
import logging


def test_craw():
    test_list=["삼성전자","현대차"]
    code_list=[]
    name_list=[]
    news_df_list=[]
    for i in test_list:
        stock_code, stock_name, news_df= craw.search_craw(i)
        code_list.append(stock_code)
        name_list.append(stock_name)
        news_df_list.append(news_df)
    print(f"code_list={code_list}")
    print(f"name_list={name_list}")
    print(f"news_df_list={news_df_list}")

def test_join():
    db.set_user_dat