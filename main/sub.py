import tkinter as tk
import database_class as db
from crawling_class import stock_craw as craw
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import webbrowser
from ai_class import machine_learning as learn



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
    stock_code=craw.search_craw(stock_name)
    db.set_all_data(stock_code,stock_name)
    open_detail(stock_name,stock_code)

#상세 페이지
def open_detail(stock_name, stock_code):

    detail_page = tk.Tk()
    detail_page.title("주식 예측 상세 내용")
    detail_page.geometry("1600x800+150+100")

    #예측 그래프
    data_df, future_data_df=learn(stock_name)


    # Matplotlib Figure 객체 생성
    fig = Figure(figsize=(8, 3), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(data_df['Date'].iloc[-30:], data_df['Close'].iloc[-30:], label='Actual Prices')
    ax.plot(future_data_df.index, future_data_df['Predicted Price'], label='Predicted Prices', marker='o',markersize=2)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.tick_params(axis='x', rotation=45)
    ax.set_title('Predict for after 30Days')
    ax.legend()
    canvas = FigureCanvasTkAgg(fig,master=detail_page)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0,padx=30,pady=20)

    # 뉴스 타이틀-링크
    def url_open(event):
        data = detail_news.selection()
        if data:
            url = detail_news.item(data, 'values')
            webbrowser.open(url[0])

    news_data = craw.news_craw(stock_name)
    detail_news = ttk.Treeview(detail_page,columns=('주소'), displaycolumns=())
    detail_news.heading('#0',text='제목')
    for index, row in news_data.iterrows():
        detail_news.insert('', tk.END, text=row['제목'], values=row['주소'])
    detail_news.bind('<ButtonRelease-1>', url_open)
    detail_news.grid(row=0, column=1,padx=23)


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


    for i, (date, open_price, high_price, low_price, close_price, adj_close_price, volume) in enumerate(data, start=1):
        detail_list.insert("", tk.END, text=date, values=(open_price, high_price, low_price, close_price, adj_close_price,volume))
    detail_list.grid(row=2, column=0, columnspan=2,padx=20)
    detail_page.mainloop()
    


