import pandas as pd

# Read the existing CSV file into a DataFrame if it exists
try:
    existing_df = pd.read_csv('modified_file.csv')
except FileNotFoundError:
    existing_df = pd.DataFrame()

try:
    analysis_df = pd.read_csv('analysis.csv')
except FileNotFoundError:
    analysis_df = pd.DataFrame()

# Read the new CSV file into a DataFrame
new_df = pd.read_csv('results.csv')

# Check for existing data and append only new rows
if not existing_df.empty:
    new_rows = new_df[~new_df['timestamp'].isin(existing_df['timestamp'])]
    existing_df = pd.concat([existing_df, new_rows], ignore_index=True)
else:
    existing_df = new_df

# Separate timestamp into date and time columns
existing_df['date'] = pd.to_datetime(existing_df['timestamp']).dt.date
existing_df['time'] = pd.to_datetime(existing_df['timestamp']).dt.time


# Drop the specified columns
columns_to_remove = ['mouse_click', 'keyboard_log', 'eye_tracking', 'app_info']
existing_df = existing_df.drop(columns=columns_to_remove)

# Save the modified DataFrame back to a CSV file
existing_df.to_csv('modified_file.csv', index=False)

# Drop the original timestamp column
analysis_df= existing_df.drop(columns=['timestamp'])

# Save the modified DataFrame back to a CSV file
analysis_df.to_csv('analysis.csv', index=False)