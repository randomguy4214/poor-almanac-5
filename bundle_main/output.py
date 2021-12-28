#!/usr/bin/python

import os

import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'

# formatting
pd.set_option('display.max_columns', None)
pd.options.display.float_format = '{:20,.2f}'.format
pd.options.mode.use_inf_as_na = True

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"

# import files
drop_list = pd.read_excel(os.path.join(cwd,input_folder,"0_drop_list.xlsx"))
df = pd.read_csv(os.path.join(cwd,input_folder,"4_merged.csv"), low_memory=False)

# reorder and select relevant columns
cols_to_order = [
    'industry'
    , 'country'
    , 'longName'
    , 'symbol'
    , 'p'
    #, 'Market Cap'
    , 'from_low'
    , '52l'
    , 'from_high'
    , '52h'
    , 'OpMarg'
    #, 'OwnEa/SO'
    , 'OwnEa/S/p'
    , 'Rev/S/p'
    , '%QtrGrwth'
    , '%YoYGrwth'
    , 'B/S/p'
    , 'WC/Debt'
    , 'Eq/Debt'
    , 'Short%'
    , '%Ins'
    #, 'totalCashFromOperatingActivitiesTTM'
    #, 'capitalExpendituresTTM'
    #, 'capex_more_correct'
    #, 'sharesOutstanding'
    , 'marCap'
    ]

# reorder
new_columns = cols_to_order + (df.columns.drop(cols_to_order).tolist())
df_export = df[cols_to_order]

# sort and export unfiltered
df_export.sort_values(by=['from_low'], ascending=[True], inplace=True, na_position ='last')
output_raw = '5_df_output_unflitered.xlsx'
df_export.to_excel(os.path.join(cwd,output_raw), index=False)

# filter by drop list
drop_list_ticker = drop_list['symbol'].tolist()
df_export = df_export[~df_export['symbol'].isin(drop_list_ticker)] # drop some tickers
drop_list_industry = drop_list['industry'].tolist()
df_export = df_export[~df_export['industry'].isin(drop_list_industry)] # drop some industries
drop_list_country = drop_list['country'].tolist()
df_export = df_export[df_export['country'].isin(drop_list_country)] # drop some industries

# filter by variables
#df_export = df_export[(df_export['from_low'] >= 0)] # impossible
df_export = df_export[(df_export['marCap'] >= 1)] # more than 1m marcap
#df_export = df_export[(df_export['from_low'] < 30)] # less than x% increase from lowest point
#df_export = df_export[(df_export['price'] < 5)] # less than 5 bucks
#df_export = df_export[df_export['B/S/P'] > 0.6] # Book to market

# export
output_filtered = '5_df_output_filtered.xlsx'
df_export.to_excel(os.path.join(cwd,output_filtered), index=False)

# export tickers again. just to have more narrowed result
stocks = df_export[['symbol']].sort_values(by=['symbol'], ascending= True).drop_duplicates()
stocks.to_csv(os.path.join(cwd,input_folder,"5_tickers_filtered.csv"), index = False)
print("datasets are merged and exported")

print('please see the raw results in ' + output_raw + ' and filteted in '+ output_filtered)