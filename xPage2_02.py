from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib
import matplotlib.pyplot as plt

import numpy as np

import pandas as pd

import yfinance as yf

from data import *

class MyWindow:
    
    def __init__(self, root):

        self.width = 770
        self.height = 396
        self.box = 22
        self.ticker = ''
        self.historical_data = []
        
                #_____Imput field for company search_____ 
        self.companies = ttk.Combobox(root)
        self.companies['values'] = companies_01
        self.companies.bind('<KeyRelease>', self.check_companies)
        self.companies.place(x=12*self.box, y=1*self.box,width=11*self.box, height=1*self.box)

        self.search = Button(root, text="Search")
        self.search.bind('<Button-1>', self.search_companies)
        self.search.place(x=23*self.box, y=1*self.box,width=4*self.box,height=1*self.box)

                #_____Buttons for certain intervall visualization_____ 
        self.one_week = Button(root, text="One week")
        self.one_week.bind('<Button-1>', self.change_vizualization_ow)
        self.one_week.place(x=1*self.box, y=4*self.box,width=5*self.box,height=1*self.box)

        self.two_week = Button(root, text="Two weeks")
        self.two_week.bind('<Button-1>', self.change_vizualization_tw)
        self.two_week.place(x=1*self.box, y=7*self.box,width=5*self.box,height=1*self.box)
        
        self.one_month = Button(root, text="One months")
        self.one_month.bind('<Button-1>', self.change_vizualization_om)
        self.one_month.place(x=1*self.box, y=10*self.box,width=5*self.box,height=1*self.box)

        self.six_month = Button(root, text="Six months")
        self.six_month.bind('<Button-1>', self.change_vizualization_sm)
        self.six_month.place(x=1*self.box, y=13*self.box,width=5*self.box,height=1*self.box)
        
        self.one_year = Button(root, text="One year")
        self.one_year.bind('<Button-1>', self.change_vizualization_oy)
        self.one_year.place(x=29*self.box, y=4*self.box,width=5*self.box,height=1*self.box)

        self.five_year = Button(root, text="Five years")
        self.five_year.bind('<Button-1>', self.change_vizualization_fy)
        self.five_year.place(x=29*self.box, y=7*self.box,width=5*self.box,height=1*self.box)

        self.max = Button(root, text="Maximum time")
        self.max.bind('<Button-1>', self.change_vizualization_mt)
        self.max.place(x=29*self.box, y=10*self.box,width=5*self.box,height=1*self.box)

                #_____Buttons for page change_____
        self.more_detail = Button(root, text="More Details")
        self.more_detail.bind('<Button-1>', self.change_page_to_more_details)
        self.more_detail.place(x=29*self.box, y=13*self.box,width=5*self.box,height=1*self.box)
        
        self.analize_01 = Button(root, text="Analize a)")
        self.analize_01.bind('<Button-1>', self.change_page_to_analize_01)
        self.analize_01.place(x=8*self.box, y=16*self.box,width=5*self.box,height=1*self.box)

        self.analize_02 = Button(root, text="Analize b)")
        self.analize_02.bind('<Button-1>', self.change_page_to_analize_02)
        self.analize_02.place(x=15*self.box, y=16*self.box,width=5*self.box,height=1*self.box)

        self.analize_03 = Button(root, text="Analize c)")
        self.analize_03.bind('<Button-1>', self.change_page_to_analize_03)
        self.analize_03.place(x=22*self.box, y=16*self.box,width=5*self.box,height=1*self.box)

                #_____Graph abouth the data_____
        self.figure = Figure(figsize=(4.5, 6), dpi=100)
        
        self.subplot = self.figure.add_subplot(111)
        self.subplot.set_ylabel('Value($)', fontsize=6)
        self.subplot.set_xlabel('Time(day)', fontsize=6)
        self.subplot.set_xlim(9, 11)
        self.subplot.set_ylim(9, 11)
        
        self.plots = FigureCanvasTkAgg(self.figure, root)
        self.plots.get_tk_widget().place(x=7*self.box, y=3*self.box,width=21*self.box,height=12*self.box)

                #_____Label for information of the graph_____
        self.graph_info = Label(root, text="")
        self.graph_info.place(x=9*self.box, y=2*self.box,width=17*self.box,height=1*self.box)

    def check_companies(self, event):
        value = event.widget.get()

        if value == '':
            self.companies['values'] = companies_01
        else:
            data = []
            for item in companies_01:
                if value.lower() in item.lower():
                    data.append(item)

            self.companies['values'] = data

    def searh_for_ticker(self, company_name):
        
        ok=True
        for companie in companies_02:
            if company_name == companie[0]:
                ok=False
                return companie[1]
                break

        if ok:
            return "ERROR" 
        
            
    def search_companies(self, event):
        company_name = str(self.companies.get())
        #print(company_name)

        self.ticker = self.searh_for_ticker(company_name)
        #print(self.ticker)

        if self.ticker == "ERROR":
            messagebox.showerror('Python Error', 'Error: No such company in the data base!')
            return
        
        data = yf.download(
            tickers = self.ticker,
            period = "max",
            interval = "1d",
            ignore_tz = False,
            group_by = 'ticker',
            auto_adjust = True,
            prepost = False,
            threads = False,
            proxy = None
            )
        
        data.to_csv("downloads/" + str(self.ticker + ".csv"))

        #self.historical_data = pd.read_csv("downloads/" + str(self.ticker + ".csv"))
        file = open("downloads/" + str(self.ticker + ".csv"), 'r')
        self.historical_data = file.readlines()
        
        self.change_vizualization_ow(event)                                 

    def increased_or_decreased(self, begin_period, end_period):
        
        historical_row_begin = begin_period.strip().split(',')
        num_begin = historical_row_begin[4]
        num_flo_begin = round(float(num_begin), 2)
        
        historical_row_end = end_period.strip().split(',')
        num_end = historical_row_end[4]
        num_flo_end = round(float(num_end), 2)
        
        diff = round(num_flo_begin - num_flo_end,2)
        diff_percentage = round(abs(diff)*100/num_flo_begin, 2)
        information = "" 
        
        if diff>0:
            information = "Curent: " + str(num_flo_end) + ", change: -" + str(diff) + "(-" + str(diff_percentage) + "%)"
            return "red", information
        elif diff<0:
            information = "Curent: " + str(num_flo_end) + ", change: +" + str(abs(diff)) + "(+" + str(diff_percentage) + "%)"
            return "green", information
        else:
            information = "Curent: " + str(num_flo_end) + ", change: 0(+0%)"
            return "blue", information
        
    def change_vizualization_ow(self, event):

        if self.ticker == "ERROR":
            messagebox.showerror('Python Error', 'Error: The data is not loaded yet!')
            return
        
        size = len(self.historical_data)
        if size < 7:
            messagebox.showerror('Python Error', 'Error: Not enough data is available yet!')
            return

        self.subplot.clear()
        
        min_val = 2000000000.0
        max_val = 0.0
        x = []
        y = []
        
        for i in range(size-7, size):
            historical_row = self.historical_data[i].strip().split(',')

            num = historical_row[4]
            num_flo = float(num)
            
            min_val = min(min_val, num_flo)
            max_val = max(max_val, num_flo)

            x.append(i-size+7)
            y.append(num_flo)

        dif = (max_val-min_val)*10/100
        color, information = self.increased_or_decreased(self.historical_data[size-7],self.historical_data[size-1])
        
        self.subplot.set_xlim(0, 6)
        self.subplot.set_ylim(min_val-dif, max_val+dif)
        self.subplot.plot(x, y, color, lw=1)
        self.plots.draw()

        self.graph_info.config(text = information, fg = color)
        
    def change_vizualization_tw(self, event):
        if self.ticker == "ERROR":
            messagebox.showerror('Python Error', 'Error: The data is not loaded yet!')
            return
        
        size = len(self.historical_data)
        if size < 14:
            messagebox.showerror('Python Error', 'Error: Not enough data is available yet!')
            return

        self.subplot.clear()
        
        min_val = 2000000000.0
        max_val = 0.0

        x = []
        y = []
        
        for i in range(size-14, size):
            historical_row = self.historical_data[i].strip().split(',')

            num = historical_row[4]
            num_flo = float(num)
            
            min_val = min(min_val, num_flo)
            max_val = max(max_val, num_flo)

            x.append(i-size+14)
            y.append(num_flo)

        dif = (max_val-min_val)*10/100
        color, information = self.increased_or_decreased(self.historical_data[size-14],self.historical_data[size-1])
        
        self.subplot.set_xlim(0, 13)
        self.subplot.set_ylim(min_val-dif, max_val+dif)
        self.subplot.plot(x, y, color, lw=1)
        self.plots.draw()

        self.graph_info.config(text = information, fg = color)

    def change_vizualization_om(self, event):
        if self.ticker == "ERROR":
            messagebox.showerror('Python Error', 'Error: The data is not loaded yet!')
            return
        
        size = len(self.historical_data)
        if size < 30:
            messagebox.showerror('Python Error', 'Error: Not enough data is available yet!')
            return

        self.subplot.clear()
        
        min_val = 2000000000.0
        max_val = 0.0

        x = []
        y = []
        
        for i in range(size-30, size):
            historical_row = self.historical_data[i].strip().split(',')

            num = historical_row[4]
            num_flo = float(num)
            
            min_val = min(min_val, num_flo)
            max_val = max(max_val, num_flo)

            x.append(i-size+30)
            y.append(num_flo)

        dif = (max_val-min_val)*10/100
        color, information = self.increased_or_decreased(self.historical_data[size-30],self.historical_data[size-1])

        self.subplot.set_xlim(0, 29)
        self.subplot.set_ylim(min_val-dif, max_val+dif)
        self.subplot.plot(x, y, color, lw=1)
        self.plots.draw()
        
        self.graph_info.config(text = information, fg = color)

    def change_vizualization_sm(self, event):
        if self.ticker == "ERROR":
            messagebox.showerror('Python Error', 'Error: The data is not loaded yet!')
            return
        
        size = len(self.historical_data)
        if size < 180:
            messagebox.showerror('Python Error', 'Error: Not enough data is available yet!')
            return

        self.subplot.clear()
        
        min_val = 2000000000.0
        max_val = 0.0

        x = []
        y = []
        
        for i in range(size-180, size):
            historical_row = self.historical_data[i].strip().split(',')

            num = historical_row[4]
            num_flo = float(num)
            
            min_val = min(min_val, num_flo)
            max_val = max(max_val, num_flo)

            x.append(i-size+180)
            y.append(num_flo)

        dif = (max_val-min_val)*10/100
        color, information = self.increased_or_decreased(self.historical_data[size-180],self.historical_data[size-1])

        self.subplot.set_xlim(0, 179)
        self.subplot.set_ylim(min_val-dif, max_val+dif)
        self.subplot.plot(x, y, color, lw=1)
        self.plots.draw()
        
        self.graph_info.config(text = information, fg = color)

    def change_vizualization_oy(self, event):
        if self.ticker == "ERROR":
            messagebox.showerror('Python Error', 'Error: The data is not loaded yet!')
            return
        
        size = len(self.historical_data)
        if size < 365:
            messagebox.showerror('Python Error', 'Error: Not enough data is available yet!')
            return

        self.subplot.clear()
        
        size = len(self.historical_data)
        min_val = 2000000000.0
        max_val = 0.0

        x = []
        y = []
        
        for i in range(size-365, size):
            historical_row = self.historical_data[i].strip().split(',')

            num = historical_row[4]
            num_flo = float(num)
            
            min_val = min(min_val, num_flo)
            max_val = max(max_val, num_flo)

            x.append(i-size+365)
            y.append(num_flo)

        dif = (max_val-min_val)*10/100
        color, information = self.increased_or_decreased(self.historical_data[size-365],self.historical_data[size-1])

        self.subplot.set_xlim(0, 364)
        self.subplot.set_ylim(min_val-dif, max_val+dif)
        self.subplot.plot(x, y, color, lw=1)
        self.plots.draw()
        
        self.graph_info.config(text = information, fg = color)

    def change_vizualization_fy(self, event):
        if self.ticker == "ERROR":
            messagebox.showerror('Python Error', 'Error: The data is not loaded yet!')
            return
        
        size = len(self.historical_data)
        if size < 1825:
            messagebox.showerror('Python Error', 'Error: Not enough data is available yet!')
            return

        self.subplot.clear()
        
        size = len(self.historical_data)
        min_val = 2000000000.0
        max_val = 0.0

        x = []
        y = []
        
        for i in range(size-1825, size):
            historical_row = self.historical_data[i].strip().split(',')

            num = historical_row[4]
            num_flo = float(num)
            
            min_val = min(min_val, num_flo)
            max_val = max(max_val, num_flo)

            x.append(i-size+1825)
            y.append(num_flo)

        dif = (max_val-min_val)*10/100
        color, information = self.increased_or_decreased(self.historical_data[size-1825],self.historical_data[size-1])

        self.subplot.set_xlim(0, 1824)
        self.subplot.set_ylim(min_val-dif, max_val+dif)
        self.subplot.plot(x, y, color, lw=1)
        self.plots.draw()
        
        self.graph_info.config(text = information, fg = color)

    def change_vizualization_mt(self, event):
        if self.ticker == "ERROR":
            messagebox.showerror('Python Error', 'Error: The data is not loaded yet!')
            return
        
        self.subplot.clear()
        
        size = len(self.historical_data)
        min_val = 2000000000.0
        max_val = 0.0

        x = []
        y = []
        
        for i in range(1, size):
            historical_row = self.historical_data[i].strip().split(',')

            num = historical_row[4]
            num_flo = float(num)
            
            min_val = min(min_val, num_flo)
            max_val = max(max_val, num_flo)

            x.append(i)
            y.append(num_flo)

        dif = (max_val-min_val)*10/100
        color, information = self.increased_or_decreased(self.historical_data[1],self.historical_data[size-1])

        self.subplot.set_xlim(0, size-2)
        self.subplot.set_ylim(min_val-dif, max_val+dif)
        self.subplot.plot(x, y, color, lw=1)
        self.plots.draw()
        
        self.graph_info.config(text = information, fg = color)

    def change_page_to_more_details(self, event):
        print("More Details")

    def change_page_to_analize_01(self, event):
        print("analize_01")

    def change_page_to_analize_02(self, event):
        print("analize_02")
    
    def change_page_to_analize_03(self, event):
        print("analize_03")
        
        
root = Tk()
root.geometry("770x396")
#a laptopom full parameterei 1540x1080
#beegetve jol nez ki full kepernyo 1540x792
#1540 = 2^2*5*7*11, 792=2^3*3^2*11 

page2 = MyWindow(root)
root.title('My model')

a = root.winfo_reqwidth()
b = root.winfo_height()

root.mainloop()
