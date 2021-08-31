#!/usr/bin/python

import pandas as pd
import os
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

# select only latest data
df = df[df['Period'] == "t0"]

# filter and clean up
drop_list_ticker = drop_list['symbol'].tolist()
df = df[~df['symbol'].isin(drop_list_ticker)] # drop some tickers
drop_list_industry = drop_list['industry'].tolist()
df = df[~df['industry'].isin(drop_list_industry)] # drop some industries
drop_list_country = drop_list['country'].tolist()
df = df[~df['country'].isin(drop_list_country)] # drop some industries
df = df[~df['longName'].isnull()]

# find latest shorts value
df_shorts = pd.DataFrame(df.filter(regex='Short % of Float|symbol')).iloc[:,:]
df_shorts.dropna(how='all', axis=1, inplace=True)
#df_shorts_names = df_shorts.columns.str.strip('Short % of Float')
df_shorts_names = df_shorts.columns.str.extract('.*\((.*)\).*')
df_shorts_names.rename(columns={ df_shorts_names.columns[0]: "date" }, inplace = True)
df_shorts_names_dates = pd.to_datetime(df_shorts_names['date'])#, errors='coerce')
df_shorts.columns = df_shorts_names_dates
df_shorts_names_dates = df_shorts_names_dates.sort_values(ascending=False)
df_shorts = df_shorts[df_shorts_names_dates]
df_shorts.columns = [*df_shorts.columns[:-1], 'symbol']
df_shorts = df_shorts.melt(id_vars=["symbol"], var_name="Date")
df_shorts = df_shorts.dropna(axis = 0)
df_shorts.columns = [*df_shorts.columns[:-1], 'Short%']
#df_shorts.to_excel(os.path.join(cwd,input_folder,'5_df_shorts.xlsx'), index=False)

# merge this shit
df_merged = pd.merge(df, df_shorts, how='left', left_on=['symbol'], right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_merged.drop_duplicates()
df_merged.reset_index(drop=True, inplace=True)
#df_merged.to_excel(os.path.join(cwd,input_folder,'5_df_shorts.xlsx'), index=False)

# finally some action
df = df_merged

# process
df['Short%'] = df['Short%'].str.rstrip('%').str.replace(',','').astype('float')
#df['OpMarg'] = df['Operating Margin (ttm)'].str.rstrip('%').str.replace(',','').astype('float')
df['OpMarg'] = ((df['totalRevenue'] - df['costOfRevenue']) / df['totalRevenue'] * 100).astype('float')
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
df['marg'] = (df['totalRevenue'] - df['totalOperatingExpenses']) / df['totalRevenue'] * 100
df['WC/S'] = df['WC'] / df['SO']
df['WC/S/P'] = df['WC/S'] / df['price']
df['WC/Debt'] = df['WC'] / df['Debt']
df['Rev/S/P'] = df['Revenue Per Share (ttm)'] / df['price']

# reorder and select relevant columns
cols_to_order = ['symbol', 'price'
    , 'from_low', 'from_high'
    , 'OpMarg'
    , 'longName', 'industry', 'country'
    , 'Short%', '%Ins'
    , 'B/S/P', 'BVPS', 'Rev/S/P'
    , 'WC/S/P'
    , 'WC/Debt', 'Total Debt (mrq)', 'FCF/S/P'
    ]

# reorder
new_columns = cols_to_order + (df.columns.drop(cols_to_order).tolist())
df_export = df[cols_to_order]

# format
cols_to_format = [i for i in df_export.columns]
for col in cols_to_format:
    try:
        if col in ['from_low', 'from_high', 'OpMarg', 'B/S/P']:
            df_export[col]=df_export[col].fillna(0)
        else:
            pass
    except:
        pass

cols_to_format = [i for i in df_export.columns]
for col in cols_to_format:
    try:
        if col in ['price', 'B/S/P', 'from_low', 'from_high', 'OpMarg']:
            df_export[col]=df_export[col].round(0)
        else:
            df_export[col] = df_export[col].round(2)
    except:
        pass


# sort
df_export.sort_values(by=['from_low'], ascending=[True], inplace=True, na_position ='last')

# filter
#df_export = df_export.loc[(df_export['from_low'] < 15)] # less than x% increase from lowest point
#df_export = df_export.loc[(df_export['price'] < 5)] # less than 5 bucks
df_export = df_export.loc[df_export['B/S/P'] > 0.6] # Book to market

# export
df_export.to_excel(os.path.join(cwd,input_folder,'5_df_output.xlsx'), index=False)
