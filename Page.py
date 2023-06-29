import tkinter as tk

import numpy as np
import pandas as pd

import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

class Page(tk.Frame):

    company_data = ["","",""]
    historical_data = pd.DataFrame()

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

        #self.max_gain = []
        #self.max_lost = []
        
        self.root.state('zoomed')
        #self.root.bind("<Configure>", self.resize_window)

    def go_exit(self, event):
        self.root.destroy()

    def set_historical_data(self, data):
        self.historical_data = data.copy()

    def get_days_nr(self, date_target):
        return(self.historical_data[self.historical_data.index >= np.datetime64(date_target)].shape[0])
        
    def show(self):
        self.lift()
        self.show_widgets()

    def show_widgets(self):
        pass
