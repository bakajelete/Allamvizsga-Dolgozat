from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler
import matplotlib.pyplot as plt

import numpy as np

import pandas as pd

import yfinance as yf

from data import *

from datetime import datetime
from dateutil.relativedelta import relativedelta
import time

import Page

class xPage01(Page.Page):
    def __init__(self, root, page_manager):
        Page.Page.__init__(self, root, page_manager)

        self.data = [None]*6

                #_____Control buttons_____
        self.exit = Button(self, text="EXIT")
        self.exit.bind('<Button-1>', self.go_exit)
        
                #_____Imput field for company search_____
        self.companies = ttk.Combobox(self)
        self.companies['values'] = companies_name
        self.companies.bind('<KeyRelease>', self.check_companies)

        self.search = Button(self, text="Search")
        self.search.bind('<Button-1>', self.search_companies)
        
                #_____Grapha abouth the data_____

            #G1
        self.figure1 = Figure(figsize=(4.5, 6), dpi=100)
        
        self.subplot1 = self.figure1.add_subplot(111)
        self.figure1.subplots_adjust(left=0.1, right=0.97, bottom=0.09, top=0.985)
        
        self.plots1 = FigureCanvasTkAgg(self.figure1, self)
        self.plots1.mpl_connect("button_press_event", self.show_company1)
        
            #G2
        self.figure2 = Figure(figsize=(4.5, 6), dpi=100)
        
        self.subplot2 = self.figure2.add_subplot(111)
        self.figure2.subplots_adjust(left=0.1, right=0.97, bottom=0.09, top=0.985)
        
        self.plots2 = FigureCanvasTkAgg(self.figure2, self)
        self.plots2.mpl_connect("button_press_event", self.show_company2)
        
            #G3
        self.figure3 = Figure(figsize=(4.5, 6), dpi=100)
        
        self.subplot3 = self.figure3.add_subplot(111)
        self.figure3.subplots_adjust(left=0.1, right=0.97, bottom=0.09, top=0.985)
        
        self.plots3 = FigureCanvasTkAgg(self.figure3, self)
        self.plots3.mpl_connect("button_press_event", self.show_company3)

            #G4
        self.figure4 = Figure(figsize=(4.5, 6), dpi=100)
        
        self.subplot4 = self.figure4.add_subplot(111)
        self.figure4.subplots_adjust(left=0.1, right=0.97, bottom=0.09, top=0.985)
        
        self.plots4 = FigureCanvasTkAgg(self.figure4, self)
        self.plots4.mpl_connect("button_press_event", self.show_company4)

            #G5
        self.figure5 = Figure(figsize=(4.5, 6), dpi=100)
        
        self.subplot5 = self.figure5.add_subplot(111)
        self.figure5.subplots_adjust(left=0.1, right=0.97, bottom=0.09, top=0.985)
        
        self.plots5 = FigureCanvasTkAgg(self.figure5, self)
        self.plots5.mpl_connect("button_press_event", self.show_company5)

            #G6
        self.figure6 = Figure(figsize=(4.5, 6), dpi=100)
        
        self.subplot6 = self.figure6.add_subplot(111)
        self.figure6.subplots_adjust(left=0.1, right=0.97, bottom=0.09, top=0.985)
        
        self.plots6 = FigureCanvasTkAgg(self.figure6, self)
        self.plots6.mpl_connect("button_press_event", self.show_company6)


                #_____Labels for information of the graph_____

            #L1
        self.graph_info1 = Label(self, text="")

            #L1
        self.graph_info2 = Label(self, text="")

            #L1
        self.graph_info3 = Label(self, text="")

            #L1
        self.graph_info4 = Label(self, text="")
        
            #L1
        self.graph_info5 = Label(self, text="")

            #L1
        self.graph_info6 = Label(self, text="")

    def show_widgets(self):
        self.root.bind("<Configure>", self.resize_window)
        self.resize_window(None)
        self.change_initial_vizualization()
        
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

    def check_input_company(self, company_name):
        
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
        self.check_input_company(company_name)

        if self.company_data[0] == "ERROR":
            messagebox.showerror('Python Error', 'Error: No such company in the data base!')
            return

        self.page_manager.show_page("page02")

    def increased_or_decreased(self, begin, end):
        
        diff = round(begin - end,2)
        diff_percentage = round(abs(diff)*100/begin, 2)
        information = ""
        
        if diff>0:
            information = ": " + str(round(end, 2)) + ", change: -" + str(diff) + " (-" + str(diff_percentage) + "%)"
            return "red", information
        elif diff<0:
            information = ": " + str(round(end, 2)) + ", change: +" + str(abs(diff)) + " (+" + str(diff_percentage) + "%)"
            return "green", information
        else:
            information = ": " + str(round(end, 2)) + ", change: 0 (+0%)"
            return "blue", information
        
    def change_initial_vizualization(self):

        self.subplot1.clear()
        self.data[0] = pd.read_csv("E:/SZAKDOLGOZAT/A_DOLOGZAT/downloads/" + str(max_gain[0][1]) + ".csv")
        last_week = self.data[0][["Date","Open"]].tail(5)
        color, information = self.increased_or_decreased(float(last_week["Open"].head(1)), float(last_week["Open"].tail(1)))
        last_week.plot(x = 'Date', y='Open', color = color, grid = True, ax=self.subplot1)
        self.plots1.draw()
        self.graph_info1.config(text = max_gain[0][1] + information, fg = color)

        self.subplot2.clear()
        self.data[1] = pd.read_csv("E:/SZAKDOLGOZAT/A_DOLOGZAT/downloads/" + str(max_gain[1][1]) + ".csv")
        last_week = self.data[1][["Date", "Open"]].tail(5)
        color, information = self.increased_or_decreased(float(last_week["Open"].head(1)), float(last_week["Open"].tail(1)))
        last_week.plot(x='Date', y='Open', color = color, grid = True, ax=self.subplot2)
        self.plots2.draw()
        self.graph_info2.config(text = max_gain[1][1] + information, fg = color)

        self.subplot3.clear()
        self.data[2] = pd.read_csv("E:/SZAKDOLGOZAT/A_DOLOGZAT/downloads/" + str(max_gain[2][1]) + ".csv")
        last_week = self.data[2][["Date", "Open"]].tail(5)
        color, information = self.increased_or_decreased(float(last_week["Open"].head(1)), float(last_week["Open"].tail(1)))
        last_week.plot(x='Date', y='Open', color = color, grid = True, ax=self.subplot3)
        self.plots3.draw()
        self.graph_info3.config(text = max_gain[2][1] + information, fg = color)

        self.subplot4.clear()
        self.data[3] = pd.read_csv("E:/SZAKDOLGOZAT/A_DOLOGZAT/downloads/" + str(max_lost[0][1]) + ".csv")
        last_week = self.data[3][["Date", "Open"]].tail(5)
        color, information = self.increased_or_decreased(float(last_week["Open"].head(1)), float(last_week["Open"].tail(1)))
        last_week.plot(x='Date', y='Open', color = color, grid = True, ax=self.subplot4)
        self.plots4.draw()
        self.graph_info4.config(text = max_lost[0][1] + information, fg = color)

        self.subplot5.clear()
        self.data[4] = pd.read_csv("E:/SZAKDOLGOZAT/A_DOLOGZAT/downloads/" + str(max_lost[1][1]) + ".csv")
        last_week = self.data[4][["Date", "Open"]].tail(5)
        color, information = self.increased_or_decreased(float(last_week["Open"].head(1)), float(last_week["Open"].tail(1)))
        last_week.plot(x='Date', y='Open', color = color, grid = True, ax=self.subplot5)
        self.plots5.draw()
        self.graph_info5.config(text = max_lost[1][1] + information, fg = color)

        self.subplot6.clear()
        self.data[5] = pd.read_csv("E:/SZAKDOLGOZAT/A_DOLOGZAT/downloads/" + str(max_lost[2][1]) + ".csv")
        last_week = self.data[5][["Date", "Open"]].tail(5)
        color, information = self.increased_or_decreased(float(last_week["Open"].head(1)), float(last_week["Open"].tail(1)))
        last_week.plot(x='Date', y='Open', color = color, grid = True, ax=self.subplot6)
        self.plots6.draw()
        self.graph_info6.config(text = max_lost[2][1] + information, fg = color) 
        
    def change_company_data(self, ticker):
        ok=True
        for companie in companies_info:
            if ticker == companie[1]:
                ok=False
                self.company_data[0] = companie[0]
                self.company_data[1] = companie[1]
                break

        if ok:
            self.company_data[0] = "ERROR"

    def get_DF_val(self, df):
        return df
    
    def show_company1(self, event):
        self.change_company_data(max_gain[0][1])
        
        #print("01 before", id(self.historical_data))
        #self.historical_data = self.data[0].copy(deep=False)
        #self.set_historical_data(self.data[0].copy())
        #print("01 after", id(self.historical_data))

        #print(self.historical_data)
        
        self.page_manager.show_page("page02")

    def show_company2(self, event):
        self.change_company_data(max_gain[1][1])
        self.historical_data = self.data[1]
        
        self.page_manager.show_page("page02")

    def show_company3(self, event):
        self.change_company_data(max_gain[2][1])
        self.historical_data = self.data[2]
        
        self.page_manager.show_page("page02")

    def show_company4(self, event):
        self.change_company_data(max_lost[0][1])
        self.historical_data = self.data[3]
        
        self.page_manager.show_page("page02")
        
    def show_company5(self, event):
        self.change_company_data(max_lost[1][1])
        self.historical_data = self.data[4]
        
        self.page_manager.show_page("page02")

    def show_company6(self, event):
        self.change_company_data(max_lost[2][1])
        self.historical_data = self.data[5]
        
        self.page_manager.show_page("page02")

    def resize_window(self, event):
        self.end = time.time()

        if self.end - self.start < 0.5:
            return

        self.start = time.time()
        
        self.x_len = self.root.winfo_width()
        self.y_len = self.root.winfo_height()
        
        self.box_x = int(self.x_len/35)
        self.box_y = int(self.y_len/18)

        self.x_font = self.box_x * 20/100
        self.y_font = self.box_y * 18/100
        self.label_font = self.box_x * 28/100


                #_____Control buttons_____
        self.exit.place(x=0, y=0, width=3*self.box_x, height=1*self.box_y)
        self.exit.config(font=("Helvetica bold", int(self.label_font)))
        
                #_____Imput field for company search_____
        self.companies.place(x=12*self.box_x, y=0, width=11*self.box_x, height=1*self.box_y)
        self.companies.config(font=("Helvetica bold", int(self.label_font)))
        
        self.search.place(x=23*self.box_x, y=0, width=4*self.box_x, height=1*self.box_y)
        self.search.config(font=("Helvetica bold", int(self.label_font)))
        
            #G1
        self.subplot1.tick_params(axis='x', labelsize = self.x_font)
        self.subplot1.tick_params(axis='y', labelsize = self.y_font)
        
        self.plots1.get_tk_widget().place(x=0, y=2*self.box_y, width=11*self.box_x, height=7*self.box_y)
        
            #G2
        self.subplot2.tick_params(axis='x', labelsize = self.x_font)
        self.subplot2.tick_params(axis='y', labelsize = self.y_font)

        self.plots2.get_tk_widget().place(x=int((self.x_len-11*self.box_x)/2), y=2*self.box_y, width=11*self.box_x, height=7*self.box_y)
        
            #G3
        self.subplot3.tick_params(axis='x', labelsize = self.x_font)
        self.subplot3.tick_params(axis='y', labelsize = self.y_font)
        
        self.plots3.get_tk_widget().place(x=self.x_len-11*self.box_x, y=2*self.box_y, width=11*self.box_x, height=7*self.box_y)

            #G4
        self.subplot4.tick_params(axis='x', labelsize = self.x_font)
        self.subplot4.tick_params(axis='y', labelsize = self.y_font)
        
        self.plots4.get_tk_widget().place(x=0, y=10*self.box_y, width=11*self.box_x, height=7*self.box_y)

            #G5
        self.subplot5.tick_params(axis='x', labelsize = self.x_font)
        self.subplot5.tick_params(axis='y', labelsize = self.y_font)
        
        self.plots5.get_tk_widget().place(x=int((self.x_len-11*self.box_x)/2), y=10*self.box_y, width=11*self.box_x, height=7*self.box_y)

            #G6
        self.subplot6.tick_params(axis='x', labelsize = self.x_font)
        self.subplot6.tick_params(axis='y', labelsize = self.y_font)
        
        self.plots6.get_tk_widget().place(x=self.x_len-11*self.box_x, y=10*self.box_y, width=11*self.box_x, height=7*self.box_y)

            #L1
        self.graph_info1.place(x=0, y=9*self.box_y, width=11*self.box_x, height=1*self.box_y)
        self.graph_info1.config(font=("Helvetica bold", int(self.label_font)))
        
            #L2
        self.graph_info2.place(x=int((self.x_len-11*self.box_x)/2), y=9*self.box_y, width=11*self.box_x, height=1*self.box_y)
        self.graph_info2.config(font=("Helvetica bold", int(self.label_font)))

            #L3
        self.graph_info3.place(x=self.x_len-11*self.box_x, y=9*self.box_y, width=11*self.box_x, height=1*self.box_y)
        self.graph_info3.config(font=("Helvetica bold", int(self.label_font)))

            #L4
        self.graph_info4.place(x=0*self.box_x, y=17*self.box_y, width=11*self.box_x, height=1*self.box_y)
        self.graph_info4.config(font=("Helvetica bold", int(self.label_font)))
        
            #L5
        self.graph_info5.place(x=int((self.x_len-11*self.box_x)/2), y=17*self.box_y, width=11*self.box_x, height=1*self.box_y)
        self.graph_info5.config(font=("Helvetica bold", int(self.label_font)))

            #L6
        self.graph_info6.place(x=self.x_len-11*self.box_x, y=17*self.box_y, width=11*self.box_x, height=1*self.box_y)
        self.graph_info6.config(font=("Helvetica bold", int(self.label_font)))
        
    def next_page(self):
        self.page_manager.show_page("page2")
