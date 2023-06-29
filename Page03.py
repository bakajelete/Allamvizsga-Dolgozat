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

from datetime import datetime
from dateutil.relativedelta import relativedelta
import time

import Page

class xPage03(Page.Page):
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
        
        self.one_week_changes = Button(self, text="One week changes", anchor="center")
        self.one_week_changes.configure(command = lambda btn=self.one_week_changes: self.change_vizualization_changes(self, btn, 5))
        
        self.one_month = Button(self, text="One month", anchor="center")
        self.one_month.configure(command = lambda btn=self.one_month: self.change_vizualization(self, btn, self.get_days_nr(self.now - relativedelta(months=1))))

        self.one_month_changes = Button(self, text="One month changes",anchor="center")
        self.one_month_changes.configure(command = lambda btn=self.one_month_changes: self.change_vizualization_changes(self, btn, self.get_days_nr(self.now - relativedelta(months=1))))

        self.three_months = Button(self, text="Three months", anchor="center")
        self.three_months.configure(command = lambda btn=self.three_months: self.change_vizualization(self, btn, self.get_days_nr(self.now - relativedelta(months=3))))

        self.three_months_changes = Button(self, text="  Three months changes", anchor="center")
        self.three_months_changes.configure(command = lambda btn=self.three_months_changes: self.change_vizualization_changes(self, btn, self.get_days_nr(self.now - relativedelta(months=3))))
        
        self.six_months = Button(self, text="Six months", anchor="center")
        self.six_months.configure(command = lambda btn=self.six_months: self.change_vizualization(self, btn, self.get_days_nr(self.now - relativedelta(months=6))))
        
        self.six_months_changes = Button(self, text="Six months changes", anchor="center")
        self.six_months_changes.configure(command = lambda btn=self.six_months_changes: self.change_vizualization_changes(self, btn, self.get_days_nr(self.now - relativedelta(months=6))))
        
        self.one_year = Button(self, text="One year", anchor="center")
        self.one_year.configure(command = lambda btn=self.one_year: self.change_vizualization(self, btn, self.get_days_nr(self.now - relativedelta(years=1))))
        
        self.one_year_changes = Button(self, text="One year changes", anchor="center")
        self.one_year_changes.configure(command = lambda btn=self.one_year_changes: self.change_vizualization_changes(self, btn, self.get_days_nr(self.now - relativedelta(years=1))))
        
        self.three_years = Button(self, text="Three years", anchor="center")
        self.three_years.configure(command = lambda btn=self.three_years: self.change_vizualization(self, btn, self.get_days_nr(self.now - relativedelta(years=3))))

        self.three_years_changes = Button(self, text="Three years changes", anchor="center")
        self.three_years_changes.configure(command = lambda btn=self.three_years_changes: self.change_vizualization_changes(self, btn, self.get_days_nr(self.now - relativedelta(years=3))))
        
        self.five_years = Button(self, text="Five years", anchor="center")      
        self.five_years.configure(command = lambda btn=self.five_years: self.change_vizualization(self, btn, self.get_days_nr(self.now - relativedelta(years=5))))

        self.five_years_changes = Button(self, text="Five years  changes", anchor="center")
        self.five_years_changes.configure(command = lambda btn=self.five_years_changes: self.change_vizualization_changes(self, btn, self.get_days_nr(self.now - relativedelta(years=5))))
        
        self.max_time = Button(self, text="Max time", anchor="center")
        self.max_time.configure(command = lambda btn=self.max_time: self.change_vizualization(self, btn, self.data_time_size))
        
        self.max_time_changes = Button(self, text="Max time  changes", anchor="center")
        self.max_time_changes.configure(command = lambda btn=self.max_time_changes: self.change_vizualization_changes(self, btn, self.data_time_size))

                #_____Graph abouth the data_____
        self.figure = Figure(figsize=(4, 7), dpi=100)
        
        self.subplot = self.figure.add_subplot(111)
        
        self.figure.subplots_adjust(left=0.08, right=0.985, bottom=0.08, top=0.985)
    
        self.canvas = FigureCanvasTkAgg(self.figure, self)

                #_____Label for information of the graph_____
        self.graph_info = Label(self, text="", anchor="center")

                #____Date input for specific time period_____
        self.date_from = Label(self, text="From:", anchor="center")
        self.date_start = DateEntry(self, popanchor="n", date_pattern='YYYY-MM-DD') #, width= 16, date_pattern='YYYY-MM-DD', background= "magenta3", foreground= "white",bd=2)
        

        self.date_to = Label(self, text="To:", anchor="center")
        self.date_end = DateEntry(self, calendar_position='above', date_pattern='YYYY-MM-DD') #, width = 16, date_pattern='YYYY-MM-DD', background= "magenta3", foreground= "white",bd=2)

        self.show_all = Button(self, text="Show all", anchor="center")
        self.show_all.configure(command = lambda btn=self.show_all: self.change_vizualization_custom(self, btn))

        self.show_change = Button(self, text="Show changes", anchor="center")
        self.show_change.configure(command = lambda btn=self.show_change: self.change_vizualization_custom_changes(self, btn))

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

    def on_resize(event):
        scatter.set_sizes([0.05 * event.inches.width**2])

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

    def change_vizualization_changes(self, event, btn, period):
        if period > self.data_time_size:
            messagebox.showerror('Python Error', 'Error: Not enough data is loaded!')
            return

        if self.active_button != None:
            self.active_button.config(bg="SystemButtonFace")

        self.active_button = btn
        self.active_button.config(bg="sky blue")
        
        self.new_vizualization_changes(period)
    
    def new_vizualization(self, period):
        
        self.subplot.clear()
        time_period = self.historical_data[["Open","High","Low","Close"]].tail(period)
        time_period.index = pd.to_datetime(time_period.index, format = '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')

        color, information = self.increased_or_decreased(float(time_period["Open"].head(1)), float(time_period["Open"].tail(1)))
        time_period.plot(use_index=True, y=["Open","High","Low","Close"], color = ['green', 'blue', 'red', 'yellow'], grid = True, ax=self.subplot)
        
        self.canvas.draw()
        self.graph_info.config(text = self.company_data[1] + information, fg = color)

    def new_vizualization_changes(self, period):
        
        self.subplot.clear()

        percentage_changes = self.historical_data['Open'].tail(period).pct_change().dropna().apply(lambda x: x*100)
        time_period = self.historical_data[["Open"]].tail(period)
        color, information = self.increased_or_decreased(float(time_period['Open'].head(1)), float(time_period['Open'].tail(1)))
        
        n = len(percentage_changes)
        hist = [0]*200
        for val in percentage_changes:
            if val>100:
                val = 99
            if val < -100:
                val = -100
            hist[int(val)+100]+=1

        hist = [val*100/n for val in hist]

        self.subplot.grid(visible = True)
        self.subplot.bar(np.linspace(-15,15,31), hist[85:116])
        
        self.subplot.set_xlabel('Change percentages')
        self.subplot.set_ylabel('Distribution of changes')
        
        self.canvas.draw()

        self.graph_info.config(text = self.company_data[1] + information, fg = color)

    def change_vizualization_custom(self, event, btn):        
        start = self.date_start.get_date()
        end = self.date_end.get_date()

        if start > end:
            messagebox.showerror('Python Error', 'Error: the given dates are incorrect!')
            return

        if end > self.now:
            messagebox.showerror('Python Error', 'Error: the given dates are incorrect!')
            return
        
        custom_period = self.historical_data[["Open","High","Low","Close"]][(self.historical_data.index >= np.datetime64(start)) & (self.historical_data.index <= np.datetime64(end))]
        if custom_period.shape[0] == 0:
            messagebox.showerror('Python Error', 'Error: the selected period contains no data!')
            return
        
        if self.active_button != None:
            self.active_button.config(bg="SystemButtonFace")

        self.active_button = btn
        self.active_button.config(bg="sky blue")

        self.subplot.clear()

        custom_period.index = pd.to_datetime(custom_period.index, format = '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
            
        color, information = self.increased_or_decreased(float(custom_period["Open"].head(1)), float(custom_period["Open"].tail(1)))
        custom_period.plot(use_index=True, y=["Open","High","Low","Close"], color = ['green', 'blue', 'red', 'yellow'], grid = True, ax=self.subplot)
        self.canvas.draw()
        self.graph_info.config(text = self.company_data[1] + information, fg = color)

    def change_vizualization_custom_changes(self, event, btn):
        start = self.date_start.get_date()
        end = self.date_end.get_date()

        if start > end:
            messagebox.showerror('Python Error', 'Error: the given dates are incorrect!')
            return

        if end > self.now:
            messagebox.showerror('Python Error', 'Error: the given dates are incorrect!')
            return

        percentage_changes = self.historical_data['Open'][(self.historical_data.index >= np.datetime64(start)) & (self.historical_data.index <= np.datetime64(end))].pct_change().dropna().apply(lambda x: x*100)
        if percentage_changes.shape[0] == 0:
            messagebox.showerror('Python Error', 'Error: the selected period contains no data!')
            return
        
        if self.active_button != None:
            self.active_button.config(bg="SystemButtonFace")

        self.active_button = btn
        self.active_button.config(bg="sky blue")

        self.subplot.clear()

        time_period = self.historical_data[["Open"]][(self.historical_data.index >= np.datetime64(start)) & (self.historical_data.index <= np.datetime64(end))]
        color, information = self.increased_or_decreased(float(time_period['Open'].head(1)), float(time_period['Open'].tail(1)))
        
        n = len(percentage_changes)
        hist = [0]*200
        for val in percentage_changes:
            if val>100:
                val = 99
            if val < -100:
                val = -100
            hist[int(val)+100]+=1

        hist = [val*100/n for val in hist]

        self.subplot.grid(visible = True)
        self.subplot.bar(np.linspace(-15,15,31), hist[85:116])

        self.subplot.set_xlabel('Change percentages')
        self.subplot.set_ylabel('Distribution of changes')
        
        self.canvas.draw()

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
        
        self.one_week_changes.place(x=self.x_len-4*self.box_x, y=2*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.one_week_changes.config(font=("Helvetica bold", int(self.x_font)))
        
        self.one_month.place(x=0, y=4*self.box_y, width=3*self.box_x, height=1*self.box_y)
        self.one_month.config(font=("Helvetica bold", int(self.x_font)))
        
        self.one_month_changes.place(x=self.x_len-4*self.box_x, y=4*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.one_month_changes.config(font=("Helvetica bold", int(self.x_font)))

        self.three_months.place(x=0, y=6*self.box_y, width=3*self.box_x, height=1*self.box_y)
        self.three_months.config(font=("Helvetica bold", int(self.x_font)))
        
        self.three_months_changes.place(x=self.x_len-4*self.box_x, y=6*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.three_months_changes.config(font=("Helvetica bold", int(self.x_font)))
        
        self.six_months.place(x=0, y=8*self.box_y, width=3*self.box_x, height=1*self.box_y)
        self.six_months.config(font=("Helvetica bold", int(self.x_font)))
        
        self.six_months_changes.place(x=self.x_len-4*self.box_x, y=8*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.six_months_changes.config(font=("Helvetica bold", int(self.x_font)))
        
        self.one_year.place(x=0, y=10*self.box_y, width=3*self.box_x, height=1*self.box_y)
        self.one_year.config(font=("Helvetica bold", int(self.x_font)))
        
        self.one_year_changes.place(x=self.x_len-4*self.box_x, y=10*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.one_year_changes.config(font=("Helvetica bold", int(self.x_font)))

        self.three_years.place(x=0, y=12*self.box_y, width=3*self.box_x, height=1*self.box_y)
        self.three_years.config(font=("Helvetica bold", int(self.x_font)))
        
        self.three_years_changes.place(x=self.x_len-4*self.box_x, y=12*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.three_years_changes.config(font=("Helvetica bold", int(self.x_font)))
        
        self.five_years.place(x=0, y=14*self.box_y, width=3*self.box_x, height=1*self.box_y)        
        self.five_years.config(font=("Helvetica bold", int(self.x_font)))
        
        self.five_years_changes.place(x=self.x_len-4*self.box_x, y=14*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.five_years_changes.config(font=("Helvetica bold", int(self.x_font)))
        
        self.max_time.place(x=0, y=16*self.box_y, width=3*self.box_x, height=1*self.box_y)
        self.max_time.config(font=("Helvetica bold", int(self.x_font)))

        self.max_time_changes.place(x=self.x_len-4*self.box_x, y=16*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.max_time_changes.config(font=("Helvetica bold", int(self.x_font)))
        
                #_____Graph abouth the data_____
        
        self.subplot.tick_params(axis='x', labelsize = self.x_font)
        self.subplot.tick_params(axis='y', labelsize = self.y_font)
        self.subplot.xaxis.label.set_fontsize(int(self.x_font))
        self.subplot.yaxis.label.set_fontsize(int(self.x_font))
        
        self.canvas.get_tk_widget().place(x=3*self.box_x, y=2*self.box_y, width=29*self.box_x, height=15*self.box_y)

                #_____Label for information of the graph_____
        self.graph_info.place(x=3*self.box_x, y=17*self.box_y, width=29*self.box_x, height=1*self.box_y)
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

        self.show_all.place(x=21*self.box_x, y=1*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.show_all.config(font=("Helvetica bold", int(self.x_font)))
        
        self.show_change.place(x=26*self.box_x, y=1*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.show_change.config(font=("Helvetica bold", int(self.x_font)))


        
    
def page():    
    root = Tk()
    #root.geometry("770x396")
    Page3(root)
    root.mainloop()

if __name__ == '__main__':
    page()
