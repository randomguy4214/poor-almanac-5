
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
fundamentals_table = pd.read_csv(os.path.join(cwd,input_folder,"4_merged.csv"), low_memory=False)
fundamentals_table['totalRevenue'] = fundamentals_table['totalRevenue'].astype(int)
df = fundamentals_table.groupby(['symbol'])[['totalRevenue', 'costOfRevenue','totalCashFromOperatingActivities']].sum()
df = df.reset_index(drop=False)
#df['costOfRevenue'] = fundamentals_table.groupby(['symbol'])['costOfRevenue'].sum()

#df['costOfRevenue']
#df['totalCashFromOperatingActivities']
#df['capitalExpenditures']

print(df)
