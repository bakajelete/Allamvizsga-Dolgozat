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

import xPage1
import xPage2

class Page3:
    
    def __init__(self, root):
        
        
        self.root = root
        self.root.geometry("770x396")

        self.width = 770
        self.height = 396
        self.box_x = 22
        self.box_y = 22
        self.ticker = ''
        self.historical_data = []
        self.max_time = 0

        self.now = datetime.today().date()
        
                #_____Control buttons_____
        self.exit = Button(root, text="EXIT")
        self.exit.bind('<Button-1>', self.go_exit)
        self.exit.place(x=0*self.box_x, y=0, width=3*self.box_x, height=1*self.box_y)

        self.back = Button(root, text="BACK")
        self.back.bind('<Button-1>', self.go_back)
        self.back.place(x=3*self.box_x, y=0, width=3*self.box_x, height=1*self.box_y)
        
                #_____Imput field for company search_____
        self.companies = ttk.Combobox(root)
        self.companies.set(company_data[0])
        self.companies['values'] = companies_name
        self.companies.bind('<KeyRelease>', self.check_companies)
        self.companies.place(x=12*self.box_x, y=0, width=11*self.box_x, height=1*self.box_y)

        self.search = Button(root, text="Search")
        self.search.bind('<Button-1>', self.search_companies)
        self.search.place(x=23*self.box_x, y=0, width=4*self.box_x, height=1*self.box_y)

                #_____Buttons for certain intervall visualization_____
        self.one_week = Button(root, text="One week", command = lambda: self.change_vizualization(self, 5))
        self.one_week.place(x=0, y=2*self.box_y, width=6*self.box_x, height=1*self.box_y)
        self.one_week_changes = Button(root, text="One week changes", command = lambda: self.change_vizualization_changes(self, 5))
        self.one_week_changes.place(x=0, y=3*self.box_y, width=6*self.box_x, height=1*self.box_y)
        
        self.one_month = Button(root, text="One month", command = lambda: self.change_vizualization(self, self.get_days_nr(self.now - relativedelta(months=1))))
        self.one_month.place(x=0, y=4*self.box_y, width=6*self.box_x, height=1*self.box_y)
        self.one_month = Button(root, text="One month changes", command = lambda: self.change_vizualization_changes(self, self.get_days_nr(self.now - relativedelta(months=1))))
        self.one_month.place(x=0, y=5*self.box_y, width=6*self.box_x, height=1*self.box_y)

        self.three_months = Button(root, text="Three months", command = lambda: self.change_vizualization(self, self.get_days_nr(self.now - relativedelta(months=3))))
        self.three_months.place(x=0, y=6*self.box_y, width=6*self.box_x, height=1*self.box_y)
        self.three_months = Button(root, text="Three months changes", command = lambda: self.change_vizualization_changes(self, self.get_days_nr(self.now - relativedelta(months=3))))
        self.three_months.place(x=0, y=7*self.box_y, width=6*self.box_x, height=1*self.box_y)
        
        self.six_months = Button(root, text="Six months", command = lambda: self.change_vizualization(self, self.get_days_nr(self.now - relativedelta(months=6))))
        self.six_months.place(x=0, y=8*self.box_y, width=6*self.box_x, height=1*self.box_y)
        self.six_months = Button(root, text="Six months changes", command = lambda: self.change_vizualization_changes(self, self.get_days_nr(self.now - relativedelta(months=6))))
        self.six_months.place(x=0, y=9*self.box_y, width=6*self.box_x, height=1*self.box_y)
        
        self.one_year = Button(root, text="One year", command = lambda: self.change_vizualization(self, self.get_days_nr(self.now - relativedelta(years=1))))
        self.one_year.place(x=0, y=10*self.box_y, width=6*self.box_x, height=1*self.box_y)   
        self.one_year = Button(root, text="One year changes", command = lambda: self.change_vizualization_changes(self, self.get_days_nr(self.now - relativedelta(years=1))))
        self.one_year.place(x=0, y=11*self.box_y, width=6*self.box_x, height=1*self.box_y)

        self.three_years = Button(root, text="Three years", command = lambda: self.change_vizualization(self, self.get_days_nr(self.now - relativedelta(years=3))))
        self.three_years.place(x=0, y=12*self.box_y, width=6*self.box_x, height=1*self.box_y)
        self.five_years = Button(root, text="Three years changes", command = lambda: self.change_vizualization_changes(self, self.get_days_nr(self.now - relativedelta(years=3))))
        self.five_years.place(x=0, y=13*self.box_y, width=6*self.box_x, height=1*self.box_y)
        
        self.five_years = Button(root, text="Five years", command = lambda: self.change_vizualization(self, self.get_days_nr(self.now - relativedelta(years=5))))
        self.five_years.place(x=0, y=14*self.box_y, width=6*self.box_x, height=1*self.box_y)        
        self.five_years = Button(root, text="Five years  changes", command = lambda: self.change_vizualization_changes(self, self.get_days_nr(self.now - relativedelta(years=5))))
        self.five_years.place(x=0, y=15*self.box_y, width=6*self.box_x, height=1*self.box_y)

        self.max = Button(root, text="Max time", command = lambda: self.change_vizualization(self, self.max_time))
        self.max.place(x=0, y=16*self.box_y, width=6*self.box_x, height=1*self.box_y)
        self.max = Button(root, text="Max time  changes", command = lambda: self.change_vizualization_changes(self, self.max_time))
        self.max.place(x=0, y=17*self.box_y, width=6*self.box_x, height=1*self.box_y)
        

                #_____Graph abouth the data_____
        self.figure = Figure(figsize=(4.5, 6), dpi=100)
        
        self.subplot = self.figure.add_subplot(111)
        self.subplot.set_ylabel('Value($)', fontsize=6)
        self.subplot.set_xlabel('Time(day)', fontsize=6)
        self.subplot.set_xlim(0, 10)
        self.subplot.set_ylim(0, 10)
        self.subplot.tick_params(axis='x', labelsize=5)
        
        self.plots = FigureCanvasTkAgg(self.figure, root)
        self.plots.get_tk_widget().place(x=6*self.box_x, y=2*self.box_y, width=22*self.box_x, height=13*self.box_y)

                #_____Label for information of the graph_____
        self.graph_info = Label(root, text="", anchor="center")
        self.graph_info.place(x=9*self.box_x, y=1*self.box_y, width=17*self.box_x, height=1*self.box_y)

                #____Date input for specific time period_____
        self.date_from = Label(root, text="From:", anchor="center")
        self.date_from.place(x=7*self.box_x, y=17*self.box_y, width=2*self.box_x, height=1*self.box_y)
        self.date_start = DateEntry(root, width= 16, date_pattern='YYYY-MM-DD', background= "magenta3", foreground= "white",bd=2)
        self.date_start.place(x=9*self.box_x, y=17*self.box_y, width=5*self.box_x, height=1*self.box_y)

        self.date_to = Label(root, text="To:", anchor="center")
        self.date_to.place(x=15*self.box_x, y=17*self.box_y, width=2*self.box_x, height=1*self.box_y)
        self.date_end = DateEntry(root, width = 16, date_pattern='YYYY-MM-DD', background= "magenta3", foreground= "white",bd=2)
        self.date_end.place(x=17*self.box_x, y=17*self.box_y, width=5*self.box_x, height=1*self.box_y)

        self.show = Button(root, text="Show")
        self.show.bind('<Button-1>', self.change_vizualization_custom)
        self.show.place(x=22*self.box_x, y=17*self.box_y, width=4*self.box_x, height=1*self.box_y)

        self.show_change = Button(root, text="Show changes")
        self.show_change.bind('<Button-1>', self.change_vizualization_custom_changes)
        self.show_change.place(x=26*self.box_x, y=17*self.box_y, width=4*self.box_x, height=1*self.box_y)
        
        self.change_initial_vizualization()

    def go_exit(self, event):
        self.root.destroy()
    
    def go_back(self, event):
        win = Toplevel()
        self.root.withdraw()
        xPage2.Page2(win)
        win.deiconify()
        
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
                company_data[0] = companie[0]
                company_data[1] = companie[1]
                break

        if ok:
            company_data[0] = "ERROR"
        
            
    def search_companies(self, event):
        company_name = str(self.companies.get())

        self.ticker = self.searh_for_ticker(company_name)

        if company_data[0] == "ERROR":
            messagebox.showerror('Python Error', 'Error: No such company in the data base!')
            return
        
        self.historical_data = pd.read_csv("downloads/" + str(company_data[1]) + ".csv", index_col = "Date", parse_dates = True)
        self.max_time = self.historical_data.shape[0]
        self.new_vizualization(5)

    def get_days_nr(self, date_target):
        return(self.historical_data[self.historical_data.index >= np.datetime64(date_target)].shape[0])

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
        self.historical_data = pd.read_csv("downloads/" + str(company_data[1]) + ".csv", index_col = "Date", parse_dates = True)
        self.max_time = self.historical_data.shape[0]
        self.new_vizualization(5)

    def change_vizualization(self, event, period):
        if period > self.max_time:
            messagebox.showerror('Python Error', 'Error: Not enough data is loaded!')
            return
        
        self.new_vizualization(period)

    def change_vizualization_changes(self, event, period):
        if period > self.max_time:
            messagebox.showerror('Python Error', 'Error: Not enough data is loaded!')
            return
        
        self.new_vizualization_changes(period)
    
    def new_vizualization(self, period):
        
        self.subplot.clear()
        time_period = self.historical_data[["Open"]].tail(period)
        time_period.index = pd.to_datetime(time_period.index, format = '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
        
        color, information = self.increased_or_decreased(float(time_period['Open'].head(1)), float(time_period['Open'].tail(1)))
        
        time_period.plot(y='Open', use_index=True, color = color, grid = True, ax=self.subplot)
        
        self.plots.draw()
        self.graph_info.config(text = company_data[1] + information, fg = color)

    def new_vizualization_changes(self, period):
        
        self.subplot.clear()
        
        percentage_changes = self.historical_data[['Open']].tail(period).pct_change().dropna().apply(lambda x: x*100)
        percentage_changes.reset_index(inplace = True)

        colors = ['red' if x < 0 else 'green' for x in percentage_changes['Open']]
        sizes = [abs(x*10) for x in percentage_changes['Open']]

        color, information = self.increased_or_decreased(float(percentage_changes['Open'].head(1)), float(percentage_changes['Open'].tail(1)))

        percentage_changes.plot.scatter(x = 'Date', y = 'Open', marker = "d", s = sizes, c = colors, grid = True, ax=self.subplot)
        
        self.plots.draw()
        self.graph_info.config(text = company_data[1] + information, fg = color)
        

    def change_vizualization_custom(self, event):
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
        
        color, information = self.increased_or_decreased(float(custom_period['Open'].head(1)), float(custom_period['Open'].tail(1)))
        custom_period.plot(y='Open', color = color, grid = True, ax=self.subplot)
        self.plots.draw()
        self.graph_info.config(text = company_data[1] + information, fg = color)

    def change_vizualization_custom_changes(self, event):
        start = self.date_start.get_date()
        end = self.date_end.get_date()

        if start > end:
            messagebox.showerror('Python Error', 'Error: the given dates are incorrect!')
            return

        if end > self.now:
            messagebox.showerror('Python Error', 'Error: the given dates are incorrect!')
            return

        self.subplot.clear()

        percentage_changes = self.historical_data[['Open']][(self.historical_data.index >= np.datetime64(start)) & (self.historical_data.index <= np.datetime64(end))].pct_change().dropna().apply(lambda x: x*100)
        percentage_changes.reset_index(inplace = True)

        colors = ['red' if x < 0 else 'green' for x in percentage_changes['Open']]
        sizes = [abs(x*10) for x in percentage_changes['Open']]

        color, information = self.increased_or_decreased(float(percentage_changes['Open'].head(1)), float(percentage_changes['Open'].tail(1)))

        percentage_changes.plot.scatter(x = 'Date', y = 'Open', marker = "D", s = sizes, c = colors, grid = True, ax=self.subplot)
        
        self.plots.draw()
        self.graph_info.config(text = company_data[1] + information, fg = color)
    
def page():    
    root = Tk()
    #root.geometry("770x396")
    Page3(root)
    root.mainloop()

if __name__ == '__main__':
    page()
