
import pandas as pd
import os
import yahoo_fin as yf

pd.set_option('display.max_columns', None)
pd.options.display.float_format = '{:20,.2f}'.format
pd.options.mode.use_inf_as_na = True

cwd = os.getcwd()
input_folder = "0_input"
prices_folder = "data"
output_folder = "0_output"

tickers_narrowed = pd.read_csv(os.path.join(cwd,input_folder,"3_tickers_narrowed.csv"))
tickers_narrowed = tickers_narrowed.head(n=1)
ticker_narrowed = tickers_narrowed.values.tolist()
tickers = ' '.join(tickers_narrowed["symbol"].astype(str)).strip()
#print(tickers)

from yahoo_fin.stock_info import * #initiate yahoo_fin
financials_table = []
company_info = []
for t in tickers.split(' '):




#data = yf.download(tickers_string, start="2020-08-15", end="2021-08-15",
#                   group_by="ticker",  threads = True)
#data.to_csv(os.path.join(cwd,input_folder,"yf_test2.csv"))

