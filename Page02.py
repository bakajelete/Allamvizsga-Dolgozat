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

        self.back = Button(self, text="BACK", command = lambda: self.go_back(self, 'page01'))
                
                #_____Imput field for company search_____
        self.companies = ttk.Combobox(self)
        self.companies['values'] = companies_name
        self.companies.bind('<KeyRelease>', self.check_companies)

        self.search = Button(self, text="Search")
        self.search.bind('<Button-1>', self.search_companies)

                #____Date input for specific time period_____
        self.date_from = Label(self, text="From:", anchor="center")
        self.date_start = DateEntry(self, popanchor="n", date_pattern='YYYY-MM-DD')
    
        self.date_to = Label(self, text="To:", anchor="center")
        self.date_end = DateEntry(self, calendar_position='above', date_pattern='YYYY-MM-DD')

        self.show_open = Button(self, text="Show", anchor="center")
        self.show_open.configure(command = lambda btn=self.show_open: self.change_vizualization_custom(self, btn))

                #_____Buttons for certain intervall visualization_____ 
        self.one_week = Button(self, text="One week", anchor="center")
        self.one_week.configure(command = lambda btn=self.one_week: self.change_vizualization(self, btn, 5))
        
        self.one_month = Button(self, text="One month", anchor="center")
        self.one_month.configure(command = lambda btn=self.one_month: self.change_vizualization(self, btn, self.get_days_nr(self.now - relativedelta(months=1))))
        
        self.three_months = Button(self, text="Three months", anchor="center")
        self.three_months.configure(command = lambda btn=self.three_months: self.change_vizualization(self, btn, self.get_days_nr(self.now - relativedelta(months=3))))
        
        self.six_months = Button(self, text="Six months", anchor="center")
        self.six_months.configure(command = lambda btn=self.six_months: self.change_vizualization(self, btn, self.get_days_nr(self.now - relativedelta(months=6))))

        self.one_year = Button(self, text="One year", anchor="center")
        self.one_year.configure(command = lambda btn=self.one_year: self.change_vizualization(self, btn, self.get_days_nr(self.now - relativedelta(years=1))))
        
        self.three_years = Button(self, text="Three years", anchor="center")
        self.three_years.configure(command = lambda btn=self.three_years: self.change_vizualization(self, btn, self.get_days_nr(self.now - relativedelta(years=3))))

        self.five_years = Button(self, text="Five years", anchor="center")      
        self.five_years.configure(command = lambda btn=self.five_years: self.change_vizualization(self, btn, self.get_days_nr(self.now - relativedelta(years=5))))
        
        self.max_time = Button(self, text="Max time", anchor="center")
        self.max_time.configure(command = lambda btn=self.max_time: self.change_vizualization(self, btn, self.data_time_size))
        
                #_____Company info labels_____
        self.sector = Label(self, text="Sector:", anchor="center")
        self.sector_inf = Label(self, text="", anchor="center")

        self.industry = Label(self, text="Industry:", anchor="center")
        self.industry_inf = Label(self, text="", anchor="center")

        self.market_cap = Label(self, text="Market cap:", anchor="center")
        self.market_cap_inf = Label(self, text="", anchor="center")

        self.country = Label(self, text="Counrty:", anchor="center")
        self.country_inf = Label(self, text="", anchor="center")

                #_____Buttons for page change_____
        self.more_details = Button(self, text="More Details")
        self.more_details.bind('<Button-1>', self.change_page_to_more_details)
        
        self.analize_01 = Button(self, text="Bell model")
        self.analize_01.bind('<Button-1>', self.change_page_to_analize_01)

        self.analize_02 = Button(self, text="SMA crosess")
        self.analize_02.bind('<Button-1>', self.change_page_to_analize_02)

        self.analize_03 = Button(self, text="Polynomial regression")
        self.analize_03.bind('<Button-1>', self.change_page_to_analize_03)

        self.analize_04 = Button(self, text="RBF prediction")
        self.analize_04.bind('<Button-1>', self.change_page_to_analize_04)

        self.analize_05 = Button(self, text="Local probability space")
        self.analize_05.bind('<Button-1>', self.change_page_to_analize_05)

                #_____Graph abouth the data_____
        self.figure = Figure(figsize=(4, 7), dpi=100)
        
        self.subplot = self.figure.add_subplot(111)

        self.figure.subplots_adjust(left=0.08, right=0.985, bottom=0.08, top=0.985)
        
        self.plots = FigureCanvasTkAgg(self.figure, self)

                #_____Label for information of the graph_____
        self.graph_info = Label(self, text="", anchor="center")

    def show_widgets(self):
        self.root.bind("<Configure>", self.resize_window)
        self.companies.set(self.company_data[0])
        
        self.active_button = self.one_week
        self.active_button.config(bg="sky blue")
        self.resize_window(None)

        self.change_initial_vizualization()
        self.all_companies_info = pd.read_csv("E:/SZAKDOLGOZAT/A_DOLOGZAT/downloads/0xALL_COMPANIES.csv")###
        self.refresh_company_info_labeles()###
        
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

        if self.active_button != None:
            self.active_button.config(bg="SystemButtonFace")
        
        self.active_button = self.one_week
        self.active_button.config(bg="sky blue")
        
        self.historical_data = pd.read_csv("E:/SZAKDOLGOZAT/A_DOLOGZAT/downloads/" + str(self.company_data[1]) + ".csv", index_col = "Date", parse_dates = True)
        self.data_time_size = self.historical_data.shape[0]
        self.new_vizualization_open(5)
        self.refresh_company_info_labeles()
        
    def change_initial_vizualization(self):

        self.historical_data = pd.read_csv("E:/SZAKDOLGOZAT/A_DOLOGZAT/downloads/" + str(self.company_data[1]) + ".csv", index_col = "Date", parse_dates = True)

        self.data_time_size = self.historical_data.shape[0]
        self.new_vizualization_open(5)

    def change_vizualization(self, event, btn, period):
        if period > self.data_time_size:
            messagebox.showerror('Python Error', 'Error: Not enough data is loaded!')
            return

        if self.active_button != None:
            self.active_button.config(bg="SystemButtonFace")
        
        self.active_button = btn
        self.active_button.config(bg="sky blue")
   
        self.new_vizualization_open(period)

    def refresh_company_info_labeles(self):
        ticker = str(self.company_data[1])

        row = self.all_companies_info[self.all_companies_info['Ticker'] == ticker]
        
        self.sector_inf.config(text = row['Sector'].values[0], fg = 'blue')
        self.industry_inf.config(text = row['Industry'].values[0], fg = 'blue')
        #x = int(row['Market cap'].values[0])
        self.market_cap_inf.config(text = f"{int(row['Market cap'].values[0]):,}" + " $", fg = 'blue')
        self.country_inf.config(text = row['Country'].values[0], fg = 'blue')
    
    def new_vizualization_open(self, period):
        
        self.subplot.clear()
        time_period = self.historical_data[["Open"]].tail(period)
        time_period.index = pd.to_datetime(time_period.index, format = '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
        
        color, information = self.increased_or_decreased(float(time_period['Open'].head(1)), float(time_period['Open'].tail(1)))
        time_period.plot(use_index=True, y='Open', color = color, grid = True, ax=self.subplot)
        self.plots.draw()
        self.graph_info.config(text = self.company_data[1] + information, fg = color)

    def change_vizualization_custom(self, event, btn):

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

        time_period = self.historical_data[["Open"]][(self.historical_data.index >= np.datetime64(start)) & (self.historical_data.index <= np.datetime64(end))]
        if time_period.shape[0] == 0:
            messagebox.showerror('Python Error', 'Error: the selected period contains no data!')
            return
        
        if self.active_button != None:
            self.active_button.config(bg="SystemButtonFace")
        
        self.active_button = btn
        self.active_button.config(bg="sky blue")
        
        self.subplot.clear()

        time_period.index = pd.to_datetime(time_period.index, format = '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
            
        color, information = self.increased_or_decreased(time_period["Open"].head(1).values[0], time_period["Open"].tail(1).values[0])
        time_period.plot(use_index=True, y="Open", color = color, grid = True, ax=self.subplot)
        self.plots.draw()
        self.graph_info.config(text = self.company_data[1] + information, fg = color)

    def change_page_to_more_details(self, event):
        if self.active_button != None:
            self.active_button.config(bg="SystemButtonFace")
            
        self.page_manager.show_page("page03")

    def change_page_to_analize_01(self, event):
        if self.active_button != None:
            self.active_button.config(bg="SystemButtonFace")
            
        self.page_manager.show_page("page04")

    def change_page_to_analize_02(self, event):
        if self.active_button != None:
            self.active_button.config(bg="SystemButtonFace")
            
        self.page_manager.show_page("page05")
    
    def change_page_to_analize_03(self, event):
        if self.active_button != None:
            self.active_button.config(bg="SystemButtonFace")
            
        self.page_manager.show_page("page06")

    def change_page_to_analize_04(self, event):
        if self.active_button != None:
            self.active_button.config(bg="SystemButtonFace")
            
        self.page_manager.show_page("page07")

    def change_page_to_analize_05(self, event):
        if self.active_button != None:
            self.active_button.config(bg="SystemButtonFace")
            
        self.page_manager.show_page("page08")    

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
        self.exit.config(font=("Helvetica bold", int(self.x_font)))
        
        self.back.place(x=3*self.box_x, y=0, width=3*self.box_x, height=1*self.box_y)
        self.back.config(font=("Helvetica bold", int(self.x_font)))
                
                #_____Imput field for company search_____
        self.companies.place(x=12*self.box_x, y=0, width=11*self.box_x, height=1*self.box_y)
        self.companies.config(font=("Helvetica bold", int(self.x_font)))
        
        self.search.place(x=23*self.box_x, y=0, width=4*self.box_x, height=1*self.box_y)
        self.search.config(font=("Helvetica bold", int(self.x_font)))

                #_____Buttons for certain intervall visualization_____ 
        self.one_week.place(x=0, y=2*self.box_y, width=3*self.box_x, height=1*self.box_y)
        self.one_week.config(font=("Helvetica bold", int(self.x_font)))
        
        self.one_month.place(x=0, y=4*self.box_y, width=3*self.box_x, height=1*self.box_y)
        self.one_month.config(font=("Helvetica bold", int(self.x_font)))
        
        self.three_months.place(x=0, y=6*self.box_y, width=3*self.box_x, height=1*self.box_y)
        self.three_months.config(font=("Helvetica bold", int(self.x_font)))
        
        self.six_months.place(x=0, y=8*self.box_y, width=3*self.box_x, height=1*self.box_y)
        self.six_months.config(font=("Helvetica bold", int(self.x_font)))

        self.one_year.place(x=0, y=10*self.box_y, width=3*self.box_x, height=1*self.box_y)
        self.one_year.config(font=("Helvetica bold", int(self.x_font)))
        
        self.three_years.place(x=0, y=12*self.box_y, width=3*self.box_x, height=1*self.box_y)
        self.three_years.config(font=("Helvetica bold", int(self.x_font)))
        
        self.five_years.place(x=0, y=14*self.box_y, width=3*self.box_x, height=1*self.box_y)
        self.five_years.config(font=("Helvetica bold", int(self.x_font)))
        
        self.max_time.place(x=0, y=16*self.box_y, width=3*self.box_x, height=1*self.box_y)
        self.max_time.config(font=("Helvetica bold", int(self.x_font)))

                #_____Company info labels_____
        self.sector.place(x=30*self.box_x, y=2*self.box_y, width=5*self.box_x, height=1*self.box_y)
        self.sector.config(font=("Helvetica bold", int(self.x_font)))
        
        self.sector_inf.place(x=30*self.box_x, y=3*self.box_y, width=5*self.box_x, height=1*self.box_y)
        self.sector_inf.config(font=("Helvetica bold", int(self.x_font)))

        self.industry.place(x=30*self.box_x, y=4*self.box_y, width=5*self.box_x, height=1*self.box_y)
        self.industry.config(font=("Helvetica bold", int(self.x_font)))
        
        self.industry_inf.place(x=30*self.box_x, y=5*self.box_y, width=5*self.box_x, height=1*self.box_y)
        self.industry_inf.config(font=("Helvetica bold", int(self.x_font)))

        self.market_cap.place(x=30*self.box_x, y=6*self.box_y, width=5*self.box_x, height=1*self.box_y)
        self.market_cap.config(font=("Helvetica bold", int(self.x_font)))
        
        self.market_cap_inf.place(x=30*self.box_x, y=7*self.box_y, width=5*self.box_x, height=1*self.box_y)
        self.market_cap_inf.config(font=("Helvetica bold", int(self.x_font)))
        
        self.country.place(x=30*self.box_x, y=8*self.box_y, width=5*self.box_x, height=1*self.box_y)
        self.country.config(font=("Helvetica bold", int(self.x_font)))

        self.country_inf.place(x=30*self.box_x, y=9*self.box_y, width=5*self.box_x, height=1*self.box_y)
        self.country_inf.config(font=("Helvetica bold", int(self.x_font)))
        
                #_____Buttons for page change_____
        self.more_details.place(x=self.x_len-5*self.box_x, y=15*self.box_y, width=5*self.box_x, height=1*self.box_y)
        self.more_details.config(font=("Helvetica bold", int(self.x_font)))
        
        self.analize_01.place(x=6*self.box_x, y=17*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.analize_01.config(font=("Helvetica bold", int(self.x_font)))
        
        self.analize_02.place(x=11*self.box_x, y=17*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.analize_02.config(font=("Helvetica bold", int(self.x_font)))
        
        self.analize_03.place(x=16*self.box_x, y=17*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.analize_03.config(font=("Helvetica bold", int(self.x_font)))
        
        self.analize_04.place(x=21*self.box_x, y=17*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.analize_04.config(font=("Helvetica bold", int(self.x_font)))
        
        self.analize_05.place(x=26*self.box_x, y=17*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.analize_05.config(font=("Helvetica bold", int(self.x_font)))

                #_____Graph abouth the data_____
        self.subplot.tick_params(axis='x', labelsize = self.x_font)
        self.subplot.tick_params(axis='y', labelsize = self.y_font)
        self.plots.get_tk_widget().place(x=3*self.box_x, y=2*self.box_y, width=27*self.box_x, height=14*self.box_y)

                #_____Label for information of the graph_____
        self.graph_info.place(x=3*self.box_x, y=16*self.box_y, width=27*self.box_x, height=1*self.box_y)
        self.graph_info.config(font=("Helvetica bold", int(self.x_font)))

                #____Date input for specific time period_____
        self.date_from.place(x=6*self.box_x, y=1*self.box_y, width=2*self.box_x, height=1*self.box_y)
        self.date_from.config(font=("Helvetica bold", int(self.x_font)))
        
        self.date_start.place(x=8*self.box_x, y=1*self.box_y, width=5*self.box_x, height=1*self.box_y)
        self.date_start.config(font=("Helvetica bold", int(self.x_font)))

        self.date_to.place(x=13*self.box_x, y=1*self.box_y, width=2*self.box_x, height=1*self.box_y)
        self.date_to.config(font=("Helvetica bold", int(self.x_font)))
        
        self.date_end.place(x=15*self.box_x, y=1*self.box_y, width=5*self.box_x, height=1*self.box_y)
        self.date_end.config(font=("Helvetica bold", int(self.x_font)))

        self.show_open.place(x=21*self.box_x, y=1*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.show_open.config(font=("Helvetica bold", int(self.x_font)))


        
