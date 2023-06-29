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

import xPage2

class Page4:

    def __init__(self, root):
        self.root = root
        self.root.geometry("770x396")
        self.root.bind("<Configure>", self.resize_window)
        
        self.box_x = 22
        self.box_y = 22
        self.ticker = ''
        self.historical_data = []
        self.data_time_size = 0

        self.now = datetime.today().date()

                #_____Control buttons_____
        self.exit = Button(root, text="EXIT")
        self.exit.bind('<Button-1>', self.go_exit)
        
        self.back = Button(root, text="BACK")
        self.back.bind('<Button-1>', self.go_back)
                
                #_____Imput field for company search_____
        self.companies = ttk.Combobox(root)
        self.companies.set(company_data[0])
        self.companies['values'] = companies_name
        self.companies.bind('<KeyRelease>', self.check_companies)

        self.search = Button(root, text="Search")
        self.search.bind('<Button-1>', self.search_companies)

                #_____Buttons for certain intervall visualization_____
        self.one_week = Button(root, text="One week", command = lambda: self.change_vizualization_50(self, 5))

        self.one_month = Button(root, text="One month", command = lambda: self.change_vizualization_50(self, self.get_days_nr(self.now - relativedelta(months=1))))
        
        self.three_monts = Button(root, text="Three monts", command = lambda: self.change_vizualization_50(self, self.get_days_nr(self.now - relativedelta(months=3))))

        self.six_monts = Button(root, text="Six monts", command = lambda: self.change_vizualization_50(self, self.get_days_nr(self.now - relativedelta(months=6))))

        self.one_year = Button(root, text="One year", command = lambda: self.change_vizualization_50(self, self.get_days_nr(self.now - relativedelta(years=1))))

        self.three_years = Button(root, text="Three years", command = lambda: self.change_vizualization_50(self, self.get_days_nr(self.now - relativedelta(years=3))))

        self.five_years = Button(root, text="Five years", command = lambda: self.change_vizualization_50(self, self.get_days_nr(self.now - relativedelta(years=5))))

        self.max_time = Button(root, text="Max time", command = lambda: self.change_vizualization_50(self, self.data_time_size))

                #_____Graph abouth the data_____
        self.figure = Figure(figsize=(4, 7), dpi=100)
        
        self.subplot = self.figure.add_subplot(111)
        
        self.plots = FigureCanvasTkAgg(self.figure, root)
        
                #_____Label for information of the graph_____
        self.graph_info = Label(root, text="")

                #____Date input for specific time period_____
        self.date_from = Label(root, text="From:")
        self.date_start = DateEntry(root, width= 16, date_pattern='YYYY-MM-DD', background= "magenta3", foreground= "white",bd=2)

        self.date_to = Label(root, text="To:")
        self.date_end = DateEntry(root, width = 16, date_pattern='YYYY-MM-DD', background= "magenta3", foreground= "white",bd=2)

        self.show = Button(root, text="Show")
        self.show.bind('<Button-1>', self.change_vizualization_custom)

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
        
    def change_initial_vizualization(self):
        self.historical_data = pd.read_csv("downloads/" + str(company_data[1]) + ".csv", index_col = "Date", parse_dates = True)
        self.data_time_size = self.historical_data.shape[0]
        
        self.new_vizualization_50(5)

    def search_companies(self, event):
        company_name = str(self.companies.get())

        self.ticker = self.searh_for_ticker(company_name)

        if company_data[0] == "ERROR":
            messagebox.showerror('Python Error', 'Error: No such company in the data base!')
            return
        
        self.historical_data = pd.read_csv("downloads/" + str(company_data[1]) + ".csv", index_col = "Date", parse_dates = True)
        self.data_time_size = self.historical_data.shape[0]

        self.new_vizualization_50(5)

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

    def change_vizualization_50(self, event, period):
        if period > self.data_time_size:
            messagebox.showerror('Python Error', 'Error: Not enough data is loaded!')
            return
        
        self.new_vizualization_50(period)

    def change_vizualization_200(self, event, period):
        if period > self.data_time_size:
            messagebox.showerror('Python Error', 'Error: Not enough data is loaded!')
            return
        
        self.new_vizualization(period)
        
    def new_vizualization_50(self, period):
        
        self.subplot.clear()
        time_period = self.historical_data[["Open", "SMA50","BELL50up1", "BELL50up2", "BELL50bo1", "BELL50bo2"]].tail(period)
        time_period.index = pd.to_datetime(time_period.index, format = '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
        
        color, information = self.increased_or_decreased(float(time_period["Open"].head(1)), float(time_period["Open"].tail(1)))
        colors = [color] + ["blue", "greenyellow", "limegreen", "orangered", "maroon"]
        time_period.plot(use_index=True, y=["Open", "SMA50","BELL50up1", "BELL50up2", "BELL50bo1", "BELL50bo2"], color = colors, grid = True, ax=self.subplot)
        self.plots.draw()
        self.graph_info.config(text = company_data[1] + information, fg = color)

    def new_vizualization_200(self, period):
        
        self.subplot.clear()
        time_period = self.historical_data[["Open", "SMA200","BELL200up1", "BELL200up2", "BELL200bo1", "BELL200bo2"]].tail(period)
        time_period.index = pd.to_datetime(time_period.index, format = '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
        
        color, information = self.increased_or_decreased(float(time_period["Open"].head(1)), float(time_period["Open"].tail(1)))
        colors = [color] + ["blue", "greenyellow", "limegreen", "orangered", "maroon"]
        time_period.plot(use_index=True, y=["Open", "SMA200","BELL200up1", "BELL200up2", "BELL200bo1", "BELL200bo2"], color = colors, grid = True, ax=self.subplot)
        self.plots.draw()
        self.graph_info.config(text = company_data[1] + information, fg = color)

        
    def change_vizualization_custom(self, event):
        now = date.today()
        start = self.date_start.get_date()
        end = self.date_end.get_date()

        if start > end:
            messagebox.showerror('Python Error', 'Error: the given dates are incorrect!')
            return

        if end > now:
            messagebox.showerror('Python Error', 'Error: the given dates are incorrect!')
            return
    
        i = self.data_time_size
        a = 0
        b = 0

        while True and i>0:
            historical_row = self.historical_data[i].strip().split(',')
            date_info = historical_row[0].strip().split(' ')
            row_date = datetime.strptime(date_info[0], "%Y-%m-%d").date()

            if row_date == end:
                b = i
                break
            i-=1

        while True and i>0:
            historical_row = self.historical_data[i].strip().split(',')
            date_info = historical_row[0].strip().split(' ')
            row_date = datetime.strptime(date_info[0], "%Y-%m-%d").date()

            if row_date == start:
                a = i
                break
            i-=1

        if a == 0 or b == 0:
            messagebox.showerror('Python Error', 'Error: no such time interval in the database!')
            return

        self.change_vizualization(self, a, b)

    def resize_window(self, event):
        x_len = self.root.winfo_width()
        y_len = self.root.winfo_height()
        
        self.box_x = int(x_len/35)
        self.box_y = int(y_len/18)
        self.font = int(self.box_x/22)

        #_____Control buttons_____
        self.exit.place(x=0*self.box_x, y=0, width=3*self.box_x, height=1*self.box_y)
        
        self.back.place(x=3*self.box_x, y=0, width=3*self.box_x, height=1*self.box_y)
                
                #_____Imput field for company search_____
        self.companies.place(x=12*self.box_x, y=0, width=11*self.box_x, height=1*self.box_y)

        self.search.place(x=23*self.box_x, y=0, width=4*self.box_x, height=1*self.box_y)

                #_____Buttons for certain intervall visualization_____
        self.one_week.place(x=0*self.box_x, y=2*self.box_y, width=5*self.box_x, height=1*self.box_y)
        
        self.one_month.place(x=0*self.box_x, y=4*self.box_y, width=5*self.box_x, height=1*self.box_y)

        self.three_monts.place(x=0*self.box_x, y=6*self.box_y, width=5*self.box_x, height=1*self.box_y)

        self.six_monts.place(x=0*self.box_x, y=8*self.box_y, width=5*self.box_x, height=1*self.box_y)

        self.one_year.place(x=0*self.box_x, y=10*self.box_y, width=5*self.box_x, height=1*self.box_y)

        self.three_years.place(x=0*self.box_x, y=12*self.box_y, width=5*self.box_x, height=1*self.box_y)

        self.five_years.place(x=0*self.box_x, y=14*self.box_y, width=5*self.box_x, height=1*self.box_y)

        self.max_time.place(x=0*self.box_x, y=16*self.box_y, width=5*self.box_x, height=1*self.box_y)

            #_____Graph abouth the data_____
        self.subplot.set_ylabel('Value($)', fontsize=self.box_x*8/ 22)
        self.subplot.set_xlabel('Time(day)', fontsize=self.box_x*8/ 22)
        self.subplot.tick_params(axis='x', labelsize=self.box_x*7/ 22)
        self.subplot.tick_params(axis='y', labelsize=self.box_x*12/ 22)
        self.plots.get_tk_widget().place(x=5*self.box_x, y=2*self.box_y, width=24*self.box_x, height=15*self.box_y)

        
                #_____Label for information of the graph_____
        self.graph_info.place(x=9*self.box_x, y=1*self.box_y, width=17*self.box_x, height=1*self.box_y)

                #____Date input for specific time period_____
        self.date_from.place(x=6*self.box_x, y=17*self.box_y, width=2*self.box_x, height=1*self.box_y)
        self.date_start.place(x=8*self.box_x, y=17*self.box_y, width=5*self.box_x, height=1*self.box_y)

        self.date_to.place(x=13*self.box_x, y=17*self.box_y, width=2*self.box_x, height=1*self.box_y)
        self.date_end.place(x=15*self.box_x, y=17*self.box_y, width=5*self.box_x, height=1*self.box_y)

        self.show.place(x=20*self.box_x, y=17*self.box_y, width=5*self.box_x, height=1*self.box_y)


def page():    
    root = Tk()
    #root.geometry("770x396")
    Page4(root)
    root.mainloop()

if __name__ == '__main__':
    page()



















        
        
