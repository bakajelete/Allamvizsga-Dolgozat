from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import pandas as pd

import yfinance as yf

import threading

import time

from data import *

import xPage1
import xPage2
import xPage3
        
def download_one_company_data(ticker):

    data = yf.download(
        tickers = ticker,
        period = "max",
        interval = "1d",
        ignore_tz = False,
        group_by = 'ticker',
        auto_adjust = True,
        prepost = False,
        threads = False,
        proxy = None
    )
    data.to_csv("downloads/" + str(ticker + ".csv"))

def download_all_data():
    
    for company in companies_info:
        new_thread = threading.Thread(target = download_one_company_data, args = (company[1],))
        new_thread.start()
        
def max_gain_lost():
    
    for company in companies_info:

        file = open("downloads/" + str(company[1] + ".csv"), 'r')
        shares = file.readlines()
        n = len(shares)

        begin_row = shares[n-7].strip().split(',')
        finish_row = shares[n-1].strip().split(',')
    
        begin = round(float(begin_row[1]), 5)
        finish = round(float(finish_row[1]), 5)
                    
        if begin > finish:
            prc = (begin - finish)*100/begin
            i = 0
            while i<3:
                if prc > max_lost[i][0]:
                    break
                i+=1
                
            if i < 3:
                j=2
                while j>i:
                   max_lost[j] = max_lost[j-1];
                   j-=1
                   
                max_lost[i] = [prc, company[1]]
            
        else:
            prc = (finish - begin)*100/begin
            i = 0
            while i<3:
                if prc > max_gain[i][0]:
                    break
                i+=1
                
            if i < 3:
                j=2
                while j>i:
                   max_gain[j] = max_gain[j-1];
                   j-=1
                   
                max_gain[i] = [prc, company[1]]

                

def refresh_data(main_thread, max_gain, max_lost):

    while True:
        #download_all_data()

        '''
        refresh_thread = threading.current_thread()
        for t in threading.enumerate():
            if t is main_thread or t is refresh_thread:
                continue
            t.join()
        '''
        
        #time.sleep(35)

        max_gain_lost()
            
        now = time.localtime()
        h = int(time.strftime("%H", now))
        m = int(time.strftime("%M", now))
        s = int(time.strftime("%S", now))

        h_w = (29-h)%24-1
        m_w = 59-m
        s_w = 60-s

        wait_time = s_w + m_w * 60 + h_w * 3600

        time.sleep(wait_time)

def main():
    
    main_thread = threading.current_thread()
    data_refresh_thread = threading.Thread(target=refresh_data, args=(main_thread, max_gain, max_lost,))
    data_refresh_thread.start()

    print("INITIALIZING DATA...")

    time.sleep(4)
    
    root = Tk()
    xPage1.Page1(root)
    root.mainloop()

main()
