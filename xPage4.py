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

from datetime import date
from datetime import datetime

from data import *

import xPage2

class Page4:

    def __init__(self, root):
        self.root = root
        self.root.geometry("770x396")

        self.width = 770
        self.height = 396
        self.box_x = 22
        self.box_y = 22
        self.font = 1
        self.historical_data = []
        self.max_time = 0

                #_____Control buttons_____
        self.exit = Button(root, text="EXIT")
        self.exit.bind('<Button-1>', self.go_exit)
        self.exit.place(x=0*self.box_x, y=0*self.box_y, width=3*self.box_x, height=1*self.box_y)
        
        self.back = Button(root, text="BACK")
        self.back.bind('<Button-1>', self.go_back)
        self.back.place(x=3*self.box_x, y=0*self.box_y, width=3*self.box_x, height=1*self.box_y)
                
                #_____Imput field for company search_____
        self.companies = ttk.Combobox(root)
        self.companies.set(company_data[0])
        self.companies['values'] = companies_name
        self.companies.bind('<KeyRelease>', self.check_companies)
        self.companies.place(x=12*self.box_x, y=1*self.box_y, width=11*self.box_x, height=1*self.box_y)

        self.search = Button(root, text="Search")
        self.search.bind('<Button-1>', self.search_companies)
        self.search.place(x=23*self.box_x, y=1*self.box_y, width=4*self.box_x, height=1*self.box_y)

                #_____Buttons for certain intervall visualization_____
        self.one_week = Button(root, text="One week", command = lambda: self.change_vizualization(self, self.max_time-6, self.max_time))
        self.one_week.place(x=0*self.box_x, y=2*self.box_y, width=5*self.box_x, height=1*self.box_y)

        self.one_week = Button(root, text="Two weeks", command = lambda: self.change_vizualization(self, self.max_time-13, self.max_time))
        self.one_week.place(x=0*self.box_x, y=4*self.box_y, width=5*self.box_x, height=1*self.box_y)
        
        self.one_week = Button(root, text="One month", command = lambda: self.change_vizualization(self, self.max_time-29, self.max_time))
        self.one_week.place(x=0*self.box_x, y=6*self.box_y, width=5*self.box_x, height=1*self.box_y)

        self.one_week = Button(root, text="Three monts", command = lambda: self.change_vizualization(self, self.max_time-89, self.max_time))
        self.one_week.place(x=0*self.box_x, y=8*self.box_y, width=5*self.box_x, height=1*self.box_y)

        self.one_week = Button(root, text="Six monts", command = lambda: self.change_vizualization(self, self.max_time-179, self.max_time))
        self.one_week.place(x=0*self.box_x, y=10*self.box_y, width=5*self.box_x, height=1*self.box_y)

        self.one_week = Button(root, text="One year", command = lambda: self.change_vizualization(self, self.max_time-364, self.max_time))
        self.one_week.place(x=0*self.box_x, y=12*self.box_y, width=5*self.box_x, height=1*self.box_y)

        self.one_week = Button(root, text="Five years", command = lambda: self.change_vizualization(self, self.max_time-1824, self.max_time))
        self.one_week.place(x=0*self.box_x, y=14*self.box_y, width=5*self.box_x, height=1*self.box_y)

        self.one_week = Button(root, text="Max time", command = lambda: self.change_vizualization(self, 1, self.max_time))
        self.one_week.place(x=0*self.box_x, y=16*self.box_y, width=5*self.box_x, height=1*self.box_y)

            #_____Graph abouth the data_____
        self.figure = Figure(figsize=(6, 6), dpi=100)
        
        self.subplot = self.figure.add_subplot(111)
        self.subplot.set_ylabel('Value($)', fontsize=6)
        self.subplot.set_xlabel('Time(day)', fontsize=6)
        self.subplot.set_xlim(0, 10)
        self.subplot.set_ylim(0, 10)
        
        self.plots = FigureCanvasTkAgg(self.figure, root)
        self.plots.get_tk_widget().place(x=5*self.box_x, y=3*self.box_y, width=23*self.box_x, height=14*self.box_y)

                #_____Label for information of the graph_____
        self.graph_info = Label(root, text="")
        self.graph_info.place(x=9*self.box_x, y=2*self.box_y, width=17*self.box_x, height=1*self.box_y)

                #____Date input for specific time period_____
        self.date_from = Label(root, text="From:")
        self.date_from.place(x=6*self.box_x, y=17*self.box_y, width=2*self.box_x, height=1*self.box_y)
        self.date_start = DateEntry(root, width= 16, background= "magenta3", foreground= "white",bd=2)
        self.date_start.place(x=8*self.box_x, y=17*self.box_y, width=5*self.box_x, height=1*self.box_y)

        self.date_to = Label(root, text="To:")
        self.date_to.place(x=13*self.box_x, y=17*self.box_y, width=2*self.box_x, height=1*self.box_y)
        self.date_end = DateEntry(root, width = 16, background= "magenta3", foreground= "white",bd=2)
        self.date_end.place(x=15*self.box_x, y=17*self.box_y, width=5*self.box_x, height=1*self.box_y)

        self.show = Button(root, text="Show")
        self.show.bind('<Button-1>', self.change_vizualization_custom)
        self.show.place(x=20*self.box_x, y=17*self.box_y, width=5*self.box_x, height=1*self.box_y)


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
        
        file = open("downloads/" + str(company_data[1] + ".csv"), 'r')
        self.historical_data = file.readlines()

        self.max_time = len(self.historical_data) - 1
        
        self.change_vizualization(self, self.max_time-6, self.max_time)

    def increased_or_decreased(self, begin_period, end_period):
        
        historical_row_begin = begin_period.strip().split(',')
        num_begin = historical_row_begin[1]
        num_flo_begin = round(float(num_begin), 2)
        
        historical_row_end = end_period.strip().split(',')
        num_end = historical_row_end[1]
        num_flo_end = round(float(num_end), 2)

        if num_flo_begin == 0:
            num_flo_begin = 0.01
        
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

    def build_up_Bell_model(self, begin, end):

        su = 0
        min_val = 2000000000.0
        max_val = 0.0
        x = []
        y = []
        bell_model = [[],[],[],[],[]]
        
        for i in range(begin, end+1):
            historical_row = self.historical_data[i].strip().split(',')
            num = historical_row[1]
            num_flo = float(num)

            su += num_flo
            avg = su/(i-begin+1)

            y.append(num_flo)
            x.append(i-begin)
            
            bell_model[0].append(avg + 24*avg/100)
            bell_model[1].append(avg + 17*avg/100) 
            bell_model[2].append(avg)
            bell_model[3].append(avg - 17*avg/100)
            bell_model[4].append(avg - 24*avg/100)
            
            min_val = min(min(min_val, avg - 24*avg/100),num_flo)
            max_val = max(max(max_val, avg + 24*avg/100),num_flo)

        dif = (max_val-min_val)*5/100

        color, information = self.increased_or_decreased(self.historical_data[begin], self.historical_data[end])

        return min_val, max_val, x, y, bell_model, dif, color, information

    def change_initial_vizualization(self):
        file = open("downloads/" + str(company_data[1] + ".csv"), 'r')
        self.historical_data = file.readlines()

        self.max_time = len(self.historical_data) - 1
        
        if self.max_time == 0:
            messagebox.showerror('Python Error', 'Error: Not enough data is loaded!')
            return

        if self.max_time < 7:
            messagebox.showerror('Python Error', 'Error: Not enough data is available yet!')
            return

        if company_data[0] == "ERROR" or company_data[0] == "":
            messagebox.showerror('Python Error', 'Error: The data is not loaded yet!')
            return

        self.subplot.clear()
        min_val, max_val, x, y, bell_model, dif, color, information = self.build_up_Bell_model(self.max_time-6, self.max_time)
        self.subplot.set_xlim(0, 6)
        self.subplot.tick_params(axis='x', labelsize=11)
        self.subplot.tick_params(axis='y', labelsize=11)
        self.subplot.set_ylim(min_val-dif, max_val+dif)
        self.subplot.plot(x, y, color, lw=1)
        self.subplot.plot(x, bell_model[0], "greenyellow", lw = 1)
        self.subplot.plot(x, bell_model[1], "limegreen", lw = 1)
        self.subplot.plot(x, bell_model[2], "blue", lw = 1)
        self.subplot.plot(x, bell_model[3], "orangered", lw = 1)
        self.subplot.plot(x, bell_model[4], "maroon", lw = 1)
        self.plots.draw()
        self.graph_info.config(text = information, fg = color)
        

    def change_vizualization(self, event, begin, end):
        if self.max_time < (end-begin):
            messagebox.showerror('Python Error', 'Error: Not enough data is available yet!')
            return

        if company_data[0] == "ERROR" or company_data[0] == "":
            messagebox.showerror('Python Error', 'Error: The data is not loaded yet!')
            return

        self.subplot.clear()
        min_val, max_val, x, y, bell_model, dif, color, information = self.build_up_Bell_model(begin, end)
        self.subplot.set_xlim(0, end-begin)
        self.subplot.tick_params(axis='x', labelsize=11)
        self.subplot.tick_params(axis='y', labelsize=11)
        self.subplot.set_ylim(min_val-dif, max_val+dif)
        self.subplot.plot(x, y, color, lw=1)
        self.subplot.plot(x, bell_model[0], "greenyellow", lw = 1)
        self.subplot.plot(x, bell_model[1], "limegreen", lw = 1)
        self.subplot.plot(x, bell_model[2], "blue", lw = 1)
        self.subplot.plot(x, bell_model[3], "orangered", lw = 1)
        self.subplot.plot(x, bell_model[4], "maroon", lw = 1)
        self.plots.draw()
        self.graph_info.config(text = information, fg = color)

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
    
        i = self.max_time
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




















        
        
