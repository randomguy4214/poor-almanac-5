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
tickers_narrowed = tickers_narrowed #.head(n=1)
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
        df_T['Period'] = df_T.index

        # get "quote data"
        df_yf_quote_data = get_quote_data(t)
        df_yf_quote_data_1 = pd.Series(df_yf_quote_data)
        df_yf_quote_data_2 = pd.DataFrame(df_yf_quote_data_1).T
        df_yf_quote_data_2.reset_index(drop=False, inplace=True)
        df_yf_quote_data_2 = df_yf_quote_data_2.drop(columns=['index'])

        #get company info
        df_yf_info = get_company_info(t)
        df_yf_info.reset_index(drop=False, inplace=True)
        df_yf_info = df_yf_info[~df_yf_info['Breakdown'].duplicated(keep='first')] #catching double entries in values to properly reset the index
        df_yf_info.set_index('Breakdown', inplace=True)
        df_info = df_yf_info.T
        df_info['symbol'] = t
        df_info.reset_index(drop=False, inplace=True)

        # merge
        to_merge = df_T
        df_merged = pd.merge(df_T, df_yf_quote_data_2, how='left', left_on=['symbol'], right_on=['symbol'], suffixes=('', '_drop'))
        df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
        df_merged.drop_duplicates()
        df_merged.reset_index(inplace=True)

        to_merge = df_merged
        df_merged = pd.merge(to_merge, df_info, how='left', left_on=['symbol'], right_on=['symbol'], suffixes=('', '_drop'))
        df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
        df_merged.drop_duplicates()
        df_merged.reset_index(inplace=True)

        #append
        cols_to_order = ['Period', 'symbol', 'NAV', 'sharesOutstanding']
        new_columns = cols_to_order + (df_merged.columns.drop(cols_to_order).tolist())
        df_merged = df_merged[new_columns]
        df_merged.drop(columns=['level_0','index'])
        financials_table.append(df_merged)

    except:
        pass

# reorder and export
financials_table = pd.concat(financials_table)
financials_table.drop_duplicates()
financials_table.to_csv(os.path.join(cwd,input_folder,"4_fundamentals_processed.csv"))
financials_table.to_excel(os.path.join(cwd,input_folder,"4_fundamentals_processed.xlsx"))


