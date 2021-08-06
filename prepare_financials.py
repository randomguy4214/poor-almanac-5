#!/usr/bin/python

import pandas as pd
import os
import investpy
pd.set_option('display.max_columns', None)
pd.options.display.float_format = '{:20,.2f}'.format
pd.options.mode.use_inf_as_na = True

cwd = os.getcwd()
input_folder = "0_input"
prices_folder = "data"
output_folder = "0_output"

stocks_input = pd.read_csv(os.path.join(cwd,input_folder,"2_tickers_filtered.csv"))
stocks = stocks_input['symbol']
stocks = stocks #.head()

# stocks info
stock_info_table = []
for stock in stocks:
    try:
        pd_stock = investpy.search_quotes(text=stock, products=['stocks'], countries=['united states'], n_results=1)
        information = pd.DataFrame(pd_stock.retrieve_information(), index=[0])
        information['stock'] = stock
        stock_info_table.append(information)
    except:
        pass
stock_info_table = pd.concat(stock_info_table)
stock_info_table.to_csv(os.path.join(cwd,input_folder,"3_stock_info_table.csv"))

# cash flows
cash_flow_statements_table = []
for stock in stocks:
    try:
        pd_stock = investpy.stocks.get_stock_financial_summary(stock, 'united states', summary_type='cash_flow_statement', period='quarterly')
        pd_stock['stock'] = stock
        cash_flow_statements_table.append(pd_stock)
    except:
        pass
cash_flow_statements_table = pd.concat(cash_flow_statements_table)

#reorder cash flows
cash_flow_statements_table.reset_index(drop=True)
cols_to_order = ['stock']
new_columns = cols_to_order + (cash_flow_statements_table.columns.drop(cols_to_order).tolist())
cash_flow_statements_table = cash_flow_statements_table[new_columns]
cash_flow_statements_table.to_csv(os.path.join(cwd,input_folder,"3_cash_flow_statements_table.csv"))

#balance_sheet
balance_sheet_table = []
for stock in stocks:
    try:
        pd_stock = investpy.stocks.get_stock_financial_summary(stock, 'united states', summary_type='balance_sheet', period='quarterly')
        pd_stock['stock'] = stock
        balance_sheet_table.append(pd_stock)
    except:
        pass
balance_sheet_table = pd.concat(balance_sheet_table)
balance_sheet_table.to_csv(os.path.join(cwd,input_folder,"3_balance_sheet_table.csv"))

#income statements
income_statements_table = []
for stock in stocks:
    try:
        pd_stock = investpy.stocks.get_stock_financial_summary(stock, 'united states', summary_type='income_statement', period='quarterly')
        pd_stock['stock'] = stock
        income_statements_table.append(pd_stock)
    except:
        pass
income_statements_table = pd.concat(income_statements_table)
income_statements_table.to_csv(os.path.join(cwd,input_folder,"3_income_statements_table.csv"))

# merge financial statements
df_merged = pd.merge(cash_flow_statements_table, balance_sheet_table, how='inner', left_on=['stock', 'Date'], right_on=['stock', 'Date'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_to_merge = df_merged
df_merged = pd.merge(df_to_merge, income_statements_table, how='inner', left_on=['stock', 'Date'], right_on=['stock', 'Date'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_merged.dropna(inplace=True)
df_merged.reset_index(inplace=True)

# add info
df_to_merge = df_merged
df_merged = pd.merge(df_to_merge, stock_info_table, how='inner', left_on=['stock'], right_on=['stock'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)

# export
df_merged.to_csv(os.path.join(cwd, input_folder,"3_fundamentals_processed.csv"))
