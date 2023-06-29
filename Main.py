from tkinter import Tk
from tkinter import messagebox

import pandas as pd

import yfinance as yf
from yahooquery import Ticker

import threading

import time

from data import *

import PageManager
import Page01
import Page02
import Page03
import Page04
import Page05
import Page06
import Page07
import Page08

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

    data['SMA13'] = data['Open'].rolling(13).mean().fillna(data['Open'])
    data['SMA50'] = data['Open'].rolling(50).mean().fillna(data['Open'])
    data['R_STD50'] = data['Open'].rolling(50).std().fillna(data['Open'])
    data['SMA200'] = data['Open'].rolling(200).mean().fillna(data['Open'])
    data['R_STD200'] = data['Open'].rolling(200).std().fillna(data['Open'])
    
    data.to_csv("E:/SZAKDOLGOZAT/A_DOLOGZAT/downloads/" + str(ticker + ".csv"))

def download_all_data():
    
    for comp in companies_info:
        new_thread = threading.Thread(target = download_one_company_data, args = (comp[1],))
        new_thread.start()
        
def max_gain_lost():
    
    for company in companies_info:
        
        data = pd.read_csv("E:/SZAKDOLGOZAT/A_DOLOGZAT/downloads/" + str(company[1]) + ".csv")

        n = data.shape[0]

        if n<2:
            continue
        
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

def download_company_info():

    name = []
    tag = []
    sector = []
    industry = []
    market_cap = []
    country = []

    for comp in companies_info:
        
        name.append(comp[0])
        tag.append(comp[1])
        
        if comp[1] == "GC=F":
            sector.append(None)
            industry.append(None)
            market_cap.append(None)
            country.append(None)
            continue
        
        company = Ticker(comp[1])
        company_profile = company.asset_profile[comp[1]]
        company_summary = company.summary_detail[comp[1]]

        '''
        if comp[1] == "BTC-USD":
            sector.append(None)
            industry.append(None)
            market_cap.append(company_summary['marketCap'])
            continue
        '''
        
        if str(type(company_profile)) != '<class \'str\'>' and comp[1] != "BTC-USD":
            sector.append(company_profile['sector'])
            industry.append(company_profile['industry'])
            country.append(company_profile['country'])
        else:
            sector.append(None)
            industry.append(None)
            country.append(None)
            
        market_cap.append(company_summary['marketCap'])
                                                
    all_companies = pd.DataFrame({
        "Name" : name,
        "Ticker" : tag,
        "Sector": sector,
        "Industry": industry,
        "Market cap": market_cap,
        "Country" : country
    })

    all_companies.to_csv("E:/SZAKDOLGOZAT/A_DOLOGZAT/downloads/0xALL_COMPANIES.csv")

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
        

        #time.sleep(60)

        max_gain_lost()

        #download_company_info()
            
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
        
    page_manager = PageManager.PageManager(root)
    page_manager.create_page("page01", Page01.xPage01)
    page_manager.create_page("page02", Page02.xPage02)
    page_manager.create_page("page03", Page03.xPage03)
    page_manager.create_page("page04", Page04.xPage04)
    page_manager.create_page("page05", Page05.xPage05)
    page_manager.create_page("page06", Page06.xPage06)
    page_manager.create_page("page07", Page07.xPage07)
    page_manager.create_page("page08", Page08.xPage08)

    page_manager.show_page("page01")
    
    root.mainloop()
    
main()
