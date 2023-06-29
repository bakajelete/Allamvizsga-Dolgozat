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

                #_____Buttons for certain intervall visualization_____ 
        self.one_week = Button(root, text="One week")
        self.one_week.bind('<Button-1>', self.change_vizualization_ow)
        self.one_week.place(x=1*self.box_x, y=4*self.box_y, width=5*self.box_x, height=1*self.box_y)

        self.two_week = Button(root, text="Two weeks")
        self.two_week.bind('<Button-1>', self.change_vizualization_tw)
        self.two_week.place(x=1*self.box_x, y=7*self.box_y, width=5*self.box_x, height=1*self.box_y)
        
        self.one_month = Button(root, text="One month")
        self.one_month.bind('<Button-1>', self.change_vizualization_om)
        self.one_month.place(x=1*self.box_x, y=10*self.box_y, width=5*self.box_x, height=1*self.box_y)

        self.six_month = Button(root, text="Six months")
        self.six_month.bind('<Button-1>', self.change_vizualization_sm)
        self.six_month.place(x=1*self.box_x, y=13*self.box_y, width=5*self.box_x, height=1*self.box_y)
        
        self.one_year = Button(root, text="One year")
        self.one_year.bind('<Button-1>', self.change_vizualization_oy)
        self.one_year.place(x=29*self.box_x, y=4*self.box_y, width=5*self.box_x, height=1*self.box_y)

        self.five_year = Button(root, text="Five years")
        self.five_year.bind('<Button-1>', self.change_vizualization_fy)
        self.five_year.place(x=29*self.box_x, y=7*self.box_y, width=5*self.box_x, height=1*self.box_y)

        self.max = Button(root, text="Maximum time")
        self.max.bind('<Button-1>', self.change_vizualization_mt)
        self.max.place(x=29*self.box_x, y=10*self.box_y, width=5*self.box_x, height=1*self.box_y)

                #_____Buttons for page change_____
        self.more_detail = Button(root, text="More Details")
        self.more_detail.bind('<Button-1>', self.change_page_to_more_details)
        self.more_detail.place(x=29*self.box_x, y=13*self.box_y, width=5*self.box_x, height=1*self.box_y)
        
        self.analize_01 = Button(root, text="Linear Regression")
        self.analize_01.bind('<Button-1>', self.change_page_to_analize_01)
        self.analize_01.place(x=8*self.box_x, y=16*self.box_y, width=5*self.box_x, height=1*self.box_y)

        self.analize_02 = Button(root, text="Analize b)")
        self.analize_02.bind('<Button-1>', self.change_page_to_analize_02)
        self.analize_02.place(x=15*self.box_x, y=16*self.box_y, width=5*self.box_x, height=1*self.box_y)

        self.analize_03 = Button(root, text="Analize c)")
        self.analize_03.bind('<Button-1>', self.change_page_to_analize_03)
        self.analize_03.place(x=22*self.box_x, y=16*self.box_y, width=5*self.box_x, height=1*self.box_y)

                #_____Graph abouth the data_____
        self.figure = Figure(figsize=(4.5, 6), dpi=100)
        
        self.subplot = self.figure.add_subplot(111)
        self.subplot.set_ylabel('Value($)', fontsize=6)
        self.subplot.set_xlabel('Time(day)', fontsize=6)
        self.subplot.set_xlim(0, 10)
        self.subplot.set_ylim(0, 10)
        
        self.plots = FigureCanvasTkAgg(self.figure, root)
        self.plots.get_tk_widget().place(x=7*self.box_x, y=3*self.box_y, width=21*self.box_x, height=12*self.box_y)

                #_____Label for information of the graph_____
        self.graph_info = Label(root, text="")
        self.graph_info.place(x=9*self.box_x, y=2*self.box_y, width=17*self.box_x, height=1*self.box_y)

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
        
        file = open("downloads/" + str(company_data[1] + ".csv"), 'r')
        self.historical_data = file.readlines()

        self.max_time = len(self.historical_data) - 1
        
        self.change_vizualization_ow(event)                                 

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
    
    def load_in_historical_data(self, time):
                
        if company_data[0] == "ERROR" or company_data[0] == "":
            messagebox.showerror('Python Error', 'Error: The data is not loaded yet!')
            return
        
        min_val = 2000000000.0
        max_val = 0.0
        x = []
        y = []
        
        for i in range(self.max_time - time, self.max_time + 1):
            historical_row = self.historical_data[i].strip().split(',')

            num = historical_row[1]
            num_flo = float(num)
            time_info = historical_row[0]
            date = time_info.strip().split(' ')
            
            min_val = min(min_val, num_flo)
            max_val = max(max_val, num_flo)

            x.append(i-self.max_time+time)
            y.append(num_flo)

        dif = (max_val-min_val)*10/100

        color, information = self.increased_or_decreased(self.historical_data[self.max_time - time], self.historical_data[self.max_time-1])

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
        min_val, max_val, x, y, dif, color, information = self.load_in_historical_data(7)
        self.subplot.set_xlim(0, 6)
        self.subplot.tick_params(axis='x', labelsize=11)
        self.subplot.tick_params(axis='y', labelsize=11)
        self.subplot.set_ylim(min_val-dif, max_val+dif)
        self.subplot.plot(x, y, color, lw=1)
        self.plots.draw()
        self.graph_info.config(text = information, fg = color)
    
    def change_vizualization_ow(self, event):
        if self.max_time < 7:
            messagebox.showerror('Python Error', 'Error: Not enough data is available yet!')
            return
        
        if company_data[0] == "ERROR" or company_data[0] == "":
            messagebox.showerror('Python Error', 'Error: The data is not loaded yet!')
            return
        
        self.subplot.clear()
        min_val, max_val, x, y, dif, color, information = self.load_in_historical_data(7)
        self.subplot.set_xlim(0, 6)
        self.subplot.tick_params(axis='x', labelsize=11)
        self.subplot.tick_params(axis='y', labelsize=11)
        self.subplot.set_ylim(min_val-dif, max_val+dif)
        self.subplot.plot(x, y, color, lw=1)
        self.plots.draw()
        self.graph_info.config(text = information, fg = color)
    
        
    def change_vizualization_tw(self, event):
        if self.max_time < 14:
            messagebox.showerror('Python Error', 'Error: Not enough data is available yet!')
            return

        if company_data[0] == "ERROR" or company_data[0] == "":
            messagebox.showerror('Python Error', 'Error: The data is not loaded yet!')
            return
        
        self.subplot.clear()
        min_val, max_val, x, y, dif, color, information = self.load_in_historical_data(14)
        self.subplot.set_xlim(0, 13)
        self.subplot.tick_params(axis='x', labelsize=11)
        self.subplot.tick_params(axis='y', labelsize=11)
        self.subplot.set_ylim(min_val-dif, max_val+dif)
        self.subplot.plot(x, y, color, lw=1)
        self.plots.draw()
        self.graph_info.config(text = information, fg = color)

    def change_vizualization_om(self, event):
        if self.max_time < 30:
            messagebox.showerror('Python Error', 'Error: Not enough data is available yet!')
            return

        if company_data[0] == "ERROR" or company_data[0] == "":
            messagebox.showerror('Python Error', 'Error: The data is not loaded yet!')
            return
        
        self.subplot.clear()
        min_val, max_val, x, y, dif, color, information = self.load_in_historical_data(30)
        self.subplot.set_xlim(0, 29)
        self.subplot.tick_params(axis='x', labelsize=11)
        self.subplot.tick_params(axis='y', labelsize=11)
        self.subplot.set_ylim(min_val-dif, max_val+dif)
        self.subplot.plot(x, y, color, lw=1)
        self.plots.draw()
        self.graph_info.config(text = information, fg = color)

    def change_vizualization_sm(self, event):
        if self.max_time < 180:
            messagebox.showerror('Python Error', 'Error: Not enough data is available yet!')
            return

        if company_data[0] == "ERROR" or company_data[0] == "":
            messagebox.showerror('Python Error', 'Error: The data is not loaded yet!')
            return
        
        self.subplot.clear()
        min_val, max_val, x, y, dif, color, information = self.load_in_historical_data(180)
        self.subplot.set_xlim(0, 179)
        self.subplot.tick_params(axis='x', labelsize=11)
        self.subplot.tick_params(axis='y', labelsize=11)
        self.subplot.set_ylim(min_val-dif, max_val+dif)
        self.subplot.plot(x, y, color, lw=1)
        self.plots.draw()
        self.graph_info.config(text = information, fg = color)

    def change_vizualization_oy(self, event):
        if self.max_time < 365:
            messagebox.showerror('Python Error', 'Error: Not enough data is available yet!')
            return

        if company_data[0] == "ERROR" or company_data[0] == "":
            messagebox.showerror('Python Error', 'Error: The data is not loaded yet!')
            return
        
        self.subplot.clear()
        min_val, max_val, x, y, dif, color, information = self.load_in_historical_data(365)
        self.subplot.set_xlim(0, 364)
        self.subplot.tick_params(axis='x', labelsize=11)
        self.subplot.tick_params(axis='y', labelsize=11)
        self.subplot.set_ylim(min_val-dif, max_val+dif)
        self.subplot.plot(x, y, color, lw=1)
        self.plots.draw()
        self.graph_info.config(text = information, fg = color)

    def change_vizualization_fy(self, event):
        if self.max_time < 1825:
            messagebox.showerror('Python Error', 'Error: Not enough data is available yet!')
            return

        if company_data[0] == "ERROR" or company_data[0] == "":
            messagebox.showerror('Python Error', 'Error: The data is not loaded yet!')
            return
        
        self.subplot.clear()
        min_val, max_val, x, y, dif, color, information = self.load_in_historical_data(1825)
        self.subplot.set_xlim(0, 1824)
        self.subplot.tick_params(axis='x', labelsize=11)
        self.subplot.tick_params(axis='y', labelsize=11)
        self.subplot.set_ylim(min_val-dif, max_val+dif)
        self.subplot.plot(x, y, color, lw=1)
        self.plots.draw()
        self.graph_info.config(text = information, fg = color)

    def change_vizualization_mt(self, event):
        if company_data[0] == "ERROR" or company_data[0] == "":
            messagebox.showerror('Python Error', 'Error: The data is not loaded yet!')
            return
        
        self.subplot.clear()
        min_val, max_val, x, y, dif, color, information = self.load_in_historical_data(self.max_time - 1)
        self.subplot.set_xlim(0, self.max_time - 1)
        self.subplot.tick_params(axis='x', labelsize=11)
        self.subplot.tick_params(axis='y', labelsize=11)
        self.subplot.set_ylim(min_val-dif, max_val+dif)
        self.subplot.plot(x, y, color, lw=1)
        self.plots.draw()
        self.graph_info.config(text = information, fg = color)

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
