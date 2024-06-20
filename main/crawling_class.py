import requests as res
from bs4 import BeautifulSoup as bs

class stock_craw:
    def __init__(self):
        self.stock_name = []  # 종목 이름
        self.stock_url = []   # 종목 URL
        self.stock_code = []  # 종목 코드

    def name_craw(self):
        stock_list_res = res.get("https://finance.naver.com/sise/lastsearch2.naver")
        if stock_list_res.status_code == 200:
            stock_list_html = bs(stock_list_res.text, "lxml")
            count = 0
            for data in stock_list_html.find_all(attrs={"class": "tltle"}):
                if count < 10:
                    count += 1
                    self.stock_name.append(data.get_text())  # 종목 이름 추가
                    self.stock_url.append(data['href'])      # 종목 URL 추가
                else:
                    break
    def url_craw(self):
        base_url = "http://finance.naver.com"
        for code in self.stock_url:
            full_url = base_url + code
            temp_url = res.get(full_url)
            if temp_url.status_code == 200:
                temp_url_html = bs(temp_url.text, "lxml")
                if temp_url_html.find(attrs={"alt": "코스피"}):
                    stock_code_source = temp_url_html.find(attrs={"class": "code"}).text
                    self.stock_code.append(stock_code_source + ".KS")
                elif temp_url_html.find(attrs={"alt": "코스닥"}):
                    stock_code_source = temp_url_html.find(attrs={"class": "code"}).text
                    self.stock_code.append(stock_code_source + ".KQ")

                   
    