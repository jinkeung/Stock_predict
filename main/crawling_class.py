# 외부 라이브러리
from selenium import webdriver as web
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd
import requests as res
from bs4 import BeautifulSoup as bs
import logging
import logging_config
import logging_time_config

Log = logging.getLogger()

# 주식명, 주식코드, 뉴스 크롤링
def search_craw(search):
    try:
        op = Options()
        op.add_argument("headless")
        driver = web.Chrome(op)
        driver.get("https://finance.naver.com/")
        driver.implicitly_wait(1)
        driver.find_element(By.XPATH,'//*[@id="stock_items"]').send_keys(search)
        time.sleep(0.5)
        driver.find_element(By.XPATH,'//*[@id="atcmp"]/div[1]/div/ul/li/a').click()
        res_url = res.get(driver.current_url)
        if res_url.status_code == 200:
            res_data = bs(res_url.content,"lxml")
            news_df = news_craw(driver,res_data)
            type = res_data.find("img").attrs['alt']
            print(type)
            if type == "코스피":
                stock_code = ((res_data.find(attrs={"class","code"}).text) + ".KS")
                stock_name = res_data.find('div', class_='wrap_company').find('h2').find('a').text
            elif type == "코스닥":
                stock_code = ((res_data.find(attrs={"class","code"}).text) + ".KQ")
                stock_name = res_data.find('div', class_='wrap_company').find('h2').find('a').text
        return stock_code, stock_name, news_df
    except Exception as e:
        Log.error(f"데이터 추출중 예외가 발생했습니다 : {e}")
        pass
    finally:
        driver.close()
        driver.quit()
    stock_code=None
    stock_name=None
    news_df=pd.DataFrame(None)
    return stock_code, stock_name, news_df
# 뉴스 크롤링 서브 기능
def news_craw(driver, res_data):
    try:
        titles = []
        urls = []
        test = res_data.select('.sub_section.news_section a:not([class])')
        for data in test:
            titles.append(data.text)
            urls.append("https://finance.naver.com/"+data['href'])
        news_df = pd.DataFrame({'제목': titles, '주소': urls})
        return news_df
    except Exception as e:
        Log.error(f"뉴스 데이터 추출중 예외가 발생했습니다 : " + str(e))
        news_df = pd.DataFrame(None)
        return news_df