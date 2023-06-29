from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from tkcalendar import DateEntry

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.colors as colors

import numpy as np

from math import atan 

import pandas as pd

import yfinance as yf

import warnings

from data import *

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time

from sklearn.metrics import mean_squared_error, r2_score

import Page

class xPage08(Page.Page):
    def __init__(self, root, page_manager):
        Page.Page.__init__(self, root, page_manager)

        self.time_period = None

               #_____Control buttons_____
        self.exit = Button(self, text="EXIT")
        self.exit.bind('<Button-1>', self.go_exit)

        self.back = Button(self, text="BACK", command = lambda: self.go_back(self, 'page02'))
                
                #_____Imput field for company search_____
        self.companies = ttk.Combobox(self)
        self.companies['values'] = companies_name
        self.companies.bind('<KeyRelease>', self.check_companies)

        self.search = Button(self, text="Search")
        self.search.bind('<Button-1>', self.search_companies)

                #____Date input for specific time period_____
        self.date_from = Label(self, text="From:", anchor="center")
        self.date_start = DateEntry(self, popanchor="n", date_pattern='YYYY-MM-DD')
    
        self.date_to = Label(self, text="To:", anchor="center")
        self.date_end = DateEntry(self, calendar_position='above', date_pattern='YYYY-MM-DD')

        self.show_open = Button(self, text="Show", anchor="center")
        self.show_open.configure(command = lambda btn=self.show_open: self.change_vizualization_custom(self, btn))

                #_____Buttons for certain intervall visualization_____ 
        self.one_week = Button(self, text="One week", anchor="center")
        self.one_week.configure(command = lambda btn=self.one_week: self.change_vizualization(self, btn, 5))
        
        self.one_month = Button(self, text="One month", anchor="center")
        self.one_month.configure(command = lambda btn=self.one_month: self.change_vizualization(self, btn, self.get_days_nr(self.now - relativedelta(months=1))))
        
        self.three_months = Button(self, text="Three months", anchor="center")
        self.three_months.configure(command = lambda btn=self.three_months: self.change_vizualization(self, btn, self.get_days_nr(self.now - relativedelta(months=3))))
        
        self.six_months = Button(self, text="Six months", anchor="center")
        self.six_months.configure(command = lambda btn=self.six_months: self.change_vizualization(self, btn, self.get_days_nr(self.now - relativedelta(months=6))))

        self.one_year = Button(self, text="One year", anchor="center")
        self.one_year.configure(command = lambda btn=self.one_year: self.change_vizualization(self, btn, self.get_days_nr(self.now - relativedelta(years=1))))
        
        self.three_years = Button(self, text="Three years", anchor="center")
        self.three_years.configure(command = lambda btn=self.three_years: self.change_vizualization(self, btn, self.get_days_nr(self.now - relativedelta(years=3))))

        self.five_years = Button(self, text="Five years", anchor="center")      
        self.five_years.configure(command = lambda btn=self.five_years: self.change_vizualization(self, btn, self.get_days_nr(self.now - relativedelta(years=5))))
        
        self.max_time = Button(self, text="Max time", anchor="center")
        self.max_time.configure(command = lambda btn=self.max_time: self.change_vizualization(self, btn, self.data_time_size))

                #_____Prediction info labels_____
        self.degree = Label(self, text="Degree of approximator:", anchor="center")
        self.degree_input = Entry(self)
        self.degree_input.bind('<Key>', self.validate_numeric_input)

        self.predict_delta = Label(self, text="Prediction delta:", anchor="center")
        self.predict_delta_input = Entry(self)
        self.predict_delta_input.bind('<Key>', self.validate_numeric_input)

        self.calculate_polynom = Button(self, text="Calculate pred space:", anchor="center")
        self.calculate_polynom.bind('<Button-1>', self.calc_polynomial_regression)

        self.mse = Label(self, text="Mean squared error:", anchor="center")
        self.mse_info = Label(self, text="", anchor="center")

        self.r2 = Label(self, text="R2 score:", anchor="center")
        self.r2_info = Label(self, text="", anchor="center")

        self.prediction = Label(self, text="Average prediction:", anchor="center")
        self.prediction_info = Label(self, text="", anchor="center")
        
                #_____Graph abouth the data_____
        self.figure = Figure(figsize=(4, 7), dpi=100)
        
        self.subplot = self.figure.add_subplot(111)

        self.figure.subplots_adjust(left=0.08, right=0.985, bottom=0.08, top=0.985)
        
        self.canvas = FigureCanvasTkAgg(self.figure, self)

                #_____Label for information of the graph_____
        self.graph_info = Label(self, text="", anchor="center")

    def show_widgets(self):
        self.root.bind("<Configure>", self.resize_window)

        self.companies.set(self.company_data[0])
        
        self.degree_input.delete(0, END)
        self.degree_input.insert(0, '15')

        self.predict_delta_input.delete(0, END)
        self.predict_delta_input.insert(0, '3')
        
        self.active_button = self.one_week
        self.active_button.config(bg="sky blue")
        self.resize_window(None)

        self.change_initial_vizualization()
        self.all_companies_info = pd.read_csv("E:/SZAKDOLGOZAT/A_DOLOGZAT/downloads/0xALL_COMPANIES.csv")###
        
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
                self.company_data[0] = companie[0]
                self.company_data[1] = companie[1]
                break

        if ok:
            self.company_data[0] = "ERROR"

    def validate_numeric_input(self, event):
        key = event.char
        
        if not key.isdigit() and key != '\b':
            return 'break'
            
    def search_companies(self, event):
        company_name = str(self.companies.get())

        self.ticker = self.searh_for_ticker(company_name)

        if self.company_data[0] == "ERROR":
            messagebox.showerror('Python Error', 'Error: No such company in the data base!')
            return

        if self.active_button != None:
            self.active_button.config(bg="SystemButtonFace")
        
        self.active_button = self.one_week
        self.active_button.config(bg="sky blue")
        
        self.historical_data = pd.read_csv("E:/SZAKDOLGOZAT/A_DOLOGZAT/downloads/" + str(self.company_data[1]) + ".csv", index_col = "Date", parse_dates = True)
        self.data_time_size = self.historical_data.shape[0]
        self.new_vizualization_open(5)
        
    def change_initial_vizualization(self):

        self.historical_data = pd.read_csv("E:/SZAKDOLGOZAT/A_DOLOGZAT/downloads/" + str(self.company_data[1]) + ".csv", index_col = "Date", parse_dates = True)

        self.data_time_size = self.historical_data.shape[0]
        self.new_vizualization_open(5)

    def change_vizualization(self, event, btn, period):
        if period > self.data_time_size:
            messagebox.showerror('Python Error', 'Error: Not enough data is loaded!')
            return

        if self.active_button != None:
            self.active_button.config(bg="SystemButtonFace")
        
        self.active_button = btn
        self.active_button.config(bg="sky blue")
   
        self.new_vizualization_open(period)

    def new_vizualization_open(self, period):
        
        self.subplot.clear()
        self.time_period = self.historical_data[["Open"]].tail(period)
        self.time_period.index = pd.to_datetime(self.time_period.index, format = '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
        
        color, information = self.increased_or_decreased(self.time_period['Open'].head(1).values[0], self.time_period['Open'].tail(1).values[0])
        self.time_period.plot(use_index=True, y='Open', color = color, grid = True, ax=self.subplot)
        self.canvas.draw()
        self.graph_info.config(text = self.company_data[1] + information, fg = color)

    def change_vizualization_custom(self, event, btn):

        if len(self.historical_data) == 0:
            messagebox.showerror('Python Error', 'Error: data is not loaded yet!')
            return
            
        start = self.date_start.get_date()
        end = self.date_end.get_date()

        if start > end:
            messagebox.showerror('Python Error', 'Error: the given dates are incorrect!')
            return

        if end > self.now:
            messagebox.showerror('Python Error', 'Error: the given dates are incorrect!')
            return

        self.time_period = self.historical_data[["Open"]][(self.historical_data.index >= np.datetime64(start)) & (self.historical_data.index <= np.datetime64(end))]
        if self.time_period.shape[0] == 0:
            messagebox.showerror('Python Error', 'Error: the selected period contains no data!')
            return
        
        if self.active_button != None:
            self.active_button.config(bg="SystemButtonFace")
        
        self.active_button = btn
        self.active_button.config(bg="sky blue")
        
        self.subplot.clear()

        self.time_period.index = pd.to_datetime(self.time_period.index, format = '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
            
        color, information = self.increased_or_decreased(self.time_period["Open"].head(1).values[0], self.time_period["Open"].tail(1).values[0])
        self.time_period.plot(use_index=True, y="Open", color = color, grid = True, ax=self.subplot)
        self.canvas.draw()
        self.graph_info.config(text = self.company_data[1] + information, fg = color)

    def refresh_prediction_info_labeles(self, mse, r2, pred, delta, change_std):
        self.mse_info.config(text = str(round(mse,3)), fg = 'blue')
        self.r2_info.config(text = str(round(r2,3)), fg = 'blue')
    
        if pred>0:
            self.prediction_info.config(text = "+" + str(round(pred,2)) + '%', fg = 'green')
        else:
            self.prediction_info.config(text = str(round(pred,2)) + '%', fg = 'red')

        if abs(pred) > 100*(1+change_std)**delta-100:
            messagebox.showwarning('WARNING!', 'Warning: The calculated change is irrealy large!')

    def generate_weekday_dates(self, n, given_date):
        weekday_dates = []
        
        given_date = datetime.strptime(given_date, '%Y-%m-%d').date()
        current_date = given_date

        while len(weekday_dates) < n :
            current_date += timedelta(days=1)
            
            if current_date.weekday() < 5:
                weekday_dates.append(current_date)

        return [str(date) for date in weekday_dates]

    def convert_to_rgb(self, color_triplet):
        r = int(color_triplet[0] * 255)
        g = int(color_triplet[1] * 255)
        b = int(color_triplet[2] * 255)
        
        rgb_code = "#{:02x}{:02x}{:02x}".format(r, g, b)

        return rgb_code
            
    def calc_polynomial_regression(self, event):
        degree = self.degree_input.get()
        delta = self.predict_delta_input.get()

        if degree == '' or delta == '':
            messagebox.showerror('ERROR', 'Error: one of the parameters is not given!')
            return

        degree = int(degree)
        delta = int(delta)
        n = self.time_period.shape[0]
        
        if degree == 0:
            messagebox.showerror('Python Error', 'Error: Approximation degree can\'t be 0!')
            return

        if degree > 30:
            messagebox.showerror('Python Error', 'Error: Approximation degree can\'t be bigger than 30!')
            return

        if delta == 0:
            messagebox.showerror('Python Error', 'Error: The prediction delta can\'t be 0!')
            return

        if degree > 9*n/10:
            messagebox.showwarning('WARNING!', 'Warning: Approximation degree is too large, might cause over fitting!')
        
        if degree <= 6:
            messagebox.showwarning('WARNING!', 'Warning: Approximation degree is too small, might cause under fitting!')
            
        if delta > n/10:
            messagebox.showwarning('WARNING!', 'Warning: The prediction delta is too large, might cause exponential prediction error!')            

        color_g = 'blue'
        if self.time_period['Open'][-1:][0] > self.time_period['Open'][1:][0]:
            color_g = 'green'
        if self.time_period['Open'][-1:][0] < self.time_period['Open'][1:][0]:
            color_g = 'red'
                
        changes = self.time_period['Open'].pct_change(1)[1:]
        dist = [0] * 200
        n -= 1

        for val in changes:
            p = int(val*100) + 100
            
            p = max(p,-100)
            p = min(p, 99)
        
            dist[p]+=1

        for i in range(200):
            dist[i] *=100/n

        x_tr = np.linspace(-14,15,30)
        y_tr = dist[85:115]

        with warnings.catch_warnings():
            warnings.simplefilter('ignore', np.RankWarning)
            model = np.poly1d(np.polyfit(x_tr, y_tr, degree))
            y_pr = [max(model(i),0) for i in x_tr]

        mse = mean_squared_error(y_tr,y_pr)
        r2 = r2_score(y_tr,y_pr)

        last = self.time_period['Open'].values[-1:][0]
        changes = x_tr/100+1
        changes_mat = [changes * 30]
        pred = last * changes
        
        max_ = max(y_pr)
        colors_scatter = [[(max_-val)/max_,(max_-val)/max_, 1] for val in y_pr]

        pred_dates = self.generate_weekday_dates(delta, self.time_period['Open'].index[-1:][0])

        real_val = self.time_period.values
        real_ind = self.time_period.index.values

        pred_val = []
        pred_ind = []
        pred_col = []

        change_std = np.std(self.time_period['Open'].pct_change(1)[1:])

        for i in range(0,delta):
            for j in range(30):
                if abs((pred[j] - last)*100/last) <= 100*(1+change_std)**(i+1)-100:
                    pred_val.append(pred[j])
                    pred_ind.append(pred_dates[i])
                    pred_col.append(colors_scatter[j])
            
            avg_pred = pred[15]
            pred = (pred * changes_mat/30)[0]
            
        self.subplot.grid(visible = True)
        self.subplot.plot(real_ind, real_val, c = color_g)
        self.subplot.scatter(x = pred_ind, y = pred_val, c = pred_col)
        
        self.canvas.draw()

        pred = (avg_pred - last)*100/last
        self.refresh_prediction_info_labeles(mse, r2, pred, delta, change_std)

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
        
        self.one_month.place(x=0, y=4*self.box_y, width=3*self.box_x, height=1*self.box_y)
        self.one_month.config(font=("Helvetica bold", int(self.x_font)))
        
        self.three_months.place(x=0, y=6*self.box_y, width=3*self.box_x, height=1*self.box_y)
        self.three_months.config(font=("Helvetica bold", int(self.x_font)))
        
        self.six_months.place(x=0, y=8*self.box_y, width=3*self.box_x, height=1*self.box_y)
        self.six_months.config(font=("Helvetica bold", int(self.x_font)))

        self.one_year.place(x=0, y=10*self.box_y, width=3*self.box_x, height=1*self.box_y)
        self.one_year.config(font=("Helvetica bold", int(self.x_font)))
        
        self.three_years.place(x=0, y=12*self.box_y, width=3*self.box_x, height=1*self.box_y)
        self.three_years.config(font=("Helvetica bold", int(self.x_font)))
        
        self.five_years.place(x=0, y=14*self.box_y, width=3*self.box_x, height=1*self.box_y)
        self.five_years.config(font=("Helvetica bold", int(self.x_font)))
        
        self.max_time.place(x=0, y=16*self.box_y, width=3*self.box_x, height=1*self.box_y)
        self.max_time.config(font=("Helvetica bold", int(self.x_font)))

                #_____Prediction info labels_____
        self.degree.place(x=self.x_len-4*self.box_x, y=2*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.degree.config(font=("Helvetica bold", int(self.x_font)))

        self.degree_input.place(x=self.x_len-4*self.box_x, y=3*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.degree_input.config(font=("Helvetica bold", int(self.x_font)))
        
        self.predict_delta.place(x=self.x_len-4*self.box_x, y=4*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.predict_delta.config(font=("Helvetica bold", int(self.x_font)))

        self.predict_delta_input.place(x=self.x_len-4*self.box_x, y=5*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.predict_delta_input.config(font=("Helvetica bold", int(self.x_font)))

        self.calculate_polynom.place(x=self.x_len-4*self.box_x, y=6*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.calculate_polynom.config(font=("Helvetica bold", int(self.x_font)))

        self.mse.place(x=self.x_len-4*self.box_x, y=7*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.mse.config(font=("Helvetica bold", int(self.x_font)))
        
        self.mse_info.place(x=self.x_len-4*self.box_x, y=8*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.mse_info.config(font=("Helvetica bold", int(self.x_font)))

        self.r2.place(x=self.x_len-4*self.box_x, y=9*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.r2.config(font=("Helvetica bold", int(self.x_font)))
        
        self.r2_info.place(x=self.x_len-4*self.box_x, y=10*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.r2_info.config(font=("Helvetica bold", int(self.x_font)))

        self.prediction.place(x=self.x_len-4*self.box_x, y=11*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.prediction.config(font=("Helvetica bold", int(self.x_font)))
        
        self.prediction_info.place(x=self.x_len-4*self.box_x, y=12*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.prediction_info.config(font=("Helvetica bold", int(self.x_font)))

                #_____Graph abouth the data_____
        self.subplot.tick_params(axis='x', labelsize = self.x_font)
        self.subplot.tick_params(axis='y', labelsize = self.y_font)
        self.canvas.get_tk_widget().place(x=3*self.box_x, y=2*self.box_y, width=28*self.box_x, height=15*self.box_y)

                #_____Label for information of the graph_____
        self.graph_info.place(x=3*self.box_x, y=17*self.box_y, width=28*self.box_x, height=1*self.box_y)
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

        self.show_open.place(x=21*self.box_x, y=1*self.box_y, width=4*self.box_x, height=1*self.box_y)
        self.show_open.config(font=("Helvetica bold", int(self.x_font)))
