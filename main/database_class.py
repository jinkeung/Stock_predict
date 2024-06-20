from crawling_class import stock_craw
import pymysql as db
# StockCrawler 클래스의 인스턴스 생성
crawler = stock_craw()

# 종목 이름과 URL 추출 메서드 호출
crawler.name_craw()

# 종목 코드 추출 메서드 호출
crawler.url_craw()
try: # MySQL 데이터베이스 연결
    con = db.connect(host='localhost',
                     user='root',
                     password='root',
                     db='stock_db')
    cursor = con.cursor()
    for name, code in zip(crawler.stock_name,crawler.stock_code):
        sql = "INSERT INTO stock_list (stock_name, stock_code) VALUES (%s, %s)"
        cursor.execute(sql, (name, code))
    con.commit()
    con.close()
except Exception as e:
    print(e)