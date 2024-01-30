import pandas as pd

def process_installments(input_file_path, output_file_path):
    # Load the Excel file
    df = pd.read_excel(input_file_path)

    # Convert 'date' column to datetime and extract year and month
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month

    # Drop the original 'date' column
    df.drop('date', axis=1, inplace=True)

    # Create a DataFrame with all combinations of contractId, year, and month
    all_combinations = pd.MultiIndex.from_product(
        [df['contractId'].unique(), df['year'].unique(), range(1, 13)],
        names=['contractId', 'year', 'month']
    ).to_frame(index=False)

    # Merge with the original data
    merged_df = pd.merge(all_combinations, df, on=['contractId', 'year', 'month'], how='left')

    # Replace NaN values in 'value' column with 0
    merged_df['value'].fillna(0, inplace=True)

    # Save the modified DataFrame to a new Excel file
    merged_df.to_excel(output_file_path, index=False)

# Example usage
input_file_path = 'input_data/installments.xlsx'  # Replace with the path to your input file
output_file_path = 'output/installments_12_months.xlsx'  # Replace with the path to your output file

process_installments(input_file_path, output_file_path)

