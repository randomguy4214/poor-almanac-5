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
financials_temp = "financials"

# prepare tickers list
tickers_narrowed = pd.read_csv(os.path.join(cwd,input_folder,"2_tickers_filtered.csv"))
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

            #get statistics
            df_yf_stats = get_stats(t)
            df_yf_stats.reset_index(drop=True, inplace=True)
            df_yf_stats.set_index('Attribute', inplace=True)
            df_stats = df_yf_stats.T
            df_stats['symbol'] = t
            df_stats.reset_index(drop=True, inplace=True)

            #get company info
            df_yf_info = get_company_info(t)
            df_yf_info.reset_index(drop=False, inplace=True)
            df_yf_info = df_yf_info[~df_yf_info['Breakdown'].duplicated(keep='first')] #catching double entries in values to properly reset the index
            df_yf_info.set_index('Breakdown', inplace=True)
            df_info = df_yf_info.T
            df_info['symbol'] = t
            df_info.reset_index(drop=False, inplace=True)

            # merge
            # financials to quote data
            to_merge = df_T
            df_merged = pd.merge(df_T, df_yf_quote_data_2, how='left', left_on=['symbol'], right_on=['symbol'], suffixes=('', '_drop'))
            df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
            df_merged.drop_duplicates()
            df_merged.reset_index(drop=True, inplace=True)

            # to stats
            to_merge = df_merged
            df_merged = pd.merge(to_merge, df_stats, how='left', left_on=['symbol'], right_on=['symbol'], suffixes=('', '_drop'))
            df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
            df_merged.drop_duplicates()
            df_merged.reset_index(drop=True, inplace=True)

            # to info
            to_merge = df_merged
            df_merged = pd.merge(to_merge, df_info, how='left', left_on=['symbol'], right_on=['symbol'], suffixes=('', '_drop'))
            df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
            df_merged.drop_duplicates()
            df_merged.reset_index(drop=True, inplace=True)

            # append
            cols_to_order = ['Period', 'symbol', 'NAV', 'sharesOutstanding']
            new_columns = cols_to_order + (df_merged.columns.drop(cols_to_order).tolist())
            df_merged = df_merged[new_columns]
            #financials_table.append(df_merged)

            # export
            name = t + ".csv"
            df_merged.to_csv(os.path.join(cwd, input_folder, temp_folder, financials_temp, name), index=False)
        else:
            pass
    except:
        pass
