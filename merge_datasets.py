#!/usr/bin/python

import pandas as pd
import os
pd.options.mode.chained_assignment = None  # default='warn'

# formatting
#pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.options.display.float_format = '{:20,.2f}'.format
pd.options.mode.use_inf_as_na = True

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"
prices_folder = "data"

# import files
drop_list = pd.read_excel(os.path.join(cwd,input_folder,"0_drop_list.xlsx"))
df_prices = pd.read_csv(os.path.join(cwd,input_folder,"3_narrowed_filter.csv"), low_memory=False)
df_fundamentals_processed = pd.read_excel(os.path.join(cwd,input_folder,"4_fundamentals_processed.xlsx"))

#some additional filtering
df_prices = df_prices[df_prices['Date'] == df_prices['Date'].max()] #double check
df_fundamentals_processed = df_fundamentals_processed[df_fundamentals_processed['Period'] == "t0"]
#df_fundamentals_processed = df_fundamentals_processed[df_fundamentals_processed['country'] == "United States"]

# merge data sets
df_merged = pd.merge(df_prices, df_fundamentals_processed, how='left', left_on=['symbol'], right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_merged.drop_duplicates()
df_merged.reset_index(inplace=True)

# drop if no longName (usually filters out trash companies that dont have info on yahoo finance)
df_merged = df_merged[~df_merged['longName'].isnull()]

# filter on tickers and industries
drop_list_ticker = drop_list['symbol'].tolist()
df_merged = df_merged[~df_merged['symbol'].isin(drop_list_ticker)] # drop some tickers
drop_list_industry = drop_list['industry'].tolist()
df_merged = df_merged[~df_merged['industry'].isin(drop_list_industry)] # drop some industries
drop_list_country = drop_list['country'].tolist()
df_merged = df_merged[~df_merged['country'].isin(drop_list_country)] # drop some industries

# calculate additional variables
df_merged['NAV_per_share'] = df_merged['NAV'] / df_merged['sharesOutstanding']
df_merged['NAV_per_share_to_price'] = df_merged['NAV_per_share'] / df_merged['price']
df_merged['FCF_per_share'] = (df_merged['totalCashFromOperatingActivities'] - df_merged['capitalExpenditures']) / df_merged['sharesOutstanding']
#df_merged['marg'] = df_merged['Gross Profit'] / df_merged['Revenue'] * 100
df_merged['marg'] = (df_merged['totalRevenue'] - df_merged['costOfRevenue']) / df_merged['totalRevenue'] * 100

# reorder and drop irrelevant columns
cols_to_order = ['symbol', 'price', 'low', 'high', 'from_low', 'from_high', 'NAV_per_share_to_price', 'FCF_per_share', 'marg', 'longName', 'industry', 'country']
new_columns = cols_to_order + (df_merged.columns.drop(cols_to_order).tolist())
#df_merged = df_merged[new_columns]
# df_merged = df_merged.round(2)

df_merged_2 = df_merged[cols_to_order]
df_merged_2 = df_merged_2.round(2)
df_merged_2.sort_values(by=['NAV_per_share_to_price','from_low'], ascending=[False,True], inplace=True)
# export full fundamentals
df_merged_2.to_excel(os.path.join(cwd,input_folder,'5_merged.xlsx'), index=False)




