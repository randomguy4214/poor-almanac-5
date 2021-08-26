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

# select only latest data
df_prices = df_prices[df_prices['Date'] == df_prices['Date'].max()] #double check
df_fundamentals_processed = df_fundamentals_processed[df_fundamentals_processed['Period'] == "t0"]

# merge data sets
df_merged = pd.merge(df_prices, df_fundamentals_processed, how='left', left_on=['symbol'], right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_merged.drop_duplicates()
df_merged.reset_index(inplace=True)

# filter on tickers and industries
drop_list_ticker = drop_list['symbol'].tolist()
df_merged = df_merged[~df_merged['symbol'].isin(drop_list_ticker)] # drop some tickers
drop_list_industry = drop_list['industry'].tolist()
df_merged = df_merged[~df_merged['industry'].isin(drop_list_industry)] # drop some industries
drop_list_country = drop_list['country'].tolist()
df_merged = df_merged[~df_merged['country'].isin(drop_list_country)] # drop some industries

# rename
df = df_merged
df['Short%'] = df['Short % of Float (Aug 12, 2021) 4'].str.rstrip('%').str.replace(',','').astype('float')
df['OpMarg'] = df['Operating Margin (ttm)'].str.rstrip('%').str.replace(',','').astype('float')
df['%Ins'] = df['% Held by Insiders 1'].str.rstrip('%').str.replace(',','').astype('float')
df['BVPS'] = df['Book Value Per Share (mrq)']

# fix from https://stackoverflow.com/questions/39684548/convert-the-string-2-90k-to-2900-or-5-2m-to-5200000-in-pandas-dataframe
df['Debt'] = (df['Total Debt (mrq)'].replace(r'[ktmbKTMB]+$', '', regex=True).astype(float) *
            df['Total Debt (mrq)'].str.extract(r'[\d\.]+([ktmbKTMB]+)', expand=False).fillna(1).replace(
            ['k', 't', 'm', 'b', 'K', 'T', 'M', 'B']
            , [10**3, 10**3, 10**6, 10**9, 10**3, 10**3, 10**6, 10**9]).astype(int))

df['SO'] = (df['Shares Outstanding 5'].replace(r'[ktmbKTMB]+$', '', regex=True).astype(float) *
            df['Shares Outstanding 5'].str.extract(r'[\d\.]+([ktmbKTMB]+)', expand=False).fillna(1).replace(
            ['k', 't', 'm', 'b', 'K', 'T', 'M', 'B']
            , [10**3, 10**3, 10**6, 10**9, 10**3, 10**3, 10**6, 10**9]).astype(int))


# calculate additional variables
df['NAV_per_share'] = df['NAV'] / df['sharesOutstanding']
df['B/S/P'] = df['NAV_per_share'] / df['price']
df['FCF/S'] = (df['totalCashFromOperatingActivities'] - df['capitalExpenditures']) / df['sharesOutstanding']
df['FCF/S/P'] = df['FCF/S'] / df['price']
df['marg'] = (df['totalRevenue'] - df['costOfRevenue']) / df['totalRevenue'] * 100
df['WC/S'] = df['WC'] / df['SO']
df['WC/S/P'] = df['WC/S'] / df['price']
df['WC/Debt'] = df['WC'] / df['Debt']

# filter
#df = df.loc[(df['from_low'] < 15) | (df['price'] < 5)] # less than x% increase from lowest point or less than 5 bucks
#df = df.loc[df['B/S/P'] > 0.8]

# drop if no longName (usually filters out trash companies that dont have info on yahoo finance)
df = df_merged[~df_merged['longName'].isnull()]

# reorder and select relevant columns
cols_to_order = ['symbol', 'price'
    #, 'low', 'high'
    , 'from_low', 'from_high'
    , 'OpMarg'
    , 'longName', 'industry', 'country'
    , 'Short%', '%Ins'
    , 'B/S/P', 'BVPS'
    , 'WC/S/P'
    , 'WC/Debt', 'Total Debt (mrq)', 'FCF/S/P'
    ]
new_columns = cols_to_order + (df.columns.drop(cols_to_order).tolist())
df_export = df[cols_to_order]
df_export = df_export.round(2).fillna(method="ffill")
df_export.sort_values(by=['from_low'], ascending=[False], inplace=True, na_position ='last')

# export
df_export.to_excel(os.path.join(cwd,input_folder,'5_df_output.xlsx'), index=False)