
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
fundamentals_table = pd.read_csv(os.path.join(cwd,input_folder,"3_fundamentals_processed.csv"), low_memory=False)
d = fundamentals_table.head(59)
df = d.value_counts(subset=['symbol'], sort=False)
df.sort_values(by=['2'], ascending=[True], inplace=True, na_position ='last')

print(df)
