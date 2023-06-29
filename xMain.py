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
        progress= False,
        period = "max",
        interval = "1d",
        ignore_tz = False,
        group_by = 'ticker',
        auto_adjust = False,
        prepost = False,
        threads = False,
        proxy = None
    )

    data.index = pd.to_datetime(data.index, format = '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
    
    data['SMA50'] = data['Open'].rolling(50).mean().fillna(data['Open'])
    data['BELL50up2'] = data.apply(lambda x: x['SMA50'] + x['SMA50'] * 24/100, axis=1)
    data['BELL50up1'] = data.apply(lambda x: x['SMA50'] + x['SMA50'] * 17/100, axis=1)
    data['BELL50bo1'] = data.apply(lambda x: x['SMA50'] - x['SMA50'] * 17/100, axis=1)
    data['BELL50bo2'] = data.apply(lambda x: x['SMA50'] - x['SMA50'] * 24/100, axis=1)
        
    data['SMA200'] = data['Open'].rolling(200).mean().fillna(data['Open'])
    data['BELL200up2'] = data.apply(lambda x: x['SMA200'] + x['SMA200'] * 24/100, axis=1)
    data['BELL200up1'] = data.apply(lambda x: x['SMA200'] + x['SMA200'] * 17/100, axis=1)
    data['BELL200bo1'] = data.apply(lambda x: x['SMA200'] - x['SMA200'] * 17/100, axis=1)
    data['BELL200bo2'] = data.apply(lambda x: x['SMA200'] - x['SMA200'] * 24/100, axis=1)
    
    data.to_csv("downloads/" + str(ticker + ".csv"))

def download_all_data():
    
    for company in companies_info:
        new_thread = threading.Thread(target = download_one_company_data, args = (company[1],))
        new_thread.start()
        
def max_gain_lost():

    for company in companies_info:
        
        data = pd.read_csv("downloads/" + str(company[1]) + ".csv")

        n = data.shape[0]
        begin = data["Open"][n-5]
        end = data["Open"][n-1]

        prc = abs(begin - end)*100/begin
                    
        if begin>=end:
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
        
        #data_download_thread = threading.Thread(target = download_all_data)    
        #data_download_thread.start()

        '''
        refresh_thread = threading.current_thread()
        print("Refresher thread: ",refresh_thread)
        
        refresh_thread = threading.current_thread()
        print("Downloader main thread: ",refresh_thread)

        data_download_thread.join()
        
        i = 0
        for t in threading.enumerate():
            #if t is main_thread or t is refresh_thread:
                #continue
            #t.join()
            print(i, ": ", t)
            i+=1
        '''
        
        #time.sleep(180)

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
    time.sleep(5)
    print("APPLICATION START...")
    
    root = Tk()
    xPage1.Page1(root)
    root.mainloop()

main()
