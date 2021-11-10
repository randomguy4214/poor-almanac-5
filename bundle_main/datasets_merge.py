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
fundamentals_table_annually = pd.read_csv(os.path.join(cwd,input_folder,"3_fundamentals_processed_annually.csv"), low_memory=False)
fundamentals_table = pd.read_csv(os.path.join(cwd,input_folder,"4_fundamentals_processed_quarterly.csv"), low_memory=False)
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

# select only latest quarterly data to filter out balance sheet
fundamentals_table = fundamentals_table[fundamentals_table['Period'] == "t0"]
print("fundamentals_table period = t0")

# splitting annual data
df_y0 = fundamentals_table_annually[fundamentals_table_annually['Period'] == "y0"]
df_y0.rename(columns={'totalRevenue': 'revenue_last_year'}, inplace=True)
df_y0 = df_y0[['symbol', 'revenue_last_year']]

#df_y_minus_1 = fundamentals_table_annually[fundamentals_table_annually['Period'] == "y-1"]
#df_y_minus_2 = fundamentals_table_annually[fundamentals_table_annually['Period'] == "y-2"]
#df_y_minus_3 = fundamentals_table_annually[fundamentals_table_annually['Period'] == "y-3"]

# finding historical averages
df_avg_historical = fundamentals_table_annually.groupby(['symbol'])[['totalRevenue', 'capitalExpenditures', 'costOfRevenue', 'propertyPlantEquipment']].mean()
df_avg_historical = df_avg_historical.reset_index(drop=False)
df_avg_historical.rename(columns={'totalRevenue': 'mean_historical_revenue'
                                    , 'capitalExpenditures': 'mean_historical_capex'
                                    , 'costOfRevenue': 'mean_historical_costOfRevenue'
                                  , 'propertyPlantEquipment': 'mean_historical_propertyPlantEquipment'}, inplace=True)
df_avg_historical = df_avg_historical[['symbol', 'mean_historical_revenue', 'mean_historical_costOfRevenue'
                                    , 'mean_historical_capex', 'mean_historical_propertyPlantEquipment']]
print("historical averages calculated")

# merge fundamentals and prices
df_merged = pd.merge(fundamentals_table, prices_table, how='left', left_on=['symbol'], right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_merged.rename(columns={'52 Week High 3': '52h'
    , '52 Week Low 3': '52l'
    , 'Quote Price': 'p'
    , 'Quarterly Revenue Growth (yoy)': 'QtrGrwth'}, inplace=True)
print("raw fundamentals and prices merged")

# merge TTM
df_to_merge = df_merged
df_merged = pd.merge(df_to_merge, df_ttm, how='left', left_on=['symbol'], right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
print("ttm merged")

# merge last_year_revenue
df_to_merge = df_merged
df_merged = pd.merge(df_to_merge, df_y0, how='left', left_on=['symbol'], right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
print("last year revenue merged")

# merge df_avg_historical
df_to_merge = df_merged
df_merged = pd.merge(df_to_merge, df_avg_historical, how='left', left_on=['symbol'], right_on=['symbol'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
print("historical averaged data")

# fix prices and shares if missing or trash
df_merged['p'].fillna(df_merged['Previous Close'], inplace=True)
df_merged['p'].fillna(df_merged['Open'], inplace=True)
df_merged['52l'].fillna(df_merged['fiftyTwoWeekLow'], inplace=True)
df_merged['52h'].fillna(df_merged['fiftyTwoWeekHigh'], inplace=True)
df_merged.loc[df_merged['sharesOutstanding'] < 1000, 'sharesOutstanding'] = df_merged['marketCap']/df_merged['p']

# adding from low/high
df_merged.loc[df_merged['p'] < df_merged['52l'], 'p'] = df_merged['52l'] # fix too low price
df_merged['from_low'] = (df_merged['p'] - df_merged['52l'])/df_merged['52l'] * 100
df_merged['from_high'] = (df_merged['p'] - df_merged['52h'])/df_merged['52h'] * 100
#df_merged = df_merged[~(df_merged['from_low'] == 0) & ~(df_merged['from_high'] == -100)]
#df_merged = df_merged[(df_merged['p'] > 0.001)]
print('added low/high and filtered some trash')

#fix if missing
df_merged['sharesOutstanding'].fillna(df_merged['marketCap']/df_merged['p'], inplace=True)
cols_to_format = [i for i in df_merged.columns]
for col in cols_to_format:
    try:
        if col in ['p', 'from_low', 'from_high', 'SharesOutstanding']:
            df_merged[col]=df_merged[col].fillna(0)
        else:
            pass
    except:
        pass

print('fixed prices and sharesOutstanding')

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

# drop irrelevant shorts columns
df_merged.drop([col for col in df_merged.columns if 'Short %' in col],axis=1,inplace=True)
df_merged.drop([col for col in df_merged.columns if 'Shares Short' in col],axis=1,inplace=True)
df_merged.drop([col for col in df_merged.columns if 'Short Ratio' in col],axis=1,inplace=True)

print("start calculations")
df = df_merged
# fix numbers naming with KMB
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

df['marCap'] = df['marCap'].fillna(df['SO'] * df['p'])
df['marCap'] = df['marCap'] / 1000000

# start creating new variables
df['NAV'].fillna(df['totalStockholderEquity'], inplace=True)
df['Short%'] = df['Short%'].str.rstrip('%').str.replace(',','').astype('float')
df['OpMarg'] = ((df['mean_historical_revenue'] - df['mean_historical_costOfRevenue']) / df['mean_historical_revenue'] * 100).astype('float')
df['%Ins'] = df['% Held by Insiders 1'].str.rstrip('%').str.replace(',','').astype('float')
df['%QtrGrwth'] = df['QtrGrwth'].str.rstrip('%').str.replace(',','').astype('float')
df['BVPS'] = df['Book Value Per Share (mrq)']

# calculate additional variables
df['Sales_absolute_increase'] = df['totalRevenueTTM'] - df['revenue_last_year']
df['%YoYGrwth'] = (df['Sales_absolute_increase'] / df['revenue_last_year'] ) -1
df['maint_capex_ratio'] = df['mean_historical_propertyPlantEquipment'] / df['mean_historical_revenue']
df['growth_capex'] = df['maint_capex_ratio'] * df['Sales_absolute_increase']
df['capex_more_correct'] = df['capitalExpendituresTTM'] - df['growth_capex']
df['capex_more_correct'] = df['capex_more_correct'].fillna(df['capitalExpendituresTTM'])
df['capex_more_correct'] = df['capex_more_correct'].fillna(df['totalCashflowsFromInvestingActivities'])

df['NAV/S'] = df['NAV'] / df['sharesOutstanding']
df['B/S/p'] = df['NAV/S'] / df['p']
df['OwnEa'] =  df['totalCashFromOperatingActivitiesTTM'] + df['capex_more_correct']
df['OwnEa/S'] = df['OwnEa'] / df['sharesOutstanding']
df['OwnEa/S/p'] = df['OwnEa/S'] / df['p']

df['marg'] = (df['totalRevenueTTM'] - df['totalOperatingExpensesTTM']) / df['totalRevenueTTM'] * 100
df['WC/S'] = df['WC'] / df['sharesOutstanding']
df['WC/S/p'] = df['WC/S'] / df['p']
df['WC/Debt'] = df['WC'] / df['Debt']
df['Eq/Debt'] = df['totalStockholderEquity'] / (df['totalStockholderEquity'] + df['Debt'])
df['Rev/S/p'] = df['Revenue Per Share (ttm)'] / df['p']

print('additional variables calculated')

# fillna again
cols_to_fillna = [i for i in df.columns]
for col in cols_to_fillna:
    try:
        if col in ['p', 'from_low', 'from_high', 'OpMarg', 'B/S/p', 'marg', 'marCap']:
            df[col]=df[col].fillna(0)
        else:
            pass
    except:
        pass
print('fillna is done')

# format
cols_to_format = [i for i in df.columns]
for col in cols_to_format:
    try:
        if col in ['p', 'B/S/p']:
            df[col]=df[col].round(2)
        else:
            df[col] = df[col].round(0)
    except:
        pass
print('formatting is done')

# reorder
cols_to_order = ['symbol', 'p', '52l', '52h', 'from_low', 'from_high']
new_columns = cols_to_order + (df_merged.columns.drop(cols_to_order).tolist())
df_merged = df_merged[new_columns]
print('reordering is done')

#  export
print('export will take a while')
df_merged.to_csv(os.path.join(cwd,input_folder,"4_merged.csv"))
df_merged.to_excel(os.path.join(cwd,input_folder,"4_merged.xlsx"))

# export tickers again. just to have more narrowed result
stocks = df_merged[['symbol']].sort_values(by=['symbol'], ascending= True).drop_duplicates()
stocks.to_csv(os.path.join(cwd,input_folder,"4_tickers_narrowed.csv"), index = False)
print("datasets are merged and exported")

# export column
df_columns=pd.DataFrame(df_merged.columns.T)
df_columns.to_excel(os.path.join(cwd,input_folder,'4_merged_columns.xlsx'))