from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from tkcalendar import DateEntry

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import numpy as np

from math import atan 

import pandas as pd

from datetime import datetime
from dateutil.relativedelta import relativedelta
import time

import Page

class xPage05(Page.Page):
    def __init__(self, root, page_manager):
        Page.Page.__init__(self, root, page_manager)

               #_____Control buttons_____
        self.exit = Button(self, text="EXIT")
        self.exit.bind('<Button-1>', self.go_exit)

        self.back = Button(self, text="BACK", command = lambda: self.go_back(self, 'page02'))
                
                #_____Imput field for company search_____
        self.companies = ttk.Combobox(self)
        data = pd.read_csv("E:/SZAKDOLGOZAT/A_DOLOGZAT/system/BootFile.csv")
        self.companies_name = list(data['Name'].values)
        self.companies_name_symbol = self.create_name_symbol_vector(data['Name'].values, data['Symbol'].values)
        self.companies['values'] = self.companies_name
        self.companies.bind('<KeyRelease>', self.check_companies)

        self.search = Button(self, text="Search")
        self.search.bind('<Button-1>', self.search_companies)

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

            #_____SMA signal info labels_____
        self.sma13 = Label(self, text="SMA13", anchor="center")
        self.sma13_inf_01 = Label(self, text="", anchor="center")
        self.sma13_inf_02 = Label(self, text="", anchor="center")

        self.sma50 = Label(self, text="SMA50", anchor="center")
        self.sma50_inf_01 = Label(self, text="", anchor="center")
        self.sma50_inf_02 = Label(self, text="", anchor="center")

        self.sma200 = Label(self, text="SMA200", anchor="center")
        self.sma200_inf_01 = Label(self, text="", anchor="center")
        self.sma200_inf_02 = Label(self, text="", anchor="center")

        self.change_sma13 = Label(self, text="Change: ", anchor="center")
        self.trend_sma13 = Label(self, text="Trend: ", anchor="center")

        self.change_sma50 = Label(self, text="Change: ", anchor="center")
        self.trend_sma50 = Label(self, text="Trend: ", anchor="center")
        
        self.change_sma200 = Label(self, text="Change: ", anchor="center")
        self.trend_sma200 = Label(self, text="Trend: ", anchor="center")

        
                #_____Graph abouth the data_____
        self.figure = Figure(figsize=(4, 7), dpi=100)
        
        self.subplot = self.figure.add_subplot(111)

        self.figure.subplots_adjust(left=0.08, right=0.985, bottom=0.08, top=0.985)
        
        self.plots = FigureCanvasTkAgg(self.figure, self)

                #_____Label for information of the graph_____
        self.graph_info = Label(self, text="", anchor="center")
        
                #____Date input for specific time period_____
        self.date_from = Label(self, text="From:", anchor="center")
        self.date_start = DateEntry(self, popanchor="n", date_pattern='YYYY-MM-DD')
    
        self.date_to = Label(self, text="To:", anchor="center")
        self.date_end = DateEntry(self, calendar_position='above', date_pattern='YYYY-MM-DD')

        self.show_open = Button(self, text="Show", anchor="center")
        self.show_open.configure(command = lambda btn=self.show_open: self.change_vizualization_custom(self, btn))

    def show_widgets(self):
        self.root.bind("<Configure>", self.resize_window)
        self.companies.set(self.company_data[0])
        
        self.active_button = self.one_week
        self.active_button.config(bg="sky blue")
        self.resize_window(None)

        self.change_initial_vizualization()
                    
    def search_companies(self, event):
        company_name = str(self.companies.get())
        self.check_input_company(company_name)

        if self.company_data[0] == "ERROR" or self.company_data[0] == "":
            messagebox.showerror('Python Error', 'Error: No such company in the data base!')
            return

        if self.active_button != None:
            self.active_button.config(bg="SystemButtonFace")
        
        self.active_button = self.one_week
        self.active_button.config(bg="sky blue")
        self.historical_data = pd.read_csv("E:/SZAKDOLGOZAT/A_DOLOGZAT/downloads/" + str(self.company_data[1]) + ".csv", index_col = "Date", parse_dates = True)
        self.data_time_size = self.historical_data.shape[0]
        self.new_vizualization(5)

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

        self.data_time_size = self.historical_data.shape[0]
        self.new_vizualization(5)

    def change_vizualization(self, event, btn, period):
        if period > self.data_time_size:
            messagebox.showerror('Python Error', 'Error: Not enough data is loaded!')
            return

        if self.active_button != None:
            self.active_button.config(bg="SystemButtonFace")
        
        self.active_button = btn
        self.active_button.config(bg="sky blue")
   
        self.new_vizualization(period)
        
    def sma_information(self, data):
        n = data.shape[0]
        
        change_sma13, color_sma13 = self.calc_percent_change(data["SMA13"].head(1).values[0], data["SMA13"].tail(1).values[0])
        change_sma50, color_sma50 = self.calc_percent_change(data["SMA50"].head(1).values[0], data["SMA50"].tail(1).values[0])
        change_sma200, color_sma200 = self.calc_percent_change(data["SMA200"].head(1).values[0], data["SMA200"].tail(1).values[0])

        model_sma13 = np.poly1d(np.polyfit(np.linspace(0,n-1,n), data['SMA13'], 1))
        model_sma50 = np.poly1d(np.polyfit(np.linspace(0,n-1,n), data['SMA50'], 1))
        model_sma200 = np.poly1d(np.polyfit(np.linspace(0,n-1,n), data['SMA200'], 1))

        s_sma13 = model_sma13(0)
        f_sma13 = model_sma13(n-1)

        s_sma50 = model_sma50(0)
        f_sma50 = model_sma50(n-1)

        s_sma200 = model_sma200(0)
        f_sma200 = model_sma200(n-1)

        sig_13 = ''
        if change_sma13 > 0:
            sig_13 = '+'

        sig_50 = ''
        if change_sma50 > 0:
            sig_50 = '+'
            
        sig_200 = ''
        if change_sma200 > 0:
            sig_200 = '+'
            

        self.sma13_inf_01.config(text = sig_13 + str(change_sma13) + '%', fg = color_sma13)
        self.sma50_inf_01.config(text = sig_50 +str(change_sma50) + '%', fg = color_sma50)
        self.sma200_inf_01.config(text = sig_200 +str(change_sma200) + '%', fg = color_sma200)

        slope_sma13 = round(atan((f_sma13 - s_sma13)/n),3)
        slope_sma50 = round(atan((f_sma50 - s_sma50)/n),3)
        slope_sma200 = round(atan((f_sma200 - s_sma200)/n),3)

        self.sma13_inf_02.config(text = sig_13 + str(slope_sma13) + ' rad', fg = color_sma13)
        self.sma50_inf_02.config(text = sig_50 + str(slope_sma50) + ' rad', fg = color_sma50)
        self.sma200_inf_02.config(text = sig_200 + str(slope_sma200) + ' rad', fg = color_sma200)

    def new_vizualization(self, period):
        
        self.subplot.clear()
        time_period = self.historical_data[['Open', 'SMA13', 'SMA50', 'SMA200']].tail(period)
        time_period.index = pd.to_datetime(time_period.index, format = '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
        
        color, information = self.increased_or_decreased(time_period['Open'].head(1).values[0], time_period['Open'].tail(1).values[0])
        time_period.plot(use_index=True, y=['Open','SMA13', 'SMA50', 'SMA200'], color = [color, "yellow", "blue", "magenta"], grid = True, ax=self.subplot)
        self.plots.draw()
        
        self.graph_info.config(text = self.company_data[1] + information, fg = color)

        self.sma_information(time_period)
        
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

        time_period = self.historical_data[['Open', 'SMA13', 'SMA50', 'SMA200']][(self.historical_data.index >= np.datetime64(start)) & (self.historical_data.index <= np.datetime64(end))]
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
        time_period.plot(use_index=True, y=['Open','SMA13', 'SMA50', 'SMA200'], color = [color, "yellow", "blue", "magenta"], grid = True, ax=self.subplot)
        self.plots.draw()
        
        self.graph_info.config(text = self.company_data[1] + information, fg = color)

        self.sma_information(time_period)

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
        self.sma13.place(x=self.x_len-2*self.box_x, y=2*self.box_y, width=2*self.box_x, height=1*self.box_y)
        self.sma13.config(font=("Helvetica bold", int(self.x_font)))
        
        self.sma13_inf_01.place(x=self.x_len-2*self.box_x, y=3*self.box_y, width=2*self.box_x, height=1*self.box_y)
        self.sma13_inf_01.config(font=("Helvetica bold", int(self.x_font)))
        
        self.sma13_inf_02.place(x=self.x_len-2*self.box_x, y=4*self.box_y, width=2*self.box_x, height=1*self.box_y)
        self.sma13_inf_02.config(font=("Helvetica bold", int(self.x_font)))

        self.sma50.place(x=self.x_len-2*self.box_x, y=5*self.box_y, width=2*self.box_x, height=1*self.box_y)
        self.sma50.config(font=("Helvetica bold", int(self.x_font)))
        
        self.sma50_inf_01.place(x=self.x_len-2*self.box_x, y=6*self.box_y, width=2*self.box_x, height=1*self.box_y)
        self.sma50_inf_01.config(font=("Helvetica bold", int(self.x_font)))
        
        self.sma50_inf_02.place(x=self.x_len-2*self.box_x, y=7*self.box_y, width=2*self.box_x, height=1*self.box_y)
        self.sma50_inf_02.config(font=("Helvetica bold", int(self.x_font)))

        self.sma200.place(x=self.x_len-2*self.box_x, y=8*self.box_y, width=2*self.box_x, height=1*self.box_y)
        self.sma200.config(font=("Helvetica bold", int(self.x_font)))
        
        self.sma200_inf_01.place(x=self.x_len-2*self.box_x, y=9*self.box_y, width=2*self.box_x, height=1*self.box_y)
        self.sma200_inf_01.config(font=("Helvetica bold", int(self.x_font)))
        
        self.sma200_inf_02.place(x=self.x_len-2*self.box_x, y=10*self.box_y, width=2*self.box_x, height=1*self.box_y)
        self.sma200_inf_02.config(font=("Helvetica bold", int(self.x_font)))

        self.change_sma13.place(x=self.x_len-4*self.box_x, y=3*self.box_y, width=2*self.box_x, height=1*self.box_y)
        self.change_sma13.config(font=("Helvetica bold", int(self.x_font)))
        self.trend_sma13.place(x=self.x_len-4*self.box_x, y=4*self.box_y, width=2*self.box_x, height=1*self.box_y)
        self.trend_sma13.config(font=("Helvetica bold", int(self.x_font)))

        self.change_sma50.place(x=self.x_len-4*self.box_x, y=6*self.box_y, width=2*self.box_x, height=1*self.box_y)
        self.change_sma50.config(font=("Helvetica bold", int(self.x_font)))
        self.trend_sma50.place(x=self.x_len-4*self.box_x, y=7*self.box_y, width=2*self.box_x, height=1*self.box_y)
        self.trend_sma50.config(font=("Helvetica bold", int(self.x_font)))

        self.change_sma200.place(x=self.x_len-4*self.box_x, y=9*self.box_y, width=2*self.box_x, height=1*self.box_y)
        self.change_sma200.config(font=("Helvetica bold", int(self.x_font)))
        self.trend_sma200.place(x=self.x_len-4*self.box_x, y=10*self.box_y, width=2*self.box_x, height=1*self.box_y)
        self.trend_sma200.config(font=("Helvetica bold", int(self.x_font)))


                #_____Graph abouth the data_____
        self.subplot.tick_params(axis='x', labelsize = self.x_font)
        self.subplot.tick_params(axis='y', labelsize = self.y_font)
        self.plots.get_tk_widget().place(x=3*self.box_x, y=2*self.box_y, width=28*self.box_x, height=15*self.box_y)

                #_____Label for information of the graph_____
        self.graph_info.place(x=3*self.box_x, y=17*self.box_y, width=28*self.box_x, height=1*self.box_y)
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
    























        
