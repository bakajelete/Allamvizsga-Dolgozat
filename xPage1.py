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

#import config
import xPage2
import xPage3

class Page1:
    
    def __init__(self, root):
        self.root = root
        self.root.geometry("770x396")

        self.width = 770
        self.height = 396
        self.box_x = 22
        self.box_y = 22
        self.font = 1

                #_____Control buttons_____
        self.exit = Button(root, text="EXIT")
        self.exit.bind('<Button-1>', self.go_exit)
        self.exit.place(x=0*self.box_x, y=0, width=3*self.box_x, height=1*self.box_y)
        
                #_____Imput field for company search_____
        self.companies = ttk.Combobox(root)
        self.companies.set(company_data[0])
        self.companies['values'] = companies_name
        self.companies.bind('<KeyRelease>', self.check_companies)
        self.companies.place(x=12*self.box_x, y=0, width=11*self.box_x, height=1*self.box_y)

        self.search = Button(root, text="Search")
        self.search.bind('<Button-1>', self.search_companies)
        self.search.place(x=23*self.box_x, y=0, width=4*self.box_x, height=1*self.box_y)
        
                #_____Grapha abouth the data_____

            #G1
        self.figure1 = Figure(figsize=(4.5, 6), dpi=100)
        
        self.subplot1 = self.figure1.add_subplot(111)
        self.subplot1.set_ylabel('Value($)', fontsize=self.font)
        self.subplot1.set_xlabel('Time(day)', fontsize=self.font)
        self.subplot1.set_xlim(0, 10)
        self.subplot1.set_ylim(0, 10)
        self.subplot1.tick_params(axis='x', labelsize=3.3)
        self.subplot1.tick_params(axis='y', labelsize=6.6)
        
        self.plots1 = FigureCanvasTkAgg(self.figure1, root)
        self.plots1.get_tk_widget().place(x=0, y=3*self.box_y, width=11*self.box_x, height=7*self.box_y)
        self.plots1.mpl_connect("button_press_event", self.show_company1)

        
            #G2
        self.figure2 = Figure(figsize=(4.5, 6), dpi=100)
        
        self.subplot2 = self.figure2.add_subplot(111)
        self.subplot2.set_ylabel('Value($)', fontsize=self.font)
        self.subplot2.set_xlabel('Time(day)', fontsize=self.font)
        self.subplot2.set_xlim(0, 10)
        self.subplot2.set_ylim(0, 10)
        self.subplot2.tick_params(axis='x', labelsize=3.3)
        self.subplot2.tick_params(axis='y', labelsize=6.6)
        
        self.plots2 = FigureCanvasTkAgg(self.figure2, root)
        self.plots2.get_tk_widget().place(x=12*self.box_x, y=3*self.box_y, width=11*self.box_x, height=7*self.box_y)
        self.plots2.mpl_connect("button_press_event", self.show_company2)
        
            #G3
        self.figure3 = Figure(figsize=(4.5, 6), dpi=100)
        
        self.subplot3 = self.figure3.add_subplot(111)
        self.subplot3.set_ylabel('Value($)', fontsize=self.font)
        self.subplot3.set_xlabel('Time(day)', fontsize=self.font)
        self.subplot3.set_xlim(0, 10)
        self.subplot3.set_ylim(0, 10)
        self.subplot3.tick_params(axis='x', labelsize=3.3)
        self.subplot3.tick_params(axis='y', labelsize=6.6)
        
        self.plots3 = FigureCanvasTkAgg(self.figure3, root)
        self.plots3.get_tk_widget().place(x=24*self.box_x, y=3*self.box_y, width=11*self.box_x, height=7*self.box_y)
        self.plots3.mpl_connect("button_press_event", self.show_company3)

            #G4
        self.figure4 = Figure(figsize=(4.5, 6), dpi=100)
        
        self.subplot4 = self.figure4.add_subplot(111)
        self.subplot4.set_ylabel('Value($)', fontsize=self.font)
        self.subplot4.set_xlabel('Time(day)', fontsize=self.font)
        self.subplot4.set_xlim(0, 10)
        self.subplot4.set_ylim(0, 10)
        self.subplot4.tick_params(axis='x', labelsize=3.3)
        self.subplot4.tick_params(axis='y', labelsize=6.6)
        
        self.plots4 = FigureCanvasTkAgg(self.figure4, root)
        self.plots4.get_tk_widget().place(x=0, y=11*self.box_y, width=11*self.box_x, height=7*self.box_y)
        self.plots4.mpl_connect("button_press_event", self.show_company4)

            #G5
        self.figure5 = Figure(figsize=(4.5, 6), dpi=100)
        
        self.subplot5 = self.figure5.add_subplot(111)
        self.subplot5.set_ylabel('Value($)', fontsize=self.font)
        self.subplot5.set_xlabel('Time(day)', fontsize=self.font)
        self.subplot5.set_xlim(0, 10)
        self.subplot5.set_ylim(0, 10)
        self.subplot5.tick_params(axis='x', labelsize=3.3)
        self.subplot5.tick_params(axis='y', labelsize=6.6)
        
        self.plots5 = FigureCanvasTkAgg(self.figure5, root)
        self.plots5.get_tk_widget().place(x=12*self.box_x, y=11*self.box_y, width=11*self.box_x, height=7*self.box_y)
        self.plots5.mpl_connect("button_press_event", self.show_company5)

            #G6
        self.figure6 = Figure(figsize=(4.5, 6), dpi=100)
        
        self.subplot6 = self.figure6.add_subplot(111)
        self.subplot6.set_ylabel('Value($)', fontsize=self.font)
        self.subplot6.set_xlabel('Time(day)', fontsize=self.font)
        self.subplot6.set_xlim(0, 10)
        self.subplot6.set_ylim(0, 10)
        self.subplot6.tick_params(axis='x', labelsize=3.3)
        self.subplot6.tick_params(axis='y', labelsize=6.6)
        
        self.plots6 = FigureCanvasTkAgg(self.figure6, root)
        self.plots6.get_tk_widget().place(x=24*self.box_x, y=11*self.box_y, width=11*self.box_x, height=7*self.box_y)
        self.plots6.mpl_connect("button_press_event", self.show_company6)


                #_____Labels for information of the graph_____

            #L1
        self.graph_info1 = Label(root, text="")
        self.graph_info1.place(x=0*self.box_x, y=2*self.box_y, width=11*self.box_x, height=1*self.box_y)

            #L1
        self.graph_info2 = Label(root, text="")
        self.graph_info2.place(x=12*self.box_x, y=2*self.box_y, width=11*self.box_x, height=1*self.box_y)

            #L1
        self.graph_info3 = Label(root, text="")
        self.graph_info3.place(x=24*self.box_x, y=2*self.box_y, width=11*self.box_x, height=1*self.box_y)

            #L1
        self.graph_info4 = Label(root, text="")
        self.graph_info4.place(x=0*self.box_x, y=10*self.box_y, width=11*self.box_x, height=1*self.box_y)
        
            #L1
        self.graph_info5 = Label(root, text="")
        self.graph_info5.place(x=12*self.box_x, y=10*self.box_y, width=11*self.box_x, height=1*self.box_y)

            #L1
        self.graph_info6 = Label(root, text="")
        self.graph_info6.place(x=24*self.box_x, y=10*self.box_y, width=11*self.box_x, height=1*self.box_y)

        self.show_max_gain_lost()

    def go_exit(self, event):
        self.root.destroy()
        
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
                company_data[0] = companie[0]
                company_data[1] = companie[1]
                break

        if ok:
            company_data[0] = "ERROR"
        
            
    def search_companies(self, event):
        company_name = str(self.companies.get())
        self.check_input_company(company_name)

        if company_data[0] == "ERROR":
            messagebox.showerror('Python Error', 'Error: No such company in the data base!')
            return
        
        win = Toplevel()
        self.root.withdraw()
        xPage2.Page2(win)
        win.deiconify()

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
        
    def show_max_gain_lost(self):

        self.subplot1.clear()
        data = pd.read_csv("downloads/" + str(max_gain[0][1]) + ".csv")
        last_week = data[["Date", "Open"]].tail(5)
        
        color, information = self.increased_or_decreased(float(last_week["Open"].head(1)), float(last_week["Open"].tail(1)))
        last_week.plot(x='Date', y='Open', color = color, grid = True, ax=self.subplot1)
        self.plots1.draw()
        self.graph_info1.config(text = max_gain[0][1] + information, fg = color)

        self.subplot2.clear()
        data = pd.read_csv("downloads/" + str(max_gain[1][1]) + ".csv")
        last_week = data[["Date", "Open"]].tail(5)
        color, information = self.increased_or_decreased(float(last_week["Open"].head(1)), float(last_week["Open"].tail(1)))
        last_week.plot(x='Date', y='Open', color = color, grid = True, ax=self.subplot2)
        self.plots2.draw()
        self.graph_info2.config(text = max_gain[1][1] + information, fg = color)

        self.subplot3.clear()
        data = pd.read_csv("downloads/" + str(max_gain[2][1]) + ".csv")
        last_week = data[["Date", "Open"]].tail(5)
        color, information = self.increased_or_decreased(float(last_week["Open"].head(1)), float(last_week["Open"].tail(1)))
        last_week.plot(x='Date', y='Open', color = color, grid = True, ax=self.subplot3)
        self.plots3.draw()
        self.graph_info3.config(text = max_gain[2][1] + information, fg = color)

        self.subplot4.clear()
        data = pd.read_csv("downloads/" + str(max_lost[0][1]) + ".csv")
        last_week = data[["Date", "Open"]].tail(5)
        color, information = self.increased_or_decreased(float(last_week["Open"].head(1)), float(last_week["Open"].tail(1)))
        last_week.plot(x='Date', y='Open', color = color, grid = True, ax=self.subplot4)
        self.plots4.draw()
        self.graph_info4.config(text = max_lost[0][1] + information, fg = color)

        self.subplot5.clear()
        data = pd.read_csv("downloads/" + str(max_lost[1][1]) + ".csv")
        last_week = data[["Date", "Open"]].tail(5)
        color, information = self.increased_or_decreased(float(last_week["Open"].head(1)), float(last_week["Open"].tail(1)))
        last_week.plot(x='Date', y='Open', color = color, grid = True, ax=self.subplot5)
        self.plots5.draw()
        self.graph_info5.config(text = max_lost[1][1] + information, fg = color)

        self.subplot6.clear()
        data = pd.read_csv("downloads/" + str(max_lost[2][1]) + ".csv")
        last_week = data[["Date", "Open"]].tail(5)
        color, information = self.increased_or_decreased(float(last_week["Open"].head(1)), float(last_week["Open"].tail(1)))
        last_week.plot(x='Date', y='Open', color = color, grid = True, ax=self.subplot6)
        self.plots6.draw()
        self.graph_info6.config(text = max_lost[2][1] + information, fg = color) 
        
    def change_company_data(self, ticker):
        ok=True
        for companie in companies_info:
            if ticker == companie[1]:
                ok=False
                company_data[0] = companie[0]
                company_data[1] = companie[1]
                break

        if ok:
            company_data[0] = "ERROR"
    
    def show_company1(self, event):
        company_data = self.change_company_data(max_gain[0][1])
        
        win = Toplevel()
        self.root.withdraw()
        xPage2.Page2(win)
        win.deiconify()

    def show_company2(self, event):
        company_data = self.change_company_data(max_gain[1][1])
        
        win = Toplevel()
        self.root.withdraw()
        xPage2.Page2(win)
        win.deiconify()

    def show_company3(self, event):
        company_data = self.change_company_data(max_gain[2][1])
        
        win = Toplevel()
        self.root.withdraw()
        xPage2.Page2(win)
        win.deiconify()

    def show_company4(self, event):
        company_data = self.change_company_data(max_lost[0][1])
        
        win = Toplevel()
        self.root.withdraw()
        xPage2.Page2(win)
        win.deiconify()
        
    def show_company5(self, event):
        company_data = self.change_company_data(max_lost[1][1])
        
        win = Toplevel()
        self.root.withdraw()
        xPage2.Page2(win)
        win.deiconify()

    def show_company6(self, event):
        company_data = self.change_company_data(max_lost[2][1])
        
        win = Toplevel()
        self.root.withdraw()
        xPage2.Page2(win)
        win.deiconify()


def page():    
    root = Tk()
    #root.geometry("770x396")
    Page1(root)
    root.mainloop()

if __name__ == '__main__':
    page()

