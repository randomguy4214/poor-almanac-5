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
simfin = "simfin"

income_csv = pd.read_csv(os.path.join(cwd,input_folder,simfin,"us-income-ttm.csv"), sep=";")
bs_csv = pd.read_csv(os.path.join(cwd,input_folder,simfin,"us-balance-ttm.csv"), sep=";")
cf_csv = pd.read_csv(os.path.join(cwd,input_folder,simfin,"us-cashflow-ttm.csv"), sep=";")

# merge financial statements
df_merged = pd.merge(income_csv, bs_csv, how='inner', left_on=['SimFinId', 'Fiscal Year', 'Fiscal Period'], right_on=['SimFinId', 'Fiscal Year', 'Fiscal Period'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)
df_to_merge = df_merged
df_merged = pd.merge(df_to_merge, cf_csv, how='inner', left_on=['SimFinId', 'Fiscal Year', 'Fiscal Period'], right_on=['SimFinId', 'Fiscal Year', 'Fiscal Period'], suffixes=('', '_drop'))
df_merged.drop([col for col in df_merged.columns if 'drop' in col], axis=1, inplace=True)

# keep only latest per company
df_merged.drop_duplicates('Ticker', keep='last', inplace=True)

# export
df_merged.to_csv(os.path.join(cwd, input_folder,"3_fundamentals_processed.csv"))
#print(df_merged.columns.values)

