import pandas as pd
from pandas import json_normalize

# Specify the path to your JSON file
json_file_path = 'olx_houses.json'

# Read JSON data from the file into a DataFrame
df = pd.read_json(json_file_path)

# Flatten the dictionaries within 'additional_properties' and 'first_image'
df_additional_properties = json_normalize(df['additional_properties'])
df_first_image = json_normalize(df['first_image'])

# Concatenate the flattened DataFrames with the original DataFrame
df = pd.concat([df, df_additional_properties, df_first_image], axis=1)

# Drop the original columns containing dictionaries
df = df.drop(['additional_properties', 'first_image'], axis=1)

# Print the DataFrame
print(df)

# Save DataFrame to Excel
df.to_excel("lista.xlsx", index=False)





