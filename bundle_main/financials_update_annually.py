#!/usr/bin/python

import os

import pandas as pd

pd.set_option('display.max_columns', None)
pd.options.display.float_format = '{:20,.2f}'.format
pd.options.mode.use_inf_as_na = True

cwd = os.getcwd()
input_folder = "0_input"
prices_folder = "data"
output_folder = "0_output"
temp_folder = "temp"
prices_temp = "prices"
financials_temp = "financials_annually"

# prepare tickers list
tickers_narrowed = pd.read_csv(os.path.join(cwd,"0_symbols.csv"))
ticker_narrowed = tickers_narrowed.values.tolist()
tickers = ' '.join(tickers_narrowed["symbol"].astype(str)).strip()

# find last updated ticker (this is necessary if you lose internet connection, etc)
prices_last_ticker = pd.read_csv(os.path.join(cwd,input_folder,temp_folder,"financials_annually_last_ticker.csv"),index_col=0)
last_ticker_n = prices_last_ticker.values[0]
print("last ticker in financials_annually_last_ticker was number ", last_ticker_n)

# start importing
index_max = pd.to_numeric(tickers_narrowed.index.values.max())
from yahoo_fin.stock_info import *
financials_table = []
company_info = []
for t in tickers.split(' '):
    try:
        n = pd.to_numeric(tickers_narrowed["symbol"][tickers_narrowed["symbol"] == t].index).values
        if n > last_ticker_n:
            # first loop through "values" in "dictionary"
            df_yf_financials = get_financials(t, yearly=True, quarterly=False)
            values_table = []
            for keys, values in df_yf_financials.items():
                #df_keys = keys #we dont need "keys"
                df = values
                df.reset_index(drop=False, inplace=True)
                df.columns.values[[0, 1, 2, 3, 4]] = ['Breakdown', 'y0', 'y-1', 'y-2', 'y-3']
                values_table.append(df)
            values_table = pd.concat(values_table)
            values_table = values_table[~values_table['Breakdown'].duplicated(keep='first')] #catching double entries in values to properly reset the index
            values_table.drop_duplicates()
            values_table.reset_index(drop=True, inplace=True)
            values_table.set_index('Breakdown', inplace=True)

            # transpose financials
            df_T = values_table.T
            df_T.rename(columns={'netTangibleAssets':'NAV'}, inplace=True)
            df_T['WC'] = df_T['totalCurrentAssets'] - df_T['totalCurrentLiabilities']
            df_T['symbol'] = t
            df_T['Period'] = df_T.index
            df = df_T

            # print & export last_n
            print(t, n / index_max * 100, n, index_max, "financials annually update")
            financials_annually_last_ticker = pd.DataFrame({'number': n})
            financials_annually_last_ticker.to_csv(
                os.path.join(cwd, input_folder, temp_folder, "financials_annually_last_ticker.csv"))

            # export files
            name = t + ".csv"
            df.to_csv(os.path.join(cwd, input_folder, temp_folder, financials_temp, name), index=False)
    except:
        pass

financials_annually_last_ticker = pd.DataFrame({'number': [0]})
financials_annually_last_ticker.to_csv(
    os.path.join(cwd, input_folder, temp_folder, "financials_annually_last_ticker.csv"))
