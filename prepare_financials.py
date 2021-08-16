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
tickers_narrowed = tickers_narrowed.head(n=2)
ticker_narrowed = tickers_narrowed.values.tolist()
tickers = ' '.join(tickers_narrowed["symbol"].astype(str)).strip()
#print(tickers)

from yahoo_fin.stock_info import * #initiate yahoo_fin
financials_table = []
company_info = []
for t in tickers.split(' '):
    try:
        # first loop through "values" in "dictionary"
        df_yf_financials = get_financials(t, yearly=False, quarterly=True)
        values_table = []
        for keys, values in df_yf_financials.items():
            #df_keys = keys #we dont need "keys"
            df = values
            df.reset_index(drop=False, inplace=True)
            df.columns.values[[0, 1, 2, 3, 4]] = ['Breakdown', 't0', 't-1', 't-2', 't-3']
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
        #append
        financials_table.append(df_T)

        #get company info
        df_yf_info = get_company_info(t)
        df_yf_info.reset_index(drop=False, inplace=True)
        df_yf_info = df_yf_info[~df_yf_info['Breakdown'].duplicated(keep='first')] #catching double entries in values to properly reset the index
        df_yf_info.set_index('Breakdown', inplace=True)
        df_info = df_yf_info.T
        df_info['symbol'] = t
        df_info.reset_index(drop=False, inplace=True)
        company_info.append(df_info)
    except:
        pass

# reorder and export
financials_table = pd.concat(financials_table)
financials_table.drop_duplicates()
financials_table.to_csv(os.path.join(cwd,input_folder,"4_fundamentals_processed.csv"))
financials_table.to_excel(os.path.join(cwd,input_folder,"4_fundamentals_processed.xlsx"))

company_info = pd.concat(company_info)
company_info.drop_duplicates()
company_info.to_excel(os.path.join(cwd,input_folder,"4_company_info.xlsx"))

