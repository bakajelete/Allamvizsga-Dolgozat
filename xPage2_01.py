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
    
    def __init__(self, win):

        self.width = 770
        self.height = 396
        self.box = 22
        self.ticker = ''
        self.historical_data = []
        
                #_____Imput field for company search_____ 
        self.companies = ttk.Combobox(win)
        self.companies['values'] = companies_01
        self.companies.bind('<KeyRelease>', self.check_companies)
        self.companies.place(x=12*self.box, y=1*self.box,width=11*self.box, height=1*self.box)

        self.search = Button(win, text="Search")
        self.search.bind('<Button-1>', self.search_companies)
        self.search.place(x=23*self.box, y=1*self.box,width=4*self.box,height=1*self.box)

                #_____Buttons for certain intervall visualization_____ 
        self.one_week = Button(win, text="One week")
        self.one_week.bind('<Button-1>', self.change_vizualization_ow)
        self.one_week.place(x=1*self.box, y=4*self.box,width=5*self.box,height=1*self.box)

        self.two_week = Button(win, text="Two weeks")
        self.two_week.bind('<Button-1>', self.change_vizualization_tw)
        self.two_week.place(x=1*self.box, y=7*self.box,width=5*self.box,height=1*self.box)
        
        self.one_month = Button(win, text="One months")
        self.one_month.bind('<Button-1>', self.change_vizualization_om)
        self.one_month.place(x=1*self.box, y=10*self.box,width=5*self.box,height=1*self.box)

        self.six_month = Button(win, text="Six months")
        self.six_month.bind('<Button-1>', self.change_vizualization_sm)
        self.six_month.place(x=1*self.box, y=13*self.box,width=5*self.box,height=1*self.box)
        
        self.one_year = Button(win, text="One year")
        self.one_year.bind('<Button-1>', self.change_vizualization_oy)
        self.one_year.place(x=29*self.box, y=4*self.box,width=5*self.box,height=1*self.box)

        self.five_year = Button(win, text="Five years")
        self.five_year.bind('<Button-1>', self.change_vizualization_fy)
        self.five_year.place(x=29*self.box, y=7*self.box,width=5*self.box,height=1*self.box)

        self.max = Button(win, text="Maximum time")
        self.max.bind('<Button-1>', self.change_vizualization_mt)
        self.max.place(x=29*self.box, y=10*self.box,width=5*self.box,height=1*self.box)

                #_____Buttons for page change_____
        self.more_detail = Button(win, text="More Details")
        self.more_detail.bind('<Button-1>', self.change_page_to_more_details)
        self.more_detail.place(x=29*self.box, y=13*self.box,width=5*self.box,height=1*self.box)
        
        self.analize_01 = Button(win, text="Analize a)")
        self.analize_01.bind('<Button-1>', self.change_page_to_analize_01)
        self.analize_01.place(x=8*self.box, y=16*self.box,width=5*self.box,height=1*self.box)

        self.analize_02 = Button(win, text="Analize b)")
        self.analize_02.bind('<Button-1>', self.change_page_to_analize_02)
        self.analize_02.place(x=15*self.box, y=16*self.box,width=5*self.box,height=1*self.box)

        self.analize_03 = Button(win, text="Analize c)")
        self.analize_03.bind('<Button-1>', self.change_page_to_analize_03)
        self.analize_03.place(x=22*self.box, y=16*self.box,width=5*self.box,height=1*self.box)

                #_____Graph abouth the data_____
        self.figure = Figure(figsize=(4.5, 6), dpi=100)
        
        self.subplot = self.figure.add_subplot(111)
        self.subplot.set_ylabel('Value($)', fontsize=6)
        self.subplot.set_xlabel('Time(day)', fontsize=6)
        self.subplot.set_xlim(9, 11)
        self.subplot.set_ylim(9, 11)
        
        self.plots = FigureCanvasTkAgg(self.figure, win)
        self.plots.get_tk_widget().place(x=7*self.box, y=3*self.box,width=21*self.box,height=12*self.box)

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
        print(company_name)

        self.ticker = self.searh_for_ticker(company_name)
        print(self.ticker)

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
        

    def change_vizualization(self, option):
        print(option)
        '''
        if self.ticker == "ERROR":
            messagebox.showerror('Python Error', 'Error: No data is loaded yet!')
            return
        
        size = len(self.historical_data)
        min_val = 2000000000
        max_val = 0

        x = []
        y = []
    
        for i in range(size-8, size):
            min_val = min(min_val, self.historical_data[i][4])
            max_val = max(max_val, self.historical_data[i][4])
            x.append(self.historical_data[i][4])
            y.append(self.historical_data[i][0])

        dif = (max_val-min_val)*10/100
        self.subplot.set_ylim(min_val-dif, max_val+dif)
        
        one_week = self.historical_data.tail(7).groupby(by='Date').mean()[["Open","High","Low","Close"]]
        self.subplot.set(one_week.plot.line())
        '''
        print(1)

    def change_vizualization_ow(self, event):
        '''
        if self.ticker == "ERROR":
            messagebox.showerror('Python Error', 'Error: No data is loaded yet!')
            return
        
        size = len(self.historical_data)
        min_val = 2000000000
        max_val = 0

        x = []
        y = []
        
        self.subplot.set_ylim(70, 100)
        one_week = self.historical_data.tail(7).groupby(by='Date').mean()[["Open","High","Low","Close"]]
        one_week.plot.line()
        #self.subplot.set(one_week.plot.line())

        self.plots.draw()
        '''

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

            #x.append(historical_row[0])
            x.append(i-size+7)
            y.append(num_flo)

        dif = (max_val-min_val)*10/100

        self.subplot.set_xlim(0, 6)
        self.subplot.set_ylim(min_val-dif, max_val+dif)
        self.subplot.plot(x, y, 'g', lw=1)
        
        self.plots.draw()
        
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

            #x.append(historical_row[0])
            x.append(i-size+14)
            y.append(num_flo)

        dif = (max_val-min_val)*10/100

        self.subplot.set_xlim(0, 13)
        self.subplot.set_ylim(min_val-dif, max_val+dif)
        self.subplot.plot(x, y, 'g', lw=1)
        
        self.plots.draw()

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

            #x.append(historical_row[0])
            x.append(i-size+30)
            y.append(num_flo)

        dif = (max_val-min_val)*10/100

        self.subplot.set_xlim(0, 29)
        self.subplot.set_ylim(min_val-dif, max_val+dif)
        self.subplot.plot(x, y, 'g', lw=1)
        
        self.plots.draw()

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

            #x.append(historical_row[0])
            x.append(i-size+180)
            y.append(num_flo)

        dif = (max_val-min_val)*10/100

        self.subplot.set_xlim(0, 179)
        self.subplot.set_ylim(min_val-dif, max_val+dif)
        self.subplot.plot(x, y, 'g', lw=1)
        
        self.plots.draw()

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

            #x.append(historical_row[0])
            x.append(i-size+365)
            y.append(num_flo)

        dif = (max_val-min_val)*10/100

        self.subplot.set_xlim(0, 364)
        self.subplot.set_ylim(min_val-dif, max_val+dif)
        self.subplot.plot(x, y, 'g', lw=1)
        
        self.plots.draw()

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

            #x.append(historical_row[0])
            x.append(i-size+1825)
            y.append(num_flo)

        dif = (max_val-min_val)*10/100

        self.subplot.set_xlim(0, 1824)
        self.subplot.set_ylim(min_val-dif, max_val+dif)
        self.subplot.plot(x, y, 'g', lw=1)
        
        self.plots.draw()

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

            #x.append(historical_row[0])
            x.append(i)
            y.append(num_flo)

        dif = (max_val-min_val)*10/100

        self.subplot.set_xlim(0, size-2)
        self.subplot.set_ylim(min_val-dif, max_val+dif)
        self.subplot.plot(x, y, 'g', lw=1)
        
        self.plots.draw()

    def change_page_to_more_details(self, event):
        print("More Details")

    def change_page_to_analize_01(self, event):
        print("analize_01")

    def change_page_to_analize_02(self, event):
        print("analize_02")
    
    def change_page_to_analize_03(self, event):
        print("analize_03")
        
        
window = Tk()
window.geometry("770x396")
#a laptopom full parameterei 1540x1080
#beegetve jol nez ki full kepernyo 1540x792
#1540 = 2^2*5*7*11, 792=2^3*3^2*11 

win = MyWindow(window)
window.title('My model')

a = window.winfo_reqwidth()
b = window.winfo_height()

window.mainloop()
