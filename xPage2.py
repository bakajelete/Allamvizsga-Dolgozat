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

from datetime import datetime
from dateutil.relativedelta import relativedelta
import time

from data import *

import xPage1
import xPage3
import xPage4

class Page2:
    
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
        self.one_week = Button(root, text="One week", command = lambda: self.change_vizualization(self, 5))

        self.two_weeks = Button(root, text="Two weeks", command = lambda: self.change_vizualization(self, 10))
        
        self.one_month = Button(root, text="One month", command = lambda: self.change_vizualization(self, self.get_days_nr(self.now - relativedelta(months=1))))

        self.six_months = Button(root, text="Six months", command = lambda: self.change_vizualization(self, self.get_days_nr(self.now - relativedelta(months=6))))
        
        self.one_year = Button(root, text="One year", command = lambda: self.change_vizualization(self, self.get_days_nr(self.now - relativedelta(years=1))))

        self.five_years = Button(root, text="Five years", command = lambda: self.change_vizualization(self, self.get_days_nr(self.now - relativedelta(years=5))))

        self.max_time = Button(root, text="Max time", command = lambda: self.change_vizualization(self, self.data_time_size))


                #_____Buttons for page change_____
        self.more_detail = Button(root, text="More Details")
        self.more_detail.bind('<Button-1>', self.change_page_to_more_details)
        
        self.analize_01 = Button(root, text="Linear Regression")
        self.analize_01.bind('<Button-1>', self.change_page_to_analize_01)

        self.analize_02 = Button(root, text="Analize b)")
        self.analize_02.bind('<Button-1>', self.change_page_to_analize_02)

        self.analize_03 = Button(root, text="Analize c)")
        self.analize_03.bind('<Button-1>', self.change_page_to_analize_03)

                #_____Graph abouth the data_____
        self.figure = Figure(figsize=(4, 7), dpi=100)
        
        self.subplot = self.figure.add_subplot(111)
        
        self.plots = FigureCanvasTkAgg(self.figure, root)

                #_____Label for information of the graph_____
        self.graph_info = Label(root, text="")  
        
        self.change_initial_vizualization()

    def go_exit(self, event):
        self.root.destroy()
    
    def go_back(self, event):
        win = Toplevel()
        self.root.withdraw()
        xPage1.Page1(win)
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
        self.data_time_size = self.historical_data.shape[0]
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
        self.data_time_size = self.historical_data.shape[0]
        self.new_vizualization(5)

    def change_vizualization(self, event, period):
        if period > self.data_time_size:
            messagebox.showerror('Python Error', 'Error: Not enough data is loaded!')
            return
        
        self.new_vizualization(period)
    
    def new_vizualization(self, period):
        
        self.subplot.clear()
        time_period = self.historical_data[["Open"]].tail(period)
        time_period.index = pd.to_datetime(time_period.index, format = '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
        
        color, information = self.increased_or_decreased(float(time_period['Open'].head(1)), float(time_period['Open'].tail(1)))
        time_period.plot(use_index=True, y='Open', color = color, grid = True, ax=self.subplot)
        self.plots.draw()
        self.graph_info.config(text = company_data[1] + information, fg = color)

    def change_page_to_more_details(self, event):
        win = Toplevel()
        self.root.withdraw()
        xPage3.Page3(win)
        win.deiconify()
        

    def change_page_to_analize_01(self, event):
        win = Toplevel()
        self.root.withdraw()
        xPage4.Page4(win)
        win.deiconify()

    def change_page_to_analize_02(self, event):
        print("analize_02")
    
    def change_page_to_analize_03(self, event):
        print("analize_03")

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
        self.one_week.place(x=0, y=2*self.box_y, width=5*self.box_x, height=1*self.box_y)
        self.two_weeks.place(x=0, y=5*self.box_y, width=5*self.box_x, height=1*self.box_y)
        self.one_month.place(x=0, y=8*self.box_y, width=5*self.box_x, height=1*self.box_y)
        self.six_months.place(x=0, y=11*self.box_y, width=5*self.box_x, height=1*self.box_y)
        self.one_year.place(x=x_len-5*self.box_x, y=2*self.box_y, width=5*self.box_x, height=1*self.box_y)
        self.five_years.place(x=x_len-5*self.box_x, y=5*self.box_y, width=5*self.box_x, height=1*self.box_y)
        self.max_time.place(x=x_len-5*self.box_x, y=8*self.box_y, width=5*self.box_x, height=1*self.box_y)
        
                #_____Buttons for page change_____
        self.more_detail.place(x=x_len-5*self.box_x, y=11*self.box_y, width=5*self.box_x, height=1*self.box_y)
        self.analize_01.place(x=8*self.box_x, y=16*self.box_y, width=5*self.box_x, height=1*self.box_y)
        self.analize_02.place(x=15*self.box_x, y=16*self.box_y, width=5*self.box_x, height=1*self.box_y)
        self.analize_03.place(x=22*self.box_x, y=16*self.box_y, width=5*self.box_x, height=1*self.box_y)

                #_____Graph abouth the data_____
        self.subplot.set_ylabel('Value($)', fontsize=self.box_x*8/ 22)
        self.subplot.set_xlabel('Time(day)', fontsize=self.box_x*8/ 22)
        self.subplot.tick_params(axis='x', labelsize=self.box_x*8/ 22)
        self.subplot.tick_params(axis='y', labelsize=self.box_x*12/ 22)
        self.plots.get_tk_widget().place(x=5*self.box_x, y=2*self.box_y, width=25*self.box_x, height=14*self.box_y)

                #_____Label for information of the graph_____
        self.graph_info.place(x=9*self.box_x, y=1*self.box_y, width=17*self.box_x, height=1*self.box_y)

'''
root = Tk()
#root.geometry("770x396")
#a laptopom full parameterei 1540x1080
#beegetve jol nez ki full kepernyo 1540x792
#1540 = 2^2*5*7*11, 792=2^3*3^2*11 

page2 = Page2(root)
root.title('My model')

a = root.winfo_reqwidth()
b = root.winfo_height()

root.mainloop()

'''
def page():
    root = Tk()
    root.geometry("770x396")
    Page2(root)
    root.mainloop()

if __name__ == '__main__':
    page()
