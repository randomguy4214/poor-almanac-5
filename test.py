#!/usr/bin/python

import pandas as pd
import os
import yfinance as yf
yf.pdr_override() # yfinance to pandas

pd.set_option('display.max_columns', None)
pd.options.display.float_format = '{:20,.2f}'.format
pd.options.mode.use_inf_as_na = True

cwd = os.getcwd()
input_folder = "0_input"
prices_folder = "data"
output_folder = "0_output"

tickers_narrowed = pd.read_csv(os.path.join(cwd,input_folder,"3_tickers_narrowed.csv"))
tickers_list = tickers_narrowed.head().values.tolist()
tickers_string = tickers_narrowed.head().to_string(index=False, header=None)

financials_table = []
for ticker in tickers_list:
    try:
        print(ticker)
        yf_ticker = yf.Ticker(ticker)
        yf = yf_ticker.financials
        financials_table.append(yf)
    except:
        pass

financials_table = pd.concat(financials_table)
financials_table.drop_duplicates()
financials_table.to_csv(os.path.join(cwd,input_folder,"financials_table.csv"))
print(financials_table)


#data = yf.download(tickers_string, start="2020-08-15", end="2021-08-15",
#                   group_by="ticker",  threads = True)
#data.to_csv(os.path.join(cwd,input_folder,"yf_test2.csv"))


