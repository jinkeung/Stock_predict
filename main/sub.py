import tkinter as tk
import database_class as db
from crawling_class import stock_craw as crawl
#리스트 클릭시
def list_click(event,list):
    index=list.curselection()
    if index:
        stock_name = list.get(index)
        stock_code = db.return_stock_code(stock_name)
        db.get_all_data(stock_code,stock_name)
        open_detail(stock_name,stock_code)


#검색 클릭시
def search_click(stock_name):
    stock_name=stock_name
    stock_code=crawl.search_craw(stock_name)
    db.get_all_data(stock_code,stock_name)
    open_detail(stock_name,stock_code)

def open_detail(stock_name,stock_code):
    detail_page=tk.Toplevel()


