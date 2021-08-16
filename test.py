#!/usr/bin/python

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


from yahoo_fin.stock_info import *
financials_table = []
values_table = []
for t in tickers.split(' '):
    try:
        # first loop through "values" in "dictionary"
        df_yf = get_financials(t, yearly=False, quarterly=True)
        for keys, values in df_yf.items():
            #df_keys = keys #we dont need "keys"
            df = values
            values_table.append(df)
        values_table = pd.concat(values_table)
        values_table.reset_index(drop=False, inplace=True)
        values_table.columns.values[[0, 1, 2, 3, 4]] = ['Breakdown', 't0', 't-1', 't-2', 't-3']
        values_table.set_index('Breakdown', inplace=True)

        # then transpose and combine
        df_T = values_table.T
        #df_T = df_T.drop(index=df_T.index[0], axis=0, inplace=True)
        #df_T.rename(columns={'netTangibleAssets':'NAV'}, inplace=True)
        print(df_T)
        df_T['WC'] = df_T['totalCurrentAssets'] - df_T['totalCurrentLiabilities']
        df_T['symbol'] = t

        #export
        financials_table.append(df_T)
    except:
        pass

financials_table = pd.concat(financials_table)
financials_table.drop_duplicates()
financials_table.to_csv(os.path.join(cwd,input_folder,"financials_table.csv"))
financials_table.to_excel(os.path.join(cwd,input_folder,"financials_table.xlsx"))
#print(financials_table)


#data = yf.download(tickers_string, start="2020-08-15", end="2021-08-15",
#                   group_by="ticker",  threads = True)
#data.to_csv(os.path.join(cwd,input_folder,"yf_test2.csv"))

