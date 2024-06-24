import requests as res
from bs4 import BeautifulSoup as bs
from selenium import webdriver as web
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import tkinter.messagebox as ms
import time
import pandas as pd
class stock_craw:
    def __init__(self):
        self.stock_name = []  # 종목 이름
        self.stock_url = []   # 종목 URL
        self.stock_code = []  # 종목 코드
    # 10개 종목 리스트 가져오기
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
    # 10개 종목 코드 가져오기
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
    # 검색 종목 코드 가져오기
    def search_craw(search):
        op = Options()
        op.add_argument("headless")
        driver = web.Chrome()
        driver.get("https://finance.naver.com/")
        driver.implicitly_wait(3)
        driver.find_element(By.XPATH,'//*[@id="stock_items"]').send_keys(search)
        time.sleep(1)
        driver.find_element(By.XPATH,'//*[@id="atcmp"]/div[1]/div/ul/li/a').click()
        time.sleep(1)
        if driver.find_element(By.XPATH,'//*[@id="middle"]/div[1]/div[1]/div/img').get_attribute('alt') == '코스피':
            search_stock_code = ((driver.find_element(By.XPATH,'//*[@id="middle"]/div[1]/div[1]/div/span[1]').text) + ".KS")
            return search_stock_code
        elif driver.find_element(By.XPATH,'//*[@id="middle"]/div[1]/div[1]/div/img').get_attribute('alt') == '코스닥':
            search_stock_code = ((driver.find_element(By.XPATH,'//*[@id="middle"]/div[1]/div[1]/div/span[1]').text) + ".KQ")
            return search_stock_code
        else:
            ms.showinfo("확인불가","다시 검색해주세요")
    # 뉴스 title, url
    def news_craw(stock_name):
        op = Options()
        op.add_argument("headless")
        driver = web.Chrome(op)
        driver.get("https://finance.naver.com/")
        driver.implicitly_wait(3)
        driver.find_element(By.XPATH,'//*[@id="stock_items"]').send_keys(stock_name)
        time.sleep(1)
        driver.find_element(By.XPATH,'//*[@id="atcmp"]/div[1]/div/ul/li/a').click()
        time.sleep(1)

        titles = []
        urls = []

        for data in driver.find_elements(By.CLASS_NAME,'news_section'):
            for ud in range(1,3):
                for ld in range(1,6):
                    f_data = data.find_element(By.XPATH,f'//*[@id="content"]/div[3]/div[1]/ul[{ud}]/li[{ld}]/span/a')
                    titles.append(f_data.text)
                    urls.append(f_data.get_attribute('href'))
        news_df = pd.DataFrame({'제목': titles, '주소': urls})
        return news_df