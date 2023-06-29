import tkinter as tk

import numpy as np
import pandas as pd

import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

class Page(tk.Frame):

    company_data = ["","",""]
    max_gain = [[0,""],[0,""],[0,""]]
    max_lost = [[0,""],[0,""],[0,""]]
    
    historical_data = pd.DataFrame()
    all_companies_info = pd.DataFrame()
    
    active_button = None
    
    start = time.time()
    end = 0.0

    x_len = 0
    y_len = 0
    x_font = 0
    y_font = 0

    box_x = 22
    box_y = 22

    data_time_size = 0
    now = datetime.today().date()
    
    def __init__(self, root, page_manager):
        tk.Frame.__init__(self, root)
        self.root = root
        self.page_manager = page_manager
        
        self.root.state('zoomed')
        #self.root.bind("<Configure>", self.resize_window)

    def go_exit(self, event):
        self.root.destroy()

    def go_back(self, event, page_name):
        if self.active_button != None:
            self.active_button.config(bg="SystemButtonFace")
            
        self.page_manager.show_page(page_name)

    def set_historical_data(self, data):
        self.historical_data = data.copy()

    def get_days_nr(self, date_target):
        return(self.historical_data[self.historical_data.index >= np.datetime64(date_target)].shape[0])
    
    def calc_percent_change(self, a, b):
        a = max(a, 0.001)
        change = round((b-a)*100/b,2)
        color = ''
        
        if change < 0:
            color = 'red'
        elif change > 0:
            color = 'green'
        else:
            color = 'blue'
        
        return change, color
    
    def increased_or_decreased(self, a, b):

        change, color = self.calc_percent_change(a, b)
        information = ""
        diff = b-a
        sig = ''
        if diff>0:
            sig = '+'

        information = ": " + str(round(b,2)) + ", change: " + sig + str(round(diff,2)) + " (" + sig + str(change) + "%)"
        return color, information

    def check_companies(self, event):
        value = event.widget.get()

        if value == '':
            self.companies['values'] = self.companies_name
        else:
            data = []
            for item in self.companies_name:
                if value.lower() in item.lower():
                    data.append(item)

            self.companies['values'] = data

    def check_input_company(self, company_name):
        
        ok=True
        for company in self.companies_name_symbol:
            if company_name == company[0]:
                ok=False
                self.company_data[0] = company[0]
                self.company_data[1] = company[1]
                break

        if ok:
            self.company_data[0] = "ERROR"
            
    def create_name_symbol_vector(self, name, symbol):
        res = []

        for n,s in zip(name, symbol):
            res.append([n,s])
        
        return res
    
    def show(self):
        self.lift()
        self.show_widgets()

    def show_widgets(self):
        pass
