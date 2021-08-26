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
df_fundamentals_processed = pd.read_csv(os.path.join(cwd,input_folder,"4_fundamentals_processed.csv"), low_memory=False)

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

# rename
df = df_merged

# filter
df = df.loc[(df['from_low'] < 15)] # less than x% increase from lowest point

# fix
#df['Total Debt (mrq)'] = df['Total Debt (mrq)'].astype(int)

# calculate additional variables
df['NAV_per_share'] = df['NAV'] / df['sharesOutstanding']
df['B/P'] = df['NAV_per_share'] / df['price']
df['FCF/S'] = (df['totalCashFromOperatingActivities'] - df['capitalExpenditures']) / df['sharesOutstanding']
df['FCF/S/P'] = df['FCF/S'] / df['price']
df['marg'] = (df['totalRevenue'] - df['costOfRevenue']) / df['totalRevenue'] * 100
df['WC/S'] = df['WC'] / df['sharesOutstanding']
df['WC/S/P'] = df['WC/S'] / df['price']
#df['WC/Debt'] = df['WC'] / df['Total Debt (mrq)']


# reorder and select relevant columns
cols_to_order = ['symbol', 'price', 'low', 'high', 'from_low', 'from_high'
    , 'FCF/S/P', 'marg', 'Operating Margin (ttm)'
    , 'Short % of Shares Outstanding 4', '% Held by Insiders 1'
    , 'longName', 'industry', 'country'
    , 'B/P', 'Book Value Per Share (mrq)'
    , 'Shares Outstanding 5', 'WC/S/P'
    #, 'WC/Debt'
    , 'Total Debt (mrq)'
    ]
new_columns = cols_to_order + (df.columns.drop(cols_to_order).tolist())
df_export = df[cols_to_order]
df_export = df_export.round(2).fillna(method="ffill")
df_export.sort_values(by=['B/P', 'from_low'], ascending=[False,True], inplace=True, na_position ='last')


# export
df_export.to_excel(os.path.join(cwd,input_folder,'5_df_output.xlsx'), index=False)




