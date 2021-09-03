#!/usr/bin/python

import pandas as pd
import os
pd.options.mode.chained_assignment = None

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"
prices_folder = "data"
output_folder = "0_output"
temp_folder = "temp"

# import
fundamentals_table = pd.read_csv(os.path.join(cwd,input_folder,"3_fundamentals_processed.csv"), low_memory=False)
prices_table = pd.read_csv(os.path.join(cwd,input_folder,"2_prices_updated.csv"), low_memory=False)
#fundamentals_table = fundamentals_table.head()
#prices_table = prices_table.head()

# merge
df_merged = pd.merge(fundamentals_table, prices_table, how='inner', left_on=['symbol'], right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_merged.rename(columns={'52 Week High 3': '52h', '52 Week Low 3': '52l', 'Quote Price': 'price'}, inplace=True)
df_merged['price'].fillna(df_merged['Previous Close'], inplace=True)
df_merged['NAV'].fillna(df_merged['totalStockholderEquity'], inplace=True)

# fillna
cols_to_format = [i for i in df_merged.columns]
for col in cols_to_format:
    try:
        if col in ['price', 'from_low', 'from_high']:
            df_merged[col]=df_merged[col].fillna(0)
        else:
            pass
    except:
        pass

# adding from low/high
df_merged['from_low'] = (df_merged['price'] - df_merged['52l'])/df_merged['52l'] * 100
df_merged['from_high'] = (df_merged['price'] - df_merged['52h'])/df_merged['52h'] * 100

# adding TTM
df_ttm = df_merged.groupby(['symbol'])[['totalRevenue', 'costOfRevenue'
                                        ,'totalCashFromOperatingActivities', 'capitalExpenditures'
                                        , 'totalOperatingExpenses']].sum()
df_ttm = df_ttm.reset_index(drop=False)
df_ttm.rename(columns={'totalRevenue': 'totalRevenueTTM', 'costOfRevenue': 'costOfRevenueTTM'
    , 'totalCashFromOperatingActivities': 'totalCashFromOperatingActivitiesTTM'
    , 'totalOperatingExpenses': 'totalOperatingExpensesTTM'
    , 'capitalExpenditures': 'capitalExpendituresTTM' }, inplace=True)

# merging TTM
df_to_merge = df_merged
df_merged = pd.merge(df_to_merge, df_ttm, how='inner', left_on=['symbol'], right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)

# reorder and export
cols_to_order = ['symbol', 'price', '52l', '52h', 'from_low', 'from_high']
new_columns = cols_to_order + (df_merged.columns.drop(cols_to_order).tolist())
df_merged = df_merged[new_columns]
df_merged.to_csv(os.path.join(cwd,input_folder,"4_merged.csv"))
df_merged.to_excel(os.path.join(cwd,input_folder,"4_merged.xlsx"))

# export tickers again. just to have more narrowed result
stocks = df_merged[['symbol']].sort_values(by=['symbol'], ascending= True).drop_duplicates()
stocks.to_csv(os.path.join(cwd,input_folder,"4_tickers_filtered.csv"), index = False)