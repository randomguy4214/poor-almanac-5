#!/usr/bin/python

import os

import pandas as pd

pd.options.mode.chained_assignment = None

# set directories and files
cwd = os.getcwd()
input_folder = "0_input"
prices_folder = "data"
output_folder = "0_output"
temp_folder = "temp"
print('starting merging the financials and prices datasets')

# import
fundamentals_table = pd.read_csv(os.path.join(cwd,input_folder,"3_fundamentals_processed.csv"), low_memory=False)
prices_table = pd.read_csv(os.path.join(cwd,input_folder,"2_prices_updated.csv"), low_memory=False)
#fundamentals_table = fundamentals_table.head(1000)
#prices_table = prices_table.head()
print("importing fundamentals and prices is done")

# adding TTM from t0,t1,t2,t3 before selecting t0 only for income and cash flows
df_ttm = fundamentals_table.groupby(['symbol'])[['totalRevenue', 'costOfRevenue'
                                        ,'totalCashFromOperatingActivities', 'capitalExpenditures'
                                        , 'totalOperatingExpenses', 'totalCashflowsFromInvestingActivities']].sum()
df_ttm = df_ttm.reset_index(drop=False)
df_ttm['capitalExpenditures'].fillna(df_ttm['totalCashflowsFromInvestingActivities'], inplace=True)
df_ttm.rename(columns={'totalRevenue': 'totalRevenueTTM', 'costOfRevenue': 'costOfRevenueTTM'
    , 'totalCashFromOperatingActivities': 'totalCashFromOperatingActivitiesTTM'
    , 'totalOperatingExpenses': 'totalOperatingExpensesTTM'
    , 'capitalExpenditures': 'capitalExpendituresTTM'
    , 'Total Debt (mrq)': 'Debt'}, inplace=True)
print("ttm precalculated")

# calculating propertyPlantEquipment for first period
df_PPE_first = fundamentals_table[fundamentals_table['Period'] == "t-3"]
df_PPE = df_PPE_first[['symbol', 'propertyPlantEquipment']]
df_PPE.rename(columns={'propertyPlantEquipment': 'PPE_t_3'}, inplace=True)
print('PPE prepared for further calc' )

# select only latest data to filter out balance sheet
fundamentals_table = fundamentals_table[fundamentals_table['Period'] == "t0"]
print("fundamentals_table period = t0")

# merge fundamentals and prices
df_merged = pd.merge(fundamentals_table, prices_table, how='left', left_on=['symbol'], right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_merged.rename(columns={'52 Week High 3': '52h'
    , '52 Week Low 3': '52l'
    , 'Quote Price': 'price'
    , 'Quarterly Revenue Growth (yoy)': 'QtrGrwth'}, inplace=True)
print("raw fundamentals and prices merged")

# merge TTM
df_to_merge = df_merged
df_merged = pd.merge(df_to_merge, df_ttm, how='left', left_on=['symbol'], right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
print("ttm merged")

# merge PPE
df_to_merge = df_merged
df_merged = pd.merge(df_to_merge, df_PPE, how='left', left_on=['symbol'], right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
print("PPE merged")

# fix prices and shares if missing or trash
df_merged['price'].fillna(df_merged['Previous Close'], inplace=True)
df_merged['price'].fillna(df_merged['Open'], inplace=True)
df_merged.loc[df_merged['sharesOutstanding'] < 1000, 'sharesOutstanding'] = df_merged['marketCap']/df_merged['price']
df_merged['sharesOutstanding'].fillna(df_merged['marketCap']/df_merged['price'], inplace=True)
print('fixed prices and sharesOutstanding')

#fix other if missing
cols_to_format = [i for i in df_merged.columns]
for col in cols_to_format:
    try:
        if col in ['price', 'from_low', 'from_high', 'SharesOutstanding']:
            df_merged[col]=df_merged[col].fillna(0)
        else:
            pass
    except:
        pass

# adding from low/high
df_merged['from_low'] = (df_merged['price'] - df_merged['52l'])/df_merged['52l'] * 100
df_merged['from_high'] = (df_merged['price'] - df_merged['52h'])/df_merged['52h'] * 100
df_merged = df_merged[~(df_merged['from_low'] == 0) & ~(df_merged['from_high'] == -100)]
#df_merged = df_merged[(df_merged['price'] > 0.001)]
print('added low/high and filtered some trash')

# find latest shorts value
df_shorts = pd.DataFrame(df_merged.filter(regex='Short % of Float|symbol')).iloc[:,:]
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
#df_shorts.to_excel(os.path.join(cwd,input_folder,'4_df_shorts.xlsx'), index=False)
print("shorts calculated")

# merge shorts
df_to_merge = df_merged
df_merged = pd.merge(df_to_merge, df_shorts, how='left', left_on=['symbol'], right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_merged.drop_duplicates()
df_merged.reset_index(drop=True, inplace=True)
#df_merged.to_excel(os.path.join(cwd,input_folder,'5_df_shorts.xlsx'), index=False)
print("shorts merged")

# start creating new variables
df = df_merged
# process
df['NAV'].fillna(df['totalStockholderEquity'], inplace=True)
df['Short%'] = df['Short%'].str.rstrip('%').str.replace(',','').astype('float')
df['OpMarg'] = ((df['totalRevenueTTM'] - df['costOfRevenueTTM']) / df['totalRevenueTTM'] * 100).astype('float')
df['%Ins'] = df['% Held by Insiders 1'].str.rstrip('%').str.replace(',','').astype('float')
df['%QtrGrwth'] = df['QtrGrwth'].str.rstrip('%').str.replace(',','').astype('float')
df['BVPS'] = df['Book Value Per Share (mrq)']

# fix debt naming
# from https://stackoverflow.com/questions/39684548/convert-the-string-2-90k-to-2900-or-5-2m-to-5200000-in-pandas-dataframe
df['Debt'] = (df['Total Debt (mrq)'].replace(r'[ktmbKTMB]+$', '', regex=True).astype(float) *
            df['Total Debt (mrq)'].str.extract(r'[\d\.]+([ktmbKTMB]+)', expand=False).fillna(1).replace(
            ['k', 't', 'm', 'b', 'K', 'T', 'M', 'B']
            , [10**3, 10**3, 10**6, 10**9, 10**3, 10**3, 10**6, 10**9]).astype(int))

df['SO'] = (df['Shares Outstanding 5'].replace(r'[ktmbKTMB]+$', '', regex=True).astype(float) *
            df['Shares Outstanding 5'].str.extract(r'[\d\.]+([ktmbKTMB]+)', expand=False).fillna(1).replace(
            ['k', 't', 'm', 'b', 'K', 'T', 'M', 'B']
            , [10**3, 10**3, 10**6, 10**9, 10**3, 10**3, 10**6, 10**9]).astype(int))

df['marCap'] = (df['Market Cap'].replace(r'[ktmbKTMB]+$', '', regex=True).astype(float) *
            df['Market Cap'].str.extract(r'[\d\.]+([ktmbKTMB]+)', expand=False).fillna(1).replace(
            ['k', 't', 'm', 'b', 'K', 'T', 'M', 'B']
            , [10**3, 10**3, 10**6, 10**9, 10**3, 10**3, 10**6, 10**9]).astype(int))

# calculate additional variables
print('calculating additional variables')
print('................................................................................................')
print('Main goal is to find actual earnings to owner and compare them to the price.')
print('As of now, there is no 5y data for companies, therefore we have to do an approximation.')
print('Bad start, but we dont have anything better.')
print('We take PPE for the last period, divide it by PPE first period, and extrapolate growth rate to 4 periods.')
print('This way we can discount PPE in first quarter to get PPE last year.')
print('We also assume that %QtrGrwth is equal to YoY growth of sales.')
print('We discount sales TTM by %QtrGrwth to approximate last year sales.')
print('Divide that by PPE and you get your maintenance capex ratio.')
print('multiply this number by %QtrGrwth and get growth capex.')
print('Substract that number and learn your reinvestment capex.')
print('Use it to find Owners Earnings.')
print('Divide that by shares outstanding and then divide by sales price.')
print('This way you get your more correct earnings per share vs price')
print('................................................................................................')

df['PPE_growth_3_periods_ago'] = (df['propertyPlantEquipment'] - df['PPE_t_3']) / df['PPE_t_3'] -1
df['PPE_growth_per_period'] = (1 + df['PPE_growth_3_periods_ago']).pow(1/3) - 1
df['PPE_last_year'] = df['PPE_growth_3_periods_ago'] / (1+df['PPE_growth_per_period'])
df['Sales_last_year'] = df['totalRevenueTTM'] / (1+df['%QtrGrwth'])
df['Sales_absolute_increase'] = df['totalRevenueTTM'] - df['Sales_last_year']
df['maint_capex_ratio'] = df['PPE_last_year'] / df['Sales_last_year']
df['growth_capex'] = df['maint_capex_ratio'] * df['Sales_absolute_increase']
df['capex_more_correct'] = df['capitalExpendituresTTM'] - df['growth_capex']
df['capex_more_correct'] = df['capex_more_correct'].fillna(df['capitalExpendituresTTM'])
df['capex_more_correct'] = df['capex_more_correct'].fillna(df['totalCashflowsFromInvestingActivities'])

df['NAV/S'] = df['NAV'] / df['sharesOutstanding']
df['B/S/P'] = df['NAV/S'] / df['price']
df['OwnEa'] =  df['totalCashFromOperatingActivitiesTTM'] + df['capex_more_correct']
df['OwnEa/S'] = df['OwnEa'] / df['sharesOutstanding']
df['OwnEa/S/P'] = df['OwnEa/S'] / df['price']

df['marg'] = (df['totalRevenueTTM'] - df['totalOperatingExpensesTTM']) / df['totalRevenueTTM'] * 100
df['WC/S'] = df['WC'] / df['sharesOutstanding']
df['WC/S/P'] = df['WC/S'] / df['price']
df['WC/Debt'] = df['WC'] / df['Debt']
df['Rev/S/P'] = df['Revenue Per Share (ttm)'] / df['price']
print('additional variables calculated')

# fillna again
cols_to_format = [i for i in df.columns]
for col in cols_to_format:
    try:
        if col in ['price', 'from_low', 'from_high', 'OpMarg', 'B/S/P', 'marg']:
            df[col]=df[col].fillna(0)
        else:
            pass
    except:
        pass

# format
cols_to_format = [i for i in df.columns]
for col in cols_to_format:
    try:
        if col in ['price', 'B/S/P']:
            df[col]=df[col].round(2)
        else:
            df[col] = df[col].round(0)
    except:
        pass
print('formatting is done')

# reorder
cols_to_order = ['symbol', 'price', '52l', '52h', 'from_low', 'from_high']
new_columns = cols_to_order + (df_merged.columns.drop(cols_to_order).tolist())
df_merged = df_merged[new_columns]
print('reordering is done')

#  export
print('export will take a while')
df_merged.to_csv(os.path.join(cwd,input_folder,"4_merged.csv"))
df_merged.to_excel(os.path.join(cwd,input_folder,"4_merged.xlsx"))

# export tickers again. just to have more narrowed result
stocks = df_merged[['symbol']].sort_values(by=['symbol'], ascending= True).drop_duplicates()
stocks.to_csv(os.path.join(cwd,input_folder,"4_tickers_filtered.csv"), index = False)
print("datasets are merged and exported")