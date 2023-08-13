import pandas as pd
from tkinter import Tk, filedialog

# Create a GUI window to select the Excel files
root = Tk()
root.withdraw()  # Hide the main window

excel_files = filedialog.askopenfilenames(title="Select Excel Files", filetypes=[("Excel Files", "*.xls;*.xlsx;*.csv")])

if not excel_files:
    print("No files selected. Exiting.")
else:
    # Read the top rows of each Excel file and store them in a dictionary
    top_rows = {}
    for file_path in excel_files:
        if file_path.lower().endswith('.csv'):
            df = pd.read_csv(file_path, nrows=1, header=None)
        else:
            df = pd.read_excel(file_path, header=None, nrows=1)
        top_rows[file_path] = df.values.tolist()[0]

    # Find the common top row among all files
    common_top_row = set(top_rows[list(top_rows.keys())[0]])
    for row in top_rows.values():
        common_top_row &= set(row)

    if len(common_top_row) == 0:
        print("No common top row found among the files.")
    else:
        # Merge the files based on the common top row
        merged_data = []
        non_matching_data = []
        for file_path in excel_files:
            if file_path.lower().endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path, skiprows=1)  # Skip the header row
            matching_rows = df[df.iloc[:, 0].isin(common_top_row)]
            non_matching_rows = df[~df.iloc[:, 0].isin(common_top_row)]
            merged_data.append(matching_rows)
            non_matching_data.append(non_matching_rows)

        # Concatenate the matching rows' dataframes vertically
        merged_df = pd.concat(merged_data, ignore_index=True)

        # Concatenate the non-matching rows' dataframes at the end
        non_matching_df = pd.concat(non_matching_data, ignore_index=True)

        # Append non-matching rows to the merged dataframe
        merged_df = pd.concat([merged_df, non_matching_df], ignore_index=True)

        # Save the merged dataframe to a new Excel file
        merged_output_path = "merged_output.xlsx"
        merged_df.to_excel(merged_output_path, index=False)

        print(f"Merged data saved to {merged_output_path}")
