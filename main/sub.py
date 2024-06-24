import tkinter as tk
import database_class as db
from crawling_class import stock_craw as crawl
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import webbrowser




#리스트 클릭시
def list_click(event,list):
    index=list.curselection()
    if index:
        stock_name = list.get(index)
        stock_code = db.return_stock_code(stock_name)
        db.set_all_data(stock_code,stock_name)
        open_detail(stock_name,stock_code)

#검색 클릭시
def search_click(stock_name):
    stock_name=stock_name
    stock_code=crawl.search_craw(stock_name)
    db.set_all_data(stock_code,stock_name)
    open_detail(stock_name,stock_code)

#상세 페이지
def open_detail(stock_name, stock_code):

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
    news_data = crawl.news_craw(stock_name)
    detail_news = ttk.Treeview(detail_page,columns=('주소'), displaycolumns=())
    detail_news.heading('#0',text='제목')
    for index, row in news_data.iterrows():
        detail_news.insert('', tk.END, text=row['제목'], values=row['주소'])
    detail_news.bind('<ButtonRelease-1>', url_open)
    detail_news.grid(row=0, column=1,padx=23)
    # ----
    # 트리뷰 columns 값 설정
    detail_list = ttk.Treeview(detail_page, columns=('시가','고가','저가','종가','수정 종가','거래량'))
    detail_list.heading("#0", text="날짜")
    for col in detail_list['columns']:
        detail_list.heading(col, text=col)
    detail_list.column("#0", width=150)
    detail_list.column("시가", width=150,anchor="center")
    detail_list.column("고가", width=150,anchor="center")
    detail_list.column("저가", width=150,anchor="center")
    detail_list.column("종가", width=150,anchor="center")
    detail_list.column("수정 종가", width=150,anchor="center")
    detail_list.column("거래량", width=150,anchor="center")


    # 데이터 가져오기
    data = db.return_show_data(stock_name).values
    print(data)

    for i, (date, open_price, high_price, low_price, close_price, adj_close_price, volume) in enumerate(data, start=1):
        detail_list.insert("", tk.END, text=date, values=(open_price, high_price, low_price, close_price, adj_close_price,volume))
    detail_list.grid(row=2, column=0, columnspan=2,padx=20)
    detail_page.mainloop()
    


