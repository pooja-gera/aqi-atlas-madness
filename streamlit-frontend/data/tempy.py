import pandas as pd

# Load the Excel file
excel_file = pd.ExcelFile('AQI_history_MONTHYL.xlsx')

# Initialize an empty dictionary to store the processed data for each sheet
daily_data_dict = {}

# Iterate over each sheet in the Excel file
for sheet_name in excel_file.sheet_names:
    # Read the sheet into a DataFrame
    monthly_data = excel_file.parse(sheet_name)

    # Convert the 'DATE' column to datetime type if it's not already
    monthly_data['DATE'] = pd.to_datetime(monthly_data['DATE'])

    # Set the 'DATE' column as the index of the DataFrame
    monthly_data = monthly_data.set_index('DATE')

    # Resample the data to daily frequency and forward fill missing values
    daily_data = monthly_data.resample('D').ffill()

    # Reset the index to make 'DATE' a column again
    daily_data = daily_data.reset_index()

    # Store the processed data in the dictionary with the sheet name as the key
    daily_data_dict[sheet_name] = daily_data

# Save the processed data to a new Excel file
output_file = pd.ExcelWriter('daily_data.xlsx')
for sheet_name, daily_data in daily_data_dict.items():
    daily_data.to_excel(output_file, sheet_name=sheet_name, index=False)
output_file.save()
