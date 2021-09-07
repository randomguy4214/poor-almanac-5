#!/usr/bin/python

import pandas as pd
import os

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
tickers_narrowed = pd.read_csv(os.path.join(cwd,input_folder,"1_tickers_narrowed.csv"))
#tickers_narrowed = tickers_narrowed[tickers_narrowed['symbol'].str.contains("DE000A2GSVV5|ALTUW|UROY")] #test tickers
#tickers_narrowed = tickers_narrowed #.head(n=3)  #test tickers
ticker_narrowed = tickers_narrowed.values.tolist()
tickers = ' '.join(tickers_narrowed["symbol"].astype(str)).strip()

index_max = pd.to_numeric(tickers_narrowed.index.values.max())
from yahoo_fin.stock_info import * #initiate yahoo_fin
financials_table = []
company_info = []
for t in tickers.split(' '):
    try:
        # progress number
        n = pd.to_numeric(tickers_narrowed["symbol"][tickers_narrowed["symbol"] == t].index).values
        print(t, n/index_max*100)

        name = t + ".csv"
        if not os.path.exists(os.path.join(cwd, input_folder, temp_folder, financials_temp, name)):

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

            # export
            name = t + ".csv"
            df.to_csv(os.path.join(cwd, input_folder, temp_folder, financials_temp, name), index=False)
        else:
            pass
    except:
        pass
