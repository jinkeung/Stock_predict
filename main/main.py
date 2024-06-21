# from database_class import get_all_data
import tkinter as tk
from crawling_class import stock_craw 

def main_page():
    main=tk.Tk()
    main.geometry('500x500')
    main.title('Stock_predict main')

    stock_name=["가","나","다","라","마","바","사"]




    title_font=("나눔고딕",16,"bold")
    content_font=("나눔고딕",13)

    f_main=tk.Frame()
    la_title=tk.Label(f_main,text='Stock Vision: 주식동향 예측 프로그램',font=title_font)
    la_title.grid(row=0,column=0)
    li_stock_name=tk.Listbox(f_main,width=30,font=content_font)
    for i in stock_name:
        li_stock_name.insert("end",i)
    li_stock_name.grid(row=1,column=0,pady=20)
    la_search=tk.Label(f_main,text='더 많은 종목 정보를 검색하세요 !')
    la_search.grid(row=2,column=0,pady=10)
    e_search=tk.Entry(f_main,font=content_font)
    e_search.grid(row=3,column=0,pady=10)
    b_search=tk.Button(f_main,text='검색',command=lambda: stock_craw.search_craw(e_search.get()))
    b_search.grid(row=3,column=1)
    f_main.pack(pady=10)
    main.mainloop()
main_page()