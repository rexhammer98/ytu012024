import pandas as pd
import os
import tkinter as tk
from questioner import ask_question
from datetime import datetime, timedelta


def update_condition_threshold(condition_name, new_threshold):
    # Check if the condition exists in the DataFrame
    if condition_name in condition_thresholds_df.index:
        condition_thresholds_df.loc[condition_name, 'threshold'] = new_threshold
        condition_thresholds_df.to_csv(condition_thresholds_path, index=True)  # Save the updated DataFrame to the CSV file
        print(f"Threshold for {condition_name} updated to {new_threshold} seconds.")
    else:
        print(f"Condition {condition_name} not found in the thresholds DataFrame.")


def get_max_threshold(condition_thresholds_df):
    # Get the maximum threshold level from the condition_thresholds_df
    return max(condition_thresholds_df['threshold'])


# Function to get input for user
def get_user_input(start_time, end_time, condition_name):
    return input(
        f"Between {start_time} and {end_time}, did you work on {condition_name}? (Distracted/Working): ").strip().capitalize()


# Function to handle conditions
def handle_condition(condition_start, condition_end, condition_threshold, df, user_input_col, user_input,
                     condition_name):
    if condition_start is not None and condition_end - condition_start >= condition_threshold:
        question_main = f"Between {df.loc[condition_start, 'timestamp']} and {df.loc[condition_end, 'timestamp']}, {user_input} (1/0): "
        print(question_main)
        user_answer = ask_question(question_main)
        if user_answer == 1:
            update_condition_threshold(condition_name, int(condition_threshold*6/5))
        else:
            update_condition_threshold(condition_name, int(condition_threshold*4/5))

        df.loc[condition_start:condition_end, user_input_col] = user_answer
# Assuming you have your data in a CSV file
csv_file_path = 'output.csv'
df = pd.read_csv(csv_file_path)

# Load or initialize condition thresholds from/to a CSV file
condition_thresholds_path = 'condition_thresholds2.csv'
try:
    condition_thresholds_df = pd.read_csv(condition_thresholds_path, index_col='condition')
except FileNotFoundError:
    # If the file doesn't exist, create a new DataFrame with default values
    condition_thresholds_df = pd.DataFrame({'condition': ['condition1', 'condition2', 'condition3'],
                                            'threshold': [15, 15, 15]})
    condition_thresholds_df.set_index('condition', inplace=True)

    condition_thresholds_df.to_csv(condition_thresholds_path)


# Add a column for working_status
df['working_status'] = '1'

# Initialize variables for each condition
condition1_start = None
condition1_end = None

condition2_start = None
condition2_end = None

condition3_start = None
condition3_end = None

# Load the last processed timestamp from a file
last_processed_timestamp_path = 'last_processed_timestamp.txt'

try:
    with open(last_processed_timestamp_path, 'r') as file:
        last_processed_timestamp = pd.to_datetime(file.read(), format='%Y-%m-%d %H:%M:%S')
except FileNotFoundError:
    # If the file doesn't exist, set the last processed timestamp to the beginning of time
    last_processed_timestamp = pd.to_datetime('1970-01-01 00:00:00', format='%Y-%m-%d %H:%M:%S')

# Iterate through the DataFrame
for index, row in df.iterrows():
    # Skip rows that have been processed before
    if pd.to_datetime(row['timestamp']) <= last_processed_timestamp:
        continue

    # Condition 1: If the user is not working on ChatGPT, PyCharm, and LinkedIn more than the maximum threshold level seconds
    apps_of_interest = ['python', 'pycharm', 'linkedin', 'openai', 'word', 'notlar']
    app_names =row['app_info'].lower().replace(" ", "")
    if index > 0 and index < len(df) and any(app.lower().replace(" ", "") in app_names for app in apps_of_interest):
        condition1_start, condition1_end = None, None
    else:
        if condition1_start is None:
            condition1_start = index
        condition1_end = index

        if index == len(df) - 1 or any(
                app.lower().replace(" ", "") in df.loc[index + 1, 'app_info'].lower().replace(" ", "") for app in
                apps_of_interest):
            # Only ask the question if the next row is an app of interest or it's the last row
            question1 = f"You are using {', '.join(row['app_info'].split(','))}. Are you working?"
            handle_condition(condition1_start, condition1_end, condition_thresholds_df.loc['condition1', 'threshold'],
                             df,
                             'working_status', question1, 'condition1')
            condition1_start, condition1_end = None, None

    # Condition 2: If the user didn't change current_app AND didn't click AND didn't press any key on keyboard for the maximum threshold level seconds
    if index > 0 and index < len(df) and row['app_info'] == df['app_info'].iloc[index - 1] and row['mouse_click'] == 0 and row[
        'keyboard_press'] == 0:
        if condition2_start is None:
            condition2_start = index
        condition2_end = index

    else:
        question2 = f"You are looking at the screen and doing nothing for a while. Are you working? Using {', '.join(row['app_info'].split(','))} right now."
        handle_condition(condition2_start, condition2_end, condition_thresholds_df.loc['condition2', 'threshold'], df, 'working_status', question2, 'condition2')
        condition2_start = None
        condition2_end = None

    # Condition 3: If the user didn't click AND didn't press any key on keyboard AND is not in front of the laptop more than the maximum threshold level seconds
    if index > 0 and index < len(df) and row['mouse_click'] == 0 and row['keyboard_press'] == 0 and row['eye_tracking'] == 0:
        if condition3_start is None:
            condition3_start = index
        condition3_end = index
    else:
        question3 = f"You are away for a long time. Are you there and working? Using {', '.join(row['app_info'].split(','))} right now."
        handle_condition(condition3_start, condition3_end, condition_thresholds_df.loc['condition3', 'threshold'], df, 'working_status', question3 , 'condition3')
        condition3_start = None
        condition3_end = None

# After processing the data, update the last processed timestamp
new_last_processed_timestamp = pd.to_datetime(df['timestamp']).max()
  # Assuming your timestamp column is named 'timestamp'

# Save the new last processed timestamp to the file
with open(last_processed_timestamp_path, 'w') as file:
    file.write(new_last_processed_timestamp.strftime('%Y-%m-%d %H:%M:%S'))

# Save the updated condition thresholds to the CSV file
condition_thresholds_df.reset_index().to_csv(condition_thresholds_path, index=False)

# Append the new results to an existing CSV file
output_csv_path = 'results.csv'

if not os.path.exists(output_csv_path):
    # Create headers and write to results.csv
    headers = ["timestamp", "mouse_click", "keyboard_log", "eye_tracking", "app_info", "noise", "rgb", "brightness", "working_status"]
    pd.DataFrame(columns=headers).to_csv(output_csv_path, index=False)
elif pd.read_csv(output_csv_path, nrows=0).empty:
    # If results.csv exists but doesn't have headers, add headers
    headers = ["timestamp", "mouse_click", "keyboard_log", "eye_tracking", "app_info", "noise", "rgb", "brightness", "working_status"]
    pd.DataFrame(columns=headers).to_csv(output_csv_path, index=False, mode='a', header=False)
else:
    pass

df.to_csv(output_csv_path, mode='a', header=False, index=False)

print(f"Results appended to: {output_csv_path}")
