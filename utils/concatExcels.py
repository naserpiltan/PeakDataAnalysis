import pandas as pd
import os
def concatenate_excel_files(directory, output_file):
    # List to hold DataFrames from each Excel file
    df_list = []

    # Iterate over all Excel files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.xlsx'):
            file_path = os.path.join(directory, filename)

            # Read the Excel file into a DataFrame
            df = pd.read_excel(file_path)

            # Append the DataFrame to the list
            df_list.append(df)

    # Concatenate all DataFrames in the list into one
    concatenated_df = pd.concat(df_list, ignore_index=True)

    # Write the concatenated DataFrame to a new Excel file
    concatenated_df.to_excel(output_file, index=False)


# Example usage
directory = 'E:/TDNA_Projects/Peak_data_analysis/data/all_data_final/excel/peak_hour_classification'
output_file = 'E:/TDNA_Projects/Peak_data_analysis/data/all_data_final/excel/peak_hour_classification/peak_hour_classification_aggregated.xlsx'
concatenate_excel_files(directory, output_file)