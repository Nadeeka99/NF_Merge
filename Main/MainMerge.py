import pandas as pd
import os
from tkinter import Tk, filedialog

# Create a GUI window to select the directory containing the Excel files
root = Tk()
root.withdraw()  # Hide the main window

input_directory = filedialog.askdirectory(title="Select Directory Containing Excel Files")

if not input_directory:
    print("No directory selected. Exiting.")
else:
    # Get a list of all Excel files in the directory
    excel_files = [f for f in os.listdir(input_directory) if f.endswith('.xlsx')]

    if len(excel_files) < 2:
        print("At least 2 Excel files are required for merging.")
    else:
        # Read the top rows of each Excel file and store them in a dictionary
        top_rows = {}
        for file_name in excel_files:
            file_path = os.path.join(input_directory, file_name)
            df = pd.read_excel(file_path, header=None, nrows=1)
            top_rows[file_name] = df.values.tolist()[0]

        # Find the common top row among all files
        common_top_row = set(top_rows[excel_files[0]])
        for row in top_rows.values():
            common_top_row &= set(row)

        if len(common_top_row) == 0:
            print("No common top row found among the files.")
        else:
            # Merge the Excel files based on the common top row
            merged_data = []
            for file_name in excel_files:
                file_path = os.path.join(input_directory, file_name)
                df = pd.read_excel(file_path, skiprows=1)  # Skip the header row
                merged_data.append(df[df.iloc[:, 0].isin(common_top_row)])

            # Concatenate the dataframes vertically
            merged_df = pd.concat(merged_data, ignore_index=True)

            # Save the merged dataframe to a new Excel file
            merged_output_path = os.path.join(input_directory, 'merged_output.xlsx')
            merged_df.to_excel(merged_output_path, index=False)

            print(f"Merged data saved to {merged_output_path}")
