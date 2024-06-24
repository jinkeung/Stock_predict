import database_class as db
import tkinter as tk
import sub


#메인 화면 구현
main=tk.Tk()
main.geometry('500x500')
main.title('Stock_predict main')

stock_name=db.return_stock_name()


title_font=("나눔고딕",16,"bold")
content_font=("나눔고딕",13)

f_main=tk.Frame()
la_title=tk.Label(f_main,text='Stock Vision: 주식동향 예측 프로그램',font=title_font)
la_title.grid(row=0,column=0)
li_stock_name=tk.Listbox(f_main,width=30,font=content_font)
for i in stock_name:
    li_stock_name.insert("end",i)
li_stock_name.grid(row=1,column=0,pady=20)
li_stock_name.bind("<<ListboxSelect>>",lambda event:sub.list_click(event, li_stock_name))
la_search=tk.Label(f_main,text='더 많은 종목 정보를 검색하세요 !',font=content_font)
la_search.grid(row=2,column=0,pady=10)
e_search=tk.Entry(f_main,font=content_font)
e_search.grid(row=3,column=0,pady=10)
b_search=tk.Button(f_main,text='검색',command=lambda:sub.search_click(e_search.get()))
b_search.grid(row=3,column=1)
f_main.pack(pady=10)
main.mainloop()

