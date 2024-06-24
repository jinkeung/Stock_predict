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
def list_click(stock_name):
    stock_code = db.return_stock_code(stock_name)
    db.set_all_data(stock_code,stock_name)


#검색 클릭시
def search_click(stock_name):
    stock_name=stock_name
    stock_code=craw.search_craw(stock_name)
    db.set_all_data(stock_code,stock_name)

