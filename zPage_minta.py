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

import xPage1
import xPage3
import xPage4

class Page2:
    
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
        
        self.change_vizualization_ow(event)

    def load_in_historical_data(self, begin, end):
        
        min_val = 2000000000.0
        max_val = 0.0
        x = []
        y = []

        
        for i in range(begin, end+1):
            historical_row = self.historical_data[i].strip().split(',')
            num = historical_row[1]
            num_flo = float(num)

            y.append(num_flo)
            x.append(i-begin)
            
            min_val = min(min(min_val, avg - 24*avg/100),num_flo)
            max_val = max(max(max_val, avg + 24*avg/100),num_flo)

        dif = (max_val-min_val)*5/100

        color, information = self.increased_or_decreased(self.historical_data[begin], self.historical_data[end])

        return min_val, max_val, x, y, dif, color, information

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
        self.plots.draw()
        self.graph_info.config(text = information, fg = color)
        
def page():
    root = Tk()
    root.geometry("770x396")
    Page6(root)
    root.mainloop()

if __name__ == '__main__':
    page()
