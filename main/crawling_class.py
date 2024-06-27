# 외부 라이브러리
from selenium import webdriver as web
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd
import requests as res
from bs4 import BeautifulSoup as bs

# 검색 종목 코드 크롤링
def search_craw(search):
    try:
        op = Options()
        op.add_argument("headless")
        driver = web.Chrome(op)
        driver.get("https://finance.naver.com/")
        driver.implicitly_wait(1)
        driver.find_element(By.XPATH,'//*[@id="stock_items"]').send_keys(se)
        time.sleep(0.5)
        driver.find_element(By.XPATH,'//*[@id="atcmp"]/div[1]/div/ul/li/a').click()
        res_url = res.get(driver.current_url)
        if res_url.status_code == 200:
            res_data = bs(res_url.content,"lxml")
            type = res_data.find("img", {"alt":"코스피"}).attrs['alt']
            if type=="코스피":
                stock_code = ((res_data.find(attrs={"class","code"}).text) + ".KS")
                stock_name = res_data.find('div', class_='wrap_company').find('h2').find('a').text
                print(stock_code, stock_name)
            elif type=="코스닥":
                stock_code = ((res_data.find(attrs={"class","code"}).text) + ".KS")
                stock_name = res_data.find('div', class_='wrap_company').find('h2').find('a').text
                print(stock_code, stock_name)
        news_df = news_craw(driver)
        return stock_code, stock_name, news_df
    except Exception :
        pass
    finally:
        driver.close()
        driver.quit()
    stock_code=None
    stock_name=None
    news_df=None
    return stock_code, stock_name, news_df
# 뉴스 title, url 크롤링
def news_craw(driver):
    try:
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
    except Exception as e:
        print("뉴스 크롤링 예외처리" + str(e))
        news_df = pd.DataFrame(None)
        return news_df