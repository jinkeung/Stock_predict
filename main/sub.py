import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from crawling_class import stock_craw
import webbrowser
title_font=("나눔고딕",16,"bold")
content_font=("나눔고딕",13)
def open_detail():
    detail_page = tk.Tk()
    detail_page.title("주식 예측 상세 내용")
    detail_page.geometry("1200x600+150+100")
    fig = Figure(figsize=(6, 3), dpi=100)
    plot = fig.add_subplot(111)
    plot.plot(['A', 'B', 'C', 'D'], [7, 13, 5, 17])

    canvas = FigureCanvasTkAgg(fig,master=detail_page)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0,padx=30,pady=20)

    # 변경된 구간
    def url_open(event):
        data = detail_news.selection()
        if data:
            url = detail_news.item(data, 'values')
            webbrowser.open(url[0])
    news_data = stock_craw.news_craw()
    detail_news = ttk.Treeview(detail_page,columns=('주소'), displaycolumns=())
    detail_news.heading('#0',text='제목')
    for index, row in news_data.iterrows():
        detail_news.insert('', tk.END, text=row['제목'], values=row['주소'])
    detail_news.bind('<ButtonRelease-1>', url_open)
    detail_news.grid(row=0, column=1,padx=23)
    # ----

    # 트리뷰 columns 값 설정
    detail_list = ttk.Treeview(detail_page, columns=('시가','고가','저가','종가','거래량'))
    detail_list.heading("#0", text="날짜")
    for col in detail_list['columns']:
        detail_list.heading(col, text=col)
    
    detail_list.column("#0", width=150)
    detail_list.column("시가", width=150,anchor="center")
    detail_list.column("고가", width=150,anchor="center")
    detail_list.column("저가", width=150,anchor="center")
    detail_list.column("종가", width=150,anchor="center")
    detail_list.column("거래량", width=150,anchor="center")
    # 데이터 추가 (임의의 데이터 예시)
    # 데이터 db 추가
    data = [
        ("2024-06-19", "10000", "11000", "9800", "10500", "100000"),
        ("2024-06-20", "9500", "10500", "9200", "10000", "120000"),
        ("2024-06-21", "9800", "10200", "9500", "9800", "90000"),
    ]

    for i, (date, open_price, high_price, low_price, close_price, volume) in enumerate(data, start=1):
        detail_list.insert("", tk.END, text=date, values=(open_price, high_price, low_price, close_price, volume))
    detail_list.grid(row=2, column=0, columnspan=2,padx=20)
    detail_page.mainloop()
open_detail()
