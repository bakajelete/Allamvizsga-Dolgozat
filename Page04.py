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

class xPage04(Page.Page):
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
        self.one_week_B50 = Button(self, text="One week B50")
        self.one_week_B50.configure(command = lambda btn=self.one_week_B50: self.change_vizualization_50(self, btn, 5))

        self.one_week_B200 = Button(self, text="One week B200")
        self.one_week_B200.configure(command = lambda btn=self.one_week_B200: self.change_vizualization_200(self, btn, 5))
        
        self.one_month_B50 = Button(self, text="One month B50")
        self.one_month_B50.configure(command = lambda btn=self.one_month_B50: self.change_vizualization_50(self, btn, self.get_days_nr(self.now - relativedelta(months=1))))
        
        self.one_month_B200 = Button(self, text="One month B200")
        self.one_month_B200.configure(command = lambda btn=self.one_month_B200: self.change_vizualization_200(self, btn, self.get_days_nr(self.now - relativedelta(months=1))))
                
        self.three_monts_B50 = Button(self, text="Three monts B50")
        self.three_monts_B50.configure(command = lambda btn=self.three_monts_B50: self.change_vizualization_50(self, btn, self.get_days_nr(self.now - relativedelta(months=3))))
        
        self.three_monts_B200 = Button(self, text="Three monts B200")
        self.three_monts_B200.configure(command = lambda btn=self.three_monts_B200: self.change_vizualization_200(self, btn, self.get_days_nr(self.now - relativedelta(months=3))))
                
        self.six_monts_B50 = Button(self, text="Six monts B50")
        self.six_monts_B50.configure(command = lambda btn=self.six_monts_B50: self.change_vizualization_50(self, btn, self.get_days_nr(self.now - relativedelta(months=6))))
        
        self.six_monts_B200 = Button(self, text="Six monts B200")
        self.six_monts_B200.configure(command = lambda btn=self.six_monts_B200: self.change_vizualization_200(self, btn, self.get_days_nr(self.now - relativedelta(months=6))))
        
        self.one_year_B50 = Button(self, text="One year B50")
        self.one_year_B50.configure(command = lambda btn=self.one_year_B50: self.change_vizualization_50(self, btn, self.get_days_nr(self.now - relativedelta(years=1))))
                   
        self.one_year_B200 = Button(self, text="One year B200")
        self.one_year_B200.configure(command = lambda btn=self.one_year_B200: self.change_vizualization_200(self, btn, self.get_days_nr(self.now - relativedelta(years=1))))
        
        self.three_years_B50 = Button(self, text="Three years B50")
        self.three_years_B50.configure(command = lambda btn=self.three_years_B50: self.change_vizualization_50(self, btn, self.get_days_nr(self.now - relativedelta(years=3))))
        
        self.three_years_B200 = Button(self, text="Three years B200")
        self.three_years_B200.configure(command = lambda btn=self.three_years_B200: self.change_vizualization_200(self, btn, self.get_days_nr(self.now - relativedelta(years=3))))
                   
        self.five_years_B50 = Button(self, text="Five years B50")
        self.five_years_B50.configure(command = lambda btn=self.five_years_B50: self.change_vizualization_50(self,btn, self.get_days_nr(self.now - relativedelta(years=5))))
        
        self.five_years_B200 = Button(self, text="Five years B200")
        self.five_years_B200.configure(command = lambda btn=self.five_years_B200: self.change_vizualization_200(self, btn, self.get_days_nr(self.now - relativedelta(years=5))))
        
        self.max_time_B50 = Button(self, text="Max time B50")
        self.max_time_B50.configure(command = lambda btn=self.max_time_B50: self.change_vizualization_50(self, btn, self.data_time_size))
        
        self.max_time_B200 = Button(self, text="Max time B200")
        self.max_time_B200.configure(command = lambda btn=self.max_time_B200: self.change_vizualization_200(self, btn, self.data_time_size))
                   
                #_____Graph abouth the data_____
        self.figure = Figure(figsize=(4, 7), dpi=100)
        
        self.subplot = self.figure.add_subplot(111)

        self.figure.subplots_adjust(left=0.08, right=0.985, bottom=0.08, top=0.985)
        
        self.plots = FigureCanvasTkAgg(self.figure, self)
        
                #_____Label for information of the graph_____
        self.graph_info = Label(self, text="", anchor="center")
        self.predict_info = Label(self, text="", anchor="center")

                #____Date input for specific time period_____
        self.date_from = Label(self, text="From:", anchor="center")
        self.date_start = DateEntry(self, width= 16, date_pattern='YYYY-MM-DD', background= "magenta3", foreground= "white",bd=2)

        self.date_to = Label(self, text="To:", anchor="center")
        self.date_end = DateEntry(self, width = 16, date_pattern='YYYY-MM-DD', background= "magenta3", foreground= "white",bd=2)

        self.show_B50 = Button(self, text="Show B50", anchor="center")
        self.show_B50.configure(command = lambda btn=self.show_B50: self.change_vizualization_custom_B50(self, btn))
        
        self.show_B200 = Button(self, text="Show B200", anchor="center")
        self.show_B200.configure(command = lambda btn=self.show_B200: self.change_vizualization_custom_B200(self, btn))

    def show_widgets(self):
        self.root.bind("<Configure>", self.resize_window)
        self.companies.set(self.company_data[0])

        self.active_button = self.one_week_B50
        self.active_button.config(bg="sky blue")
        self.resize_window(None)
        self.change_initial_vizualization()
                
    def change_initial_vizualization(self):
        self.historical_data = pd.read_csv("E:/SZAKDOLGOZAT/A_DOLOGZAT/downloads/" + str(self.company_data[1]) + ".csv", index_col = "Date", parse_dates = True)
        self.data_time_size = self.historical_data.shape[0]
        
        self.new_vizualization_50(5)

    def search_companies(self, event):
        company_name = str(self.companies.get())
        self.check_input_company(company_name)

        if self.company_data[0] == "ERROR" or self.company_data[0] == "":
            messagebox.showerror('Python Error', 'Error: No such company in the data base!')
            return

        if self.active_button != None:
            self.active_button.config(bg="SystemButtonFace")
        
        self.active_button = self.one_week_B50
        self.active_button.config(bg="sky blue")
        self.historical_data = pd.read_csv("E:/SZAKDOLGOZAT/A_DOLOGZAT/downloads/" + str(self.company_data[1]) + ".csv", index_col = "Date", parse_dates = True)
        self.data_time_size = self.historical_data.shape[0]
        self.new_vizualization_50(5)

    def calculate_predict_info(self, last_val, last_sma, last_std):

        dist = abs(last_val-last_sma)
        k = dist/last_std

        if k <= 1:
            self.predict_info.config(text = "The next price change is UNPREDICTABLE", fg = 'blue')
            return

        chebyshev_nr = round((1 - 1/k**2)*100,2)

        if last_val < last_sma:
            self.predict_info.config(text = "There is a probability of " + str(chebyshev_nr) + "% for price INCREASE", fg = 'green')
            return

        if last_val > last_sma:
            self.predict_info.config(text = "There is a probability of " + str(chebyshev_nr) + "% for price DROP", fg = 'red')
            return
        
        '''
        chebyshev_nr = last_std**2/(last_val-last_sma)**2

        if chebyshev_nr >= 1:
            self.predict_info.config(text = "The price is likely to NOT CHANGE significantly", fg = 'blue')
            return

        prob = round((1-chebyshev_nr)*100,2)
        # Most akkor mi van??????????????????
        if last_val > last_sma:
            prob = round((1-chebyshev_nr)*100,2)
            if prob >= 50:
                self.predict_info.config(text = "There is a probability of " + str(prob) + "% for price DROP", fg = 'red')
                return
            else:
                self.predict_info.config(text = "There is a probability of " + str(prob) + "% for price INCREASE", fg = 'green')
                return
        else:
            prob = round(chebyshev_nr*100,2)
            if prob >= 50:
                self.predict_info.config(text = "There is a probability of " + str(prob) + "% for price INCREASE", fg = 'green')
                return
            else:
                self.predict_info.config(text = "There is a probability of " + str(prob) + "% for price DROP", fg = 'red')
                return
        '''
        
    def change_vizualization_50(self, event, btn, period):
        if period > self.data_time_size:
            messagebox.showerror('Python Error', 'Error: Not enough data is loaded!')
            return
        
        if self.active_button != None:
            self.active_button.config(bg="SystemButtonFace")
        
        self.active_button = btn
        self.active_button.config(bg="sky blue")
        
        self.new_vizualization_50(period)

    def change_vizualization_200(self, event, btn, period):
        if period > self.data_time_size:
            messagebox.showerror('Python Error', 'Error: Not enough data is loaded!')
            return

        if self.active_button != None:
            self.active_button.config(bg="SystemButtonFace")
        
        self.active_button = btn
        self.active_button.config(bg="sky blue")
        
        self.new_vizualization_200(period)
        
    def new_vizualization_50(self, period):
        
        self.subplot.clear()
        time_period = self.historical_data[["Open", "SMA50", "R_STD50"]].tail(period)
        time_period.index = pd.to_datetime(time_period.index, format = '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
        
        time_period['STD_up2'] = time_period.apply(lambda x: x['SMA50'] + 2 * x['R_STD50'], axis=1)
        time_period['STD_up1'] = time_period.apply(lambda x: x['SMA50'] + x['R_STD50'], axis=1)
        time_period['STD_lo1'] = time_period.apply(lambda x: x['SMA50'] - x['R_STD50'], axis=1)
        time_period['STD_lo2'] = time_period.apply(lambda x: x['SMA50'] - 2 * x['R_STD50'], axis=1)

        time_period['STD_lo1'] = time_period['STD_lo1'].apply(lambda x: x if x > 0 else 0)
        time_period['STD_lo2'] = time_period['STD_lo2'].apply(lambda x: x if x > 0 else 0)
        
        
        color, information = self.increased_or_decreased(float(time_period["Open"].head(1)), float(time_period["Open"].tail(1)))
        colors = [color] + ["blue", "greenyellow", "limegreen", "orangered", "maroon"]
        time_period.plot(use_index=True, y=["Open", "SMA50","STD_up2", "STD_up1", "STD_lo1", "STD_lo2"], color = colors, grid = True, ax=self.subplot)
        self.plots.draw()
        
        self.graph_info.config(text = self.company_data[1] + information, fg = color)

        last_val = time_period['Open'].tail(1).values[0]
        last_sma = time_period['SMA50'].tail(1).values[0]
        last_std = time_period['R_STD50'].tail(1).values[0]
        self.calculate_predict_info(last_val, last_sma, last_std)

    def new_vizualization_200(self, period):
        
        self.subplot.clear()
        time_period = self.historical_data[["Open", "SMA200", "R_STD200"]].tail(period)
        time_period.index = pd.to_datetime(time_period.index, format = '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
        
        time_period['STD_up2'] = time_period.apply(lambda x: x['SMA200'] + 2 * x['R_STD200'], axis=1)
        time_period['STD_up1'] = time_period.apply(lambda x: x['SMA200'] + x['R_STD200'], axis=1)
        time_period['STD_lo1'] = time_period.apply(lambda x: x['SMA200'] - x['R_STD200'], axis=1)
        time_period['STD_lo2'] = time_period.apply(lambda x: x['SMA200'] - 2 * x['R_STD200'], axis=1)

        time_period['STD_lo1'] = time_period['STD_lo1'].apply(lambda x: x if x > 0 else 0)
        time_period['STD_lo2'] = time_period['STD_lo2'].apply(lambda x: x if x > 0 else 0)

        color, information = self.increased_or_decreased(float(time_period["Open"].head(1)), float(time_period["Open"].tail(1)))
        colors = [color] + ["blue", "greenyellow", "limegreen", "orangered", "maroon"]
        time_period.plot(use_index=True, y=["Open", "SMA200", "STD_up2", "STD_up1", "STD_lo1", "STD_lo2"], color = colors, grid = True, ax=self.subplot)
        self.plots.draw()
        
        self.graph_info.config(text = self.company_data[1] + information, fg = color)

        last_val = time_period['Open'].tail(1).values[0]
        last_sma = time_period['SMA200'].tail(1).values[0]
        last_std = time_period['R_STD200'].tail(1).values[0]
        self.calculate_predict_info(last_val, last_sma, last_std)

    def change_vizualization_custom_B50(self, event, btn):
        start = self.date_start.get_date()
        end = self.date_end.get_date()

        if start > end:
            messagebox.showerror('Python Error', 'Error: the given dates are incorrect!')
            return

        if end > self.now:
            messagebox.showerror('Python Error', 'Error: the given dates are incorrect!')
            return

        custom_period = self.historical_data[["Open", "SMA50", "R_STD50"]][(self.historical_data.index >= np.datetime64(start)) & (self.historical_data.index <= np.datetime64(end))]
        if custom_period.shape[0] == 0:
            messagebox.showerror('Python Error', 'Error: the selected period contains no data!')
            return
        
        if self.active_button != None:
            self.active_button.config(bg="SystemButtonFace")
        
        self.active_button = btn
        self.active_button.config(bg="sky blue")

        self.subplot.clear()
        custom_period.index = pd.to_datetime(custom_period.index, format = '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
        
        custom_period['STD_up2'] = custom_period.apply(lambda x: x['SMA50'] + 2 * x['R_STD50'], axis=1)
        custom_period['STD_up1'] = custom_period.apply(lambda x: x['SMA50'] + x['R_STD50'], axis=1)
        custom_period['STD_lo1'] = custom_period.apply(lambda x: x['SMA50'] - x['R_STD50'], axis=1)
        custom_period['STD_lo2'] = custom_period.apply(lambda x: x['SMA50'] - 2 * x['R_STD50'], axis=1)

        custom_period['STD_lo1'] = custom_period['STD_lo1'].apply(lambda x: x if x > 0 else 0)
        custom_period['STD_lo2'] = custom_period['STD_lo2'].apply(lambda x: x if x > 0 else 0)
        
        color, information = self.increased_or_decreased(float(custom_period["Open"].head(1)), float(custom_period["Open"].tail(1)))
        colors = [color] + ["blue", "greenyellow", "limegreen", "orangered", "maroon"]
        custom_period.plot(use_index=True, y=["Open", "SMA50","STD_up2", "STD_up1", "STD_lo1", "STD_lo2"], color = colors, grid = True, ax=self.subplot)
        self.plots.draw()
        
        self.graph_info.config(text = self.company_data[1] + information, fg = color)

        last_val = time_period['Open'].tail(1).values[0]
        last_sma = time_period['SMA50'].tail(1).values[0]
        last_std = time_period['R_STD50'].tail(1).values[0]
        self.calculate_predict_info(last_val, last_sma, last_std)
        
    def change_vizualization_custom_B200(self, event, btn):
        start = self.date_start.get_date()
        end = self.date_end.get_date()

        if start > end:
            messagebox.showerror('Python Error', 'Error: the given dates are incorrect!')
            return

        if end > self.now:
            messagebox.showerror('Python Error', 'Error: the given dates are incorrect!')
            return

        custom_period = self.historical_data[["Open", "SMA200", "R_STD200"]][(self.historical_data.index >= np.datetime64(start)) & (self.historical_data.index <= np.datetime64(end))]
        if custom_period.shape[0] == 0:
            messagebox.showerror('Python Error', 'Error: the selected period contains no data!')
            return
        
        if self.active_button != None:
            self.active_button.config(bg="SystemButtonFace")
        
        self.active_button = btn
        self.active_button.config(bg="sky blue")

        self.subplot.clear()
        custom_period.index = pd.to_datetime(custom_period.index, format = '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
        
        custom_period['STD_up2'] = custom_period.apply(lambda x: x['SMA200'] + 2 * x['R_STD200'], axis=1)
        custom_period['STD_up1'] = custom_period.apply(lambda x: x['SMA200'] + x['R_STD200'], axis=1)
        custom_period['STD_lo1'] = custom_period.apply(lambda x: x['SMA200'] - x['R_STD200'], axis=1)
        custom_period['STD_lo2'] = custom_period.apply(lambda x: x['SMA200'] - 2 * x['R_STD200'], axis=1)

        custom_period['STD_lo1'] = custom_period['STD_lo1'].apply(lambda x: x if x > 0 else 0)
        custom_period['STD_lo2'] = custom_period['STD_lo2'].apply(lambda x: x if x > 0 else 0)
        
        color, information = self.increased_or_decreased(float(custom_period["Open"].head(1)), float(custom_period["Open"].tail(1)))
        colors = [color] + ["blue", "greenyellow", "limegreen", "orangered", "maroon"]
        custom_period.plot(use_index=True, y=["Open", "SMA200", "STD_up2", "STD_up1", "STD_lo1", "STD_lo2"], color = colors, grid = True, ax=self.subplot)
        self.plots.draw()
        
        self.graph_info.config(text = self.company_data[1] + information, fg = color)

        last_val = time_period['Open'].tail(1).values[0]
        last_sma = time_period['SMA200'].tail(1).values[0]
        last_std = time_period['R_STD200'].tail(1).values[0]
        self.calculate_predict_info(last_val, last_sma, last_std)

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
        self.one_week_B50.place(x=0, y=2*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.one_week_B50.config(font=("Helvetica bold", int(self.x_font)))
        
        self.one_week_B200.place(x=self.x_len-4*self.box_x, y=2*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.one_week_B200.config(font=("Helvetica bold", int(self.x_font)))
        
        self.one_month_B50.place(x=0, y=4*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.one_month_B50.config(font=("Helvetica bold", int(self.x_font)))
        
        self.one_month_B200.place(x=self.x_len-4*self.box_x, y=4*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.one_month_B200.config(font=("Helvetica bold", int(self.x_font)))
        
        self.three_monts_B50.place(x=0, y=6*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.three_monts_B50.config(font=("Helvetica bold", int(self.x_font)))
        
        self.three_monts_B200.place(x=self.x_len-4*self.box_x, y=6*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.three_monts_B200.config(font=("Helvetica bold", int(self.x_font)))

        self.six_monts_B50.place(x=0, y=8*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.six_monts_B50.config(font=("Helvetica bold", int(self.x_font)))
        
        self.six_monts_B200.place(x=self.x_len-4*self.box_x, y=8*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.six_monts_B200.config(font=("Helvetica bold", int(self.x_font)))

        self.one_year_B50.place(x=0, y=10*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.one_year_B50.config(font=("Helvetica bold", int(self.x_font)))
        
        self.one_year_B200.place(x=self.x_len-4*self.box_x, y=10*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.one_year_B200.config(font=("Helvetica bold", int(self.x_font)))

        self.three_years_B50.place(x=0, y=12*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.three_years_B50.config(font=("Helvetica bold", int(self.x_font)))
        
        self.three_years_B200.place(x=self.x_len-4*self.box_x, y=12*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.three_years_B200.config(font=("Helvetica bold", int(self.x_font)))

        self.five_years_B50.place(x=0, y=14*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.five_years_B50.config(font=("Helvetica bold", int(self.x_font)))
        
        self.five_years_B200.place(x=self.x_len-4*self.box_x, y=14*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.five_years_B200.config(font=("Helvetica bold", int(self.x_font)))

        self.max_time_B50.place(x=0, y=16*self.box_y, width = 4*self.box_x, height=1*self.box_y)
        self.max_time_B50.config(font=("Helvetica bold", int(self.x_font)))
        
        self.max_time_B200.place(x=self.x_len-4*self.box_x, y=16*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.max_time_B200.config(font=("Helvetica bold", int(self.x_font)))

            #_____Graph abouth the data_____
        self.subplot.tick_params(axis='x', labelsize = self.x_font)
        self.subplot.tick_params(axis='y', labelsize = self.y_font)

        self.plots.get_tk_widget().place(x=4*self.box_x, y=2*self.box_y, width=28*self.box_x, height=15*self.box_y)

        #_____Label for information of the graph_____
        self.graph_info.place(x=4*self.box_x, y=17*self.box_y, width=14*self.box_x, height=1*self.box_y)
        self.graph_info.config(font=("Helvetica bold", int(self.x_font)))

        self.predict_info.place(x=18*self.box_x, y=17*self.box_y, width=14*self.box_x, height=1*self.box_y)
        self.predict_info.config(font=("Helvetica bold", int(self.x_font)))

                #____Date input for specific time period_____
        self.date_from.place(x=6*self.box_x, y=1*self.box_y, width=2*self.box_x, height=1*self.box_y)
        self.date_from.config(font=("Helvetica bold", int(self.x_font)))
        
        self.date_start.place(x=8*self.box_x, y=1*self.box_y, width=5*self.box_x, height=1*self.box_y)
        self.date_start.config(font=("Helvetica bold", int(self.x_font)))

        self.date_to.place(x=13*self.box_x, y=1*self.box_y, width=2*self.box_x, height=1*self.box_y)
        self.date_to.config(font=("Helvetica bold", int(self.x_font)))
        
        self.date_end.place(x=15*self.box_x, y=1*self.box_y, width=5*self.box_x, height=1*self.box_y)
        self.date_end.config(font=("Helvetica bold", int(self.x_font)))

        self.show_B50.place(x=21*self.box_x, y=1*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.show_B50.config(font=("Helvetica bold", int(self.x_font)))
        
        self.show_B200.place(x=26*self.box_x, y=1*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.show_B200.config(font=("Helvetica bold", int(self.x_font)))

def page():    
    root = Tk()
    #root.geometry("770x396")
    Page4(root)
    root.mainloop()

if __name__ == '__main__':
    page()
