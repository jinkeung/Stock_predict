import requests as res
from bs4 import BeautifulSoup as bs


driver = res.get("https://finance.naver.com/")
if driver.status_code == 200:
    driver_html = bs(driver, "lxml")
    driver_html.find_all()

driver.find_element(By.XPATH,'//*[@id="stock_items"]').send_keys(search)
time.sleep(0.5)
driver.find_element(By.XPATH,'//*[@id="atcmp"]/div[1]/div/ul/li/a').click()
type=driver.find_element(By.XPATH,'//*[@id="middle"]/div[1]/div[1]/div/img').get_attribute('alt')
if type=="코스피":
    stock_code = ((driver.find_element(By.XPATH,'//*[@id="middle"]/div[1]/div[1]/div/span[1]').text) + ".KS")
    stock_name = driver.find_element(By.XPATH,'//*[@id="middle"]/div[1]/div[1]/h2/a').text
elif type=="코스닥":
    stock_code = ((driver.find_element(By.XPATH,'//*[@id="middle"]/div[1]/div[1]/div/span[1]').text) + ".KQ")
    stock_name = driver.find_element(By.XPATH,'//*[@id="middle"]/div[1]/div[1]/h2/a').text
news_df=news_craw(driver)
return stock_code, stock_name, news_df