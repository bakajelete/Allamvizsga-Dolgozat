from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from tkcalendar import DateEntry

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import numpy as np

import pandas as pd

import yfinance as yf

from data import *

from datetime import datetime
from dateutil.relativedelta import relativedelta
import time

import Page

class xPage02(Page.Page):
    def __init__(self, root, page_manager):
        Page.Page.__init__(self, root, page_manager)

                #_____Control buttons_____
        self.exit = Button(self, text="EXIT")
        self.exit.bind('<Button-1>', self.go_exit)
        
        self.back = Button(self, text="BACK")
        self.back.bind('<Button-1>', self.go_back)
                
                #_____Imput field for company search_____
        self.companies = ttk.Combobox(self)
        self.companies['values'] = companies_name
        self.companies.bind('<KeyRelease>', self.check_companies)

        self.search = Button(self, text="Search")
        self.search.bind('<Button-1>', self.search_companies)

                #_____Buttons for certain intervall visualization_____ 
        self.one_week = Button(self, text="One week", command = lambda: self.change_vizualization(self, 5))
        
        self.one_month = Button(self, text="One month", command = lambda: self.change_vizualization(self, self.get_days_nr(self.now - relativedelta(months=1))))

        self.three_months = Button(self, text="Three months", command = lambda: self.change_vizualization(self, self.get_days_nr(self.now - relativedelta(months=3))))
        
        self.six_months = Button(self, text="Six months", command = lambda: self.change_vizualization(self, self.get_days_nr(self.now - relativedelta(months=6))))
        
        self.one_year = Button(self, text="One year", command = lambda: self.change_vizualization(self, self.get_days_nr(self.now - relativedelta(years=1)))) 

        self.three_years = Button(self, text="Three years", command = lambda: self.change_vizualization(self, self.get_days_nr(self.now - relativedelta(years=3))))
        
        self.five_years = Button(self, text="Five years", command = lambda: self.change_vizualization(self, self.get_days_nr(self.now - relativedelta(years=5))))      

        self.max_time = Button(self, text="Max time", command = lambda: self.change_vizualization(self, self.data_time_size))


                #_____Buttons for page change_____
        self.more_details = Button(self, text="More Details")
        self.more_details.bind('<Button-1>', self.change_page_to_more_details)
        #self.more_details = Button(self, text="More Details", command = lambda: self.change_page_to_more_details(self))
        
        self.analize_01 = Button(self, text="Bell model")
        self.analize_01.bind('<Button-1>', self.change_page_to_analize_01)

        self.analize_02 = Button(self, text="ARIMA")
        self.analize_02.bind('<Button-1>', self.change_page_to_analize_02)

        self.analize_03 = Button(self, text="Polynomial regression")
        self.analize_03.bind('<Button-1>', self.change_page_to_analize_03)

        self.analize_04 = Button(self, text="04")
        self.analize_04.bind('<Button-1>', self.change_page_to_analize_04)

        self.analize_05 = Button(self, text="05")
        self.analize_05.bind('<Button-1>', self.change_page_to_analize_05)

                #_____Graph abouth the data_____
        self.figure = Figure(figsize=(4, 7), dpi=100)
        
        self.subplot = self.figure.add_subplot(111)

        self.figure.subplots_adjust(left=0.08, right=0.985, bottom=0.08, top=0.985)
        
        self.plots = FigureCanvasTkAgg(self.figure, self)

                #_____Label for information of the graph_____
        self.graph_info = Label(self, text="")
        
                #____Date input for specific time period_____
        self.date_from = Label(self, text="From:", anchor="center")
        self.date_start = DateEntry(self, popanchor="n", date_pattern='YYYY-MM-DD') #, width= 16, date_pattern='YYYY-MM-DD', background= "magenta3", foreground= "white",bd=2)
    
        self.date_to = Label(self, text="To:", anchor="center")
        self.date_end = DateEntry(self, calendar_position='above', date_pattern='YYYY-MM-DD') #, width = 16, date_pattern='YYYY-MM-DD', background= "magenta3", foreground= "white",bd=2)

        self.show_open = Button(self, text="Show", command = lambda: self.change_vizualization_custom(self))

    def show_widgets(self):
        self.root.bind("<Configure>", self.resize_window)
        self.companies.set(self.company_data[0])
        self.resize_window(None)
        self.change_initial_vizualization()
    
    def go_back(self, event):
        self.page_manager.show_page("page01")
        
    def check_companies(self, event):
        value = event.widget.get()

        if value == '':
            self.companies['values'] = companies_name
        else:
            data = []
            for item in companies_name:
                if value.lower() in item.lower():
                    data.append(item)

            self.companies['values'] = data

    def searh_for_ticker(self, company_name):
        
        ok=True
        for companie in companies_info:
            if company_name == companie[0]:
                ok=False
                self.company_data[0] = companie[0]
                self.company_data[1] = companie[1]
                break

        if ok:
            self.company_data[0] = "ERROR"
        
            
    def search_companies(self, event):
        company_name = str(self.companies.get())

        self.ticker = self.searh_for_ticker(company_name)

        if self.company_data[0] == "ERROR":
            messagebox.showerror('Python Error', 'Error: No such company in the data base!')
            return
        
        self.historical_data = pd.read_csv("E:/SZAKDOLGOZAT/A_DOLOGZAT/downloads/" + str(self.company_data[1]) + ".csv", index_col = "Date", parse_dates = True)
        self.data_time_size = self.historical_data.shape[0]
        self.new_vizualization_open(5)

    #def get_days_nr(self, date_target):   
    #    return(self.historical_data[self.historical_data.index >= np.datetime64(date_target)].shape[0])
        
    def increased_or_decreased(self, begin, end):

        begin = max(begin, 0.001)
        
        diff = round(begin - end,2)
        diff_percentage = round(abs(diff)*100/begin, 2)
        information = ""
        
        if diff>0:
            information = ": " + str(round(end,2)) + ", change: -" + str(diff) + "(-" + str(diff_percentage) + "%)"
            return "red", information
        elif diff<0:
            information = ": " + str(round(end,2)) + ", change: +" + str(abs(diff)) + "(+" + str(diff_percentage) + "%)"
            return "green", information
        else:
            information = ": " + str(round(end,2)) + ", change: 0(+0%)"
            return "blue", information
        
    def change_initial_vizualization(self):

        self.historical_data = pd.read_csv("E:/SZAKDOLGOZAT/A_DOLOGZAT/downloads/" + str(self.company_data[1]) + ".csv", index_col = "Date", parse_dates = True)
        #print("02 before", id(self.historical_data))
        #print(self.historical_data)

        self.data_time_size = self.historical_data.shape[0]
        self.new_vizualization_open(5)

    def change_vizualization(self, event, period):
        if period > self.data_time_size:
            messagebox.showerror('Python Error', 'Error: Not enough data is loaded!')
            return
   
        self.new_vizualization_open(period)
    
    def new_vizualization_open(self, period):
        
        self.subplot.clear()
        time_period = self.historical_data[["Open"]].tail(period)
        time_period.index = pd.to_datetime(time_period.index, format = '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')

        color, information = self.increased_or_decreased(float(time_period['Open'].head(1)), float(time_period['Open'].tail(1)))
        time_period.plot(use_index=True, y='Open', color = color, grid = True, ax=self.subplot)
        self.plots.draw()
        self.graph_info.config(text = self.company_data[1] + information, fg = color)

    def new_vizualization_all(self, period):
        
        self.subplot.clear()
        time_period = self.historical_data[["Open","High","Low","Close"]].tail(period)
        time_period.index = pd.to_datetime(time_period.index, format = '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')

        color, information = self.increased_or_decreased(float(time_period["Open"].head(1)), float(time_period["Open"].tail(1)))
        time_period.plot(use_index=True, y=["Open","High","Low","Close"], color = ['blue', 'green', 'red', 'yellow'], grid = True, ax=self.subplot)
        self.plots.draw()
        self.graph_info.config(text = self.company_data[1] + information, fg = color)

    def change_page_to_more_details(self, event):        
        self.page_manager.show_page("page03")

    def change_page_to_analize_01(self, event):
        self.page_manager.show_page("page04")

    def change_page_to_analize_02(self, event):
        print("analize_02")
    
    def change_page_to_analize_03(self, event):
        print("analize_03")

    def change_page_to_analize_04(self, event):
        print("analize_04")

    def change_page_to_analize_05(self, event):
        print("analize_05")
    
    def change_vizualization_custom(self, event):

        if len(self.historical_data) == 0:
            messagebox.showerror('Python Error', 'Error: data is not loaded yet!')
            return
            
        start = self.date_start.get_date()
        end = self.date_end.get_date()

        if start > end:
            messagebox.showerror('Python Error', 'Error: the given dates are incorrect!')
            return

        if end > self.now:
            messagebox.showerror('Python Error', 'Error: the given dates are incorrect!')
            return

        self.subplot.clear()

        custom_period = self.historical_data[["Open"]][(self.historical_data.index >= np.datetime64(start)) & (self.historical_data.index <= np.datetime64(end))]
        custom_period.index = pd.to_datetime(custom_period.index, format = '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
            
        color, information = self.increased_or_decreased(float(custom_period["Open"].head(1)), float(custom_period["Open"].tail(1)))
        custom_period.plot(use_index=True, y="Open", color = color, grid = True, ax=self.subplot)
        self.plots.draw()
        self.graph_info.config(text = self.company_data[1] + information, fg = color)
    

    def resize_window(self, event):
        self.end = time.time()
        
        if self.end - self.start < 0.5:
            return

        self.start = time.time()
        
        self.x_len = self.root.winfo_width()
        self.y_len = self.root.winfo_height()
        
        self.box_x = int(self.x_len/35)
        self.box_y = int(self.y_len/18)

        self.x_font = self.box_x * 28/100
        self.y_font = self.box_y * 28/100

                #_____Control buttons_____
        self.exit.place(x=0*self.box_x, y=0, width=3*self.box_x, height=1*self.box_y)
        self.back.place(x=3*self.box_x, y=0, width=3*self.box_x, height=1*self.box_y)
                
                #_____Imput field for company search_____
        self.companies.place(x=12*self.box_x, y=0, width=11*self.box_x, height=1*self.box_y)
        self.search.place(x=23*self.box_x, y=0, width=4*self.box_x, height=1*self.box_y)

                #_____Buttons for certain intervall visualization_____ 
        self.one_week.place(x=0, y=2*self.box_y, width=5*self.box_x, height=1*self.box_y)
        self.one_month.place(x=0, y=4*self.box_y, width=5*self.box_x, height=1*self.box_y)
        self.three_months.place(x=0, y=6*self.box_y, width=5*self.box_x, height=1*self.box_y)
        self.six_months.place(x=0, y=8*self.box_y, width=5*self.box_x, height=1*self.box_y)

        self.one_year.place(x=0, y=10*self.box_y, width=5*self.box_x, height=1*self.box_y)
        self.three_years.place(x=0, y=12*self.box_y, width=5*self.box_x, height=1*self.box_y)
        self.five_years.place(x=0, y=14*self.box_y, width=5*self.box_x, height=1*self.box_y)
        self.max_time.place(x=0, y=16*self.box_y, width=5*self.box_x, height=1*self.box_y)
        
        
                #_____Buttons for page change_____
        self.more_details.place(x=self.x_len-5*self.box_x, y=15*self.box_y, width=5*self.box_x, height=1*self.box_y)
        
        self.analize_01.place(x=6*self.box_x, y=17*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.analize_02.place(x=11*self.box_x, y=17*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.analize_03.place(x=16*self.box_x, y=17*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.analize_04.place(x=21*self.box_x, y=17*self.box_y, width=4*self.box_x, height=1*self.box_y)

        self.analize_05.place(x=26*self.box_x, y=17*self.box_y, width=4*self.box_x, height=1*self.box_y)

                #_____Graph abouth the data_____
        self.subplot.tick_params(axis='x', labelsize = self.x_font)
        self.subplot.tick_params(axis='y', labelsize = self.y_font)
        
        self.plots.get_tk_widget().place(x=5*self.box_x, y=2*self.box_y, width=25*self.box_x, height=14*self.box_y)

                #_____Label for information of the graph_____
        self.graph_info.place(x=9*self.box_x, y=16*self.box_y, width=17*self.box_x, height=1*self.box_y)

                #____Date input for specific time period_____
        self.date_from.place(x=8*self.box_x, y=1*self.box_y, width=3*self.box_x, height=1*self.box_y)
        self.date_start.place(x=11*self.box_x, y=1*self.box_y, width=5*self.box_x, height=1*self.box_y)

        self.date_to.place(x=16*self.box_x, y=1*self.box_y, width=3*self.box_x, height=1*self.box_y)
        self.date_end.place(x=19*self.box_x, y=1*self.box_y, width=5*self.box_x, height=1*self.box_y)

        self.show_open.place(x=24*self.box_x, y=1*self.box_y, width=4*self.box_x, height=1*self.box_y)


        
