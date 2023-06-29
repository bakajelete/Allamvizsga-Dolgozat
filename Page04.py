from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from tkcalendar import DateEntry

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib
import matplotlib.pyplot as plt

import numpy as np

import pandas as pd

import yfinance as yf

from datetime import datetime
from dateutil.relativedelta import relativedelta
import time

from data import *

import Page

class xPage04(Page.Page):
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
        self.one_week_B50 = Button(self, text="One week B50", command = lambda: self.change_vizualization_50(self, 5))
        self.one_week_B200 = Button(self, text="One week B200", command = lambda: self.change_vizualization_200(self, 5))
        
        self.one_month_B50 = Button(self, text="One month B50", command = lambda: self.change_vizualization_50(self, self.get_days_nr(self.now - relativedelta(months=1))))
        self.one_month_B200 = Button(self, text="One month B200", command = lambda: self.change_vizualization_200(self, self.get_days_nr(self.now - relativedelta(months=1))))
        
        self.three_monts_B50 = Button(self, text="Three monts B50", command = lambda: self.change_vizualization_50(self, self.get_days_nr(self.now - relativedelta(months=3))))
        self.three_monts_B200 = Button(self, text="Three monts B200", command = lambda: self.change_vizualization_200(self, self.get_days_nr(self.now - relativedelta(months=3))))
        
        self.six_monts_B50 = Button(self, text="Six monts B50", command = lambda: self.change_vizualization_50(self, self.get_days_nr(self.now - relativedelta(months=6))))
        self.six_monts_B200 = Button(self, text="Six monts B200", command = lambda: self.change_vizualization_200(self, self.get_days_nr(self.now - relativedelta(months=6))))
        
        self.one_year_B50 = Button(self, text="One year B50", command = lambda: self.change_vizualization_50(self, self.get_days_nr(self.now - relativedelta(years=1))))
        self.one_year_B200 = Button(self, text="One year B200", command = lambda: self.change_vizualization_200(self, self.get_days_nr(self.now - relativedelta(years=1))))
        
        self.three_years_B50 = Button(self, text="Three years B50", command = lambda: self.change_vizualization_50(self, self.get_days_nr(self.now - relativedelta(years=3))))
        self.three_years_B200 = Button(self, text="Three years B200", command = lambda: self.change_vizualization_200(self, self.get_days_nr(self.now - relativedelta(years=3))))
        
        self.five_years_B50 = Button(self, text="Five years B50", command = lambda: self.change_vizualization_50(self, self.get_days_nr(self.now - relativedelta(years=5))))
        self.five_years_B200 = Button(self, text="Five years B200", command = lambda: self.change_vizualization_200(self, self.get_days_nr(self.now - relativedelta(years=5))))
        
        self.max_time_B50 = Button(self, text="Max time B50", command = lambda: self.change_vizualization_50(self, self.data_time_size))
        self.max_time_B200 = Button(self, text="Max time B200", command = lambda: self.change_vizualization_200(self, self.data_time_size))
        
                #_____Graph abouth the data_____
        self.figure = Figure(figsize=(4, 7), dpi=100)
        
        self.subplot = self.figure.add_subplot(111)

        self.figure.subplots_adjust(left=0.08, right=0.985, bottom=0.08, top=0.985)
        
        self.plots = FigureCanvasTkAgg(self.figure, self)
        
                #_____Label for information of the graph_____
        self.graph_info = Label(self, text="")

                #____Date input for specific time period_____
        self.date_from = Label(self, text="From:")
        self.date_start = DateEntry(self, width= 16, date_pattern='YYYY-MM-DD', background= "magenta3", foreground= "white",bd=2)

        self.date_to = Label(self, text="To:")
        self.date_end = DateEntry(self, width = 16, date_pattern='YYYY-MM-DD', background= "magenta3", foreground= "white",bd=2)

        self.show_B50 = Button(self, text="Show B50")
        self.show_B50.bind('<Button-1>', self.change_vizualization_custom_B50)
        
        self.show_B200 = Button(self, text="Show B200")
        self.show_B200.bind('<Button-1>', self.change_vizualization_custom_B200)

    def show_widgets(self):
        self.root.bind("<Configure>", self.resize_window)
        self.companies.set(self.company_data[0])
        self.resize_window(None)
        self.change_initial_vizualization()
    
    def go_back(self, event):
        self.page_manager.show_page("page02")
        
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
        
    def change_initial_vizualization(self):
        self.historical_data = pd.read_csv("E:/SZAKDOLGOZAT/A_DOLOGZAT/downloads/" + str(self.company_data[1]) + ".csv", index_col = "Date", parse_dates = True)
        self.data_time_size = self.historical_data.shape[0]
        
        self.new_vizualization_50(5)

    def search_companies(self, event):
        company_name = str(self.companies.get())

        self.ticker = self.searh_for_ticker(company_name)

        if self.company_data[0] == "ERROR":
            messagebox.showerror('Python Error', 'Error: No such company in the data base!')
            return
        
        self.historical_data = pd.read_csv("E:/SZAKDOLGOZAT/A_DOLOGZAT/downloads/" + str(self.company_data[1]) + ".csv", index_col = "Date", parse_dates = True)
        self.data_time_size = self.historical_data.shape[0]

        self.new_vizualization_50(5)

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

    def change_vizualization_50(self, event, period):
        if period > self.data_time_size:
            messagebox.showerror('Python Error', 'Error: Not enough data is loaded!')
            return
        
        self.new_vizualization_50(period)

    def change_vizualization_200(self, event, period):
        if period > self.data_time_size:
            messagebox.showerror('Python Error', 'Error: Not enough data is loaded!')
            return
        
        self.new_vizualization_200(period)
        
    def new_vizualization_50(self, period):
        
        self.subplot.clear()
        time_period = self.historical_data[["Open", "SMA50"]].tail(period)
        time_period.index = pd.to_datetime(time_period.index, format = '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
        
        std = time_period[['Open']].std()
        time_period['STD_up2'] = time_period.apply(lambda x: x['SMA50'] + 2 * std, axis=1)
        time_period['STD_up1'] = time_period.apply(lambda x: x['SMA50'] + std, axis=1)
        time_period['STD_lo1'] = time_period.apply(lambda x: x['SMA50'] - std, axis=1)
        time_period['STD_lo2'] = time_period.apply(lambda x: x['SMA50'] - 2 * std, axis=1)

        time_period['STD_lo1'] = time_period['STD_lo1'].apply(lambda x: x if x > 0 else 0)
        time_period['STD_lo2'] = time_period['STD_lo2'].apply(lambda x: x if x > 0 else 0)
        
        
        color, information = self.increased_or_decreased(float(time_period["Open"].head(1)), float(time_period["Open"].tail(1)))
        colors = [color] + ["blue", "greenyellow", "limegreen", "orangered", "maroon"]
        time_period.plot(use_index=True, y=["Open", "SMA50","STD_up2", "STD_up1", "STD_lo1", "STD_lo2"], color = colors, grid = True, ax=self.subplot)
        self.plots.draw()
        self.graph_info.config(text = self.company_data[1] + information, fg = color)

    def new_vizualization_200(self, period):
        
        self.subplot.clear()
        time_period = self.historical_data[["Open", "SMA200"]].tail(period)
        time_period.index = pd.to_datetime(time_period.index, format = '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
        
        std = time_period[['Open']].std()
        time_period['STD_up2'] = time_period.apply(lambda x: x['SMA200'] + 2 * std, axis=1)
        time_period['STD_up1'] = time_period.apply(lambda x: x['SMA200'] + std, axis=1)
        time_period['STD_lo1'] = time_period.apply(lambda x: x['SMA200'] - std, axis=1)
        time_period['STD_lo2'] = time_period.apply(lambda x: x['SMA200'] - 2 * std, axis=1)

        time_period['STD_lo1'] = time_period['STD_lo1'].apply(lambda x: x if x > 0 else 0)
        time_period['STD_lo2'] = time_period['STD_lo2'].apply(lambda x: x if x > 0 else 0)

        color, information = self.increased_or_decreased(float(time_period["Open"].head(1)), float(time_period["Open"].tail(1)))
        colors = [color] + ["blue", "greenyellow", "limegreen", "orangered", "maroon"]
        time_period.plot(use_index=True, y=["Open", "SMA200", "STD_up2", "STD_up1", "STD_lo1", "STD_lo2"], color = colors, grid = True, ax=self.subplot)
        self.plots.draw()
        self.graph_info.config(text = self.company_data[1] + information, fg = color)

    def change_vizualization_custom_B50(self, event):
        start = self.date_start.get_date()
        end = self.date_end.get_date()

        if start > end:
            messagebox.showerror('Python Error', 'Error: the given dates are incorrect!')
            return

        if end > self.now:
            messagebox.showerror('Python Error', 'Error: the given dates are incorrect!')
            return

        self.subplot.clear()
        custom_period = self.historical_data[["Open", "SMA50"]][(self.historical_data.index >= np.datetime64(start)) & (self.historical_data.index <= np.datetime64(end))]
        custom_period.index = pd.to_datetime(custom_period.index, format = '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
        
        std = custom_period[['Open']].std()
        custom_period['STD_up2'] = custom_period.apply(lambda x: x['SMA50'] + 2 * std, axis=1)
        custom_period['STD_up1'] = custom_period.apply(lambda x: x['SMA50'] + std, axis=1)
        time_period['STD_lo1'] = time_period.apply(lambda x: x['SMA50'] - std, axis=1)
        time_period['STD_lo2'] = time_period.apply(lambda x: x['SMA50'] - 2 * std, axis=1)

        time_period['STD_lo1'] = time_period['STD_lo1'].apply(lambda x: x if x > 0 else 0)
        time_period['STD_lo2'] = time_period['STD_lo2'].apply(lambda x: x if x > 0 else 0)
        
        color, information = self.increased_or_decreased(float(custom_period["Open"].head(1)), float(custom_period["Open"].tail(1)))
        colors = [color] + ["blue", "greenyellow", "limegreen", "orangered", "maroon"]
        custom_period.plot(use_index=True, y=["Open", "SMA50","STD_up2", "STD_up1", "STD_lo1", "STD_lo2"], color = colors, grid = True, ax=self.subplot)
        self.plots.draw()
        self.graph_info.config(text = self.company_data[1] + information, fg = color)

    def change_vizualization_custom_B200(self, event):
        start = self.date_start.get_date()
        end = self.date_end.get_date()

        if start > end:
            messagebox.showerror('Python Error', 'Error: the given dates are incorrect!')
            return

        if end > self.now:
            messagebox.showerror('Python Error', 'Error: the given dates are incorrect!')
            return

        self.subplot.clear()
        custom_period = self.historical_data[["Open", "SMA200"]][(self.historical_data.index >= np.datetime64(start)) & (self.historical_data.index <= np.datetime64(end))]
        custom_period.index = pd.to_datetime(custom_period.index, format = '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
        
        std = custom_period[['Open']].std()
        custom_period['STD_up2'] = custom_period.apply(lambda x: x['SMA200'] + 2 * std, axis=1)
        custom_period['STD_up1'] = custom_period.apply(lambda x: x['SMA200'] + std, axis=1)
        time_period['STD_lo1'] = time_period.apply(lambda x: x['SMA200'] - std, axis=1)
        time_period['STD_lo2'] = time_period.apply(lambda x: x['SMA200'] - 2 * std, axis=1)

        time_period['STD_lo1'] = time_period['STD_lo1'].apply(lambda x: x if x > 0 else 0)
        time_period['STD_lo2'] = time_period['STD_lo2'].apply(lambda x: x if x > 0 else 0)
        

        color, information = self.increased_or_decreased(float(custom_period["Open"].head(1)), float(custom_period["Open"].tail(1)))
        colors = [color] + ["blue", "greenyellow", "limegreen", "orangered", "maroon"]
        custom_period.plot(use_index=True, y=["Open", "SMA200", "STD_up2", "STD_up1", "STD_lo1", "STD_lo2"], color = colors, grid = True, ax=self.subplot)
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
        self.one_week_B50.place(x=0*self.box_x, y=2*self.box_y, width=5*self.box_x, height=1*self.box_y)
        self.one_week_B200.place(x=0*self.box_x, y=3*self.box_y, width=5*self.box_x, height=1*self.box_y)
        
        self.one_month_B50.place(x=0*self.box_x, y=4*self.box_y, width=5*self.box_x, height=1*self.box_y)
        self.one_month_B200.place(x=0*self.box_x, y=5*self.box_y, width=5*self.box_x, height=1*self.box_y)
        
        self.three_monts_B50.place(x=0*self.box_x, y=6*self.box_y, width=5*self.box_x, height=1*self.box_y)
        self.three_monts_B200.place(x=0*self.box_x, y=7*self.box_y, width=5*self.box_x, height=1*self.box_y)

        self.six_monts_B50.place(x=0*self.box_x, y=8*self.box_y, width=5*self.box_x, height=1*self.box_y)
        self.six_monts_B200.place(x=0*self.box_x, y=9*self.box_y, width=5*self.box_x, height=1*self.box_y)

        self.one_year_B50.place(x=0*self.box_x, y=10*self.box_y, width=5*self.box_x, height=1*self.box_y)
        self.one_year_B200.place(x=0*self.box_x, y=11*self.box_y, width=5*self.box_x, height=1*self.box_y)

        self.three_years_B50.place(x=0*self.box_x, y=12*self.box_y, width=5*self.box_x, height=1*self.box_y)
        self.three_years_B200.place(x=0*self.box_x, y=13*self.box_y, width=5*self.box_x, height=1*self.box_y)

        self.five_years_B50.place(x=0*self.box_x, y=14*self.box_y, width=5*self.box_x, height=1*self.box_y)
        self.five_years_B200.place(x=0*self.box_x, y=15*self.box_y, width=5*self.box_x, height=1*self.box_y)

        self.max_time_B50.place(x=0*self.box_x, y=16*self.box_y, width=5*self.box_x, height=1*self.box_y)
        self.max_time_B200.place(x=0*self.box_x, y=17*self.box_y, width=5*self.box_x, height=1*self.box_y)

            #_____Graph abouth the data_____
        self.subplot.tick_params(axis='x', labelsize = self.x_font)
        self.subplot.tick_params(axis='y', labelsize = self.y_font)
        self.plots.get_tk_widget().place(x=5*self.box_x, y=2*self.box_y, width=24*self.box_x, height=15*self.box_y)

        
                #_____Label for information of the graph_____
        self.graph_info.place(x=9*self.box_x, y=17*self.box_y, width=17*self.box_x, height=1*self.box_y)

                #____Date input for specific time period_____
        self.date_from.place(x=6*self.box_x, y=1*self.box_y, width=2*self.box_x, height=1*self.box_y)
        self.date_start.place(x=8*self.box_x, y=1*self.box_y, width=5*self.box_x, height=1*self.box_y)

        self.date_to.place(x=13*self.box_x, y=1*self.box_y, width=2*self.box_x, height=1*self.box_y)
        self.date_end.place(x=15*self.box_x, y=1*self.box_y, width=5*self.box_x, height=1*self.box_y)

        self.show_B50.place(x=20*self.box_x, y=1*self.box_y, width=3*self.box_x, height=1*self.box_y)
        self.show_B200.place(x=23*self.box_x, y=1*self.box_y, width=3*self.box_x, height=1*self.box_y)


def page():    
    root = Tk()
    #root.geometry("770x396")
    Page4(root)
    root.mainloop()

if __name__ == '__main__':
    page()
