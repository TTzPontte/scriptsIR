import pandas as pd

# Load the Excel file
file_path = '../installments/input_data/installments.xlsx'
df = pd.read_excel(file_path)

df.head()
# Convert 'date' column to datetime and extract year and month
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

# Dropping the original 'date' column as we have extracted year and month
df = df.drop('date', axis=1)

# Create a DataFrame with all combinations of contractId, year, and month
all_combinations = pd.MultiIndex.from_product([df['contractId'].unique(), df['year'].unique(), range(1, 13)], names=['contractId', 'year', 'month']).to_frame(index=False)

# Merge this with the original data
merged_df = pd.merge(all_combinations, df, on=['contractId', 'year', 'month'], how='left')

# Replace NaN values in 'value' column with 0
merged_df['value'].fillna(0, inplace=True)

merged_df.head(15)  # Display the first 15 rows to check the structure
