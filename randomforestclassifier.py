import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import subprocess

# Step 1: Load Data
df = pd.read_csv('analysis.csv')

# Step 2: Data Exploration
print(df.info())
print(df.describe())

# Step 3: Data Preprocessing
# Split the 'rgb' column into three separate columns
df[['r', 'g', 'b']] = df['rgb'].str.split(',', expand=True)

# Drop the original 'rgb' column and any other columns that are not needed for training
df = df.drop(['rgb', 'date', 'time'], axis=1)

# Convert the 'r', 'g', and 'b' columns to numeric
df[['r', 'g', 'b']] = df[['r', 'g', 'b']].apply(pd.to_numeric)

X = df.drop('working_status', axis=1)
y = df['working_status']

# Step 4: Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 5: Random Forest Model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Step 6: Feature Importance
feature_importances = pd.DataFrame(rf_model.feature_importances_, index=X.columns, columns=['Importance'])
feature_importances.sort_values(by='Importance', ascending=False, inplace=True)
print("Feature Importances:\n", feature_importances)

# Step 7: Analyze Correlations
correlation_matrix = df[['noise', 'brightness', 'r', 'g', 'b', 'working_status']].corr()
print("Correlation Matrix:\n", correlation_matrix)

# Use the highest importance for each feature as the threshold
working_status_1_thresholds = {}

for variable in ['noise', 'brightness', 'r', 'g', 'b']:
    mean_value = df[df['working_status'] == 1][variable].mean()
    min_value = df[df['working_status'] == 1][variable].min()
    max_value = df[df['working_status'] == 1][variable].max()

    lowest_threshold = mean_value - (mean_value - min_value) * 60 / 100
    highest_threshold = mean_value + (max_value - mean_value) * 60 / 100

    working_status_1_thresholds[variable] = (lowest_threshold, highest_threshold)
    print(f"Working Status 1 Thresholds for {variable.upper()}:\n", working_status_1_thresholds[variable])
# Example user's conditions
user_conditions = {'noise': 3.65, 'brightness': 63.57, 'r': 10, 'g': 91, 'b': 104}

# Check conditions against dynamic thresholds and provide feedback
best_working_conditions = []

# Brightness condition
if working_status_1_thresholds['brightness'][0] <= user_conditions['brightness'] <= working_status_1_thresholds['brightness'][1]:
    best_working_conditions.append("Maintain higher brightness levels for better focus.")
else:
    best_working_conditions.append("Maintain lower brightness levels for better focus.")

# Noise condition
if working_status_1_thresholds['noise'][0] <= user_conditions['noise'] <= working_status_1_thresholds['noise'][1]:
    best_working_conditions.append("Minimize noise levels for improved concentration.")
else:
    best_working_conditions.append("Increase noise levels for improved concentration.Put some music or white noise on.")

# RGB conditions
rgb_conditions = []
for color in ['r', 'g', 'b']:
    lower_bound, upper_bound = working_status_1_thresholds[color]
    if lower_bound <= user_conditions[color] <= upper_bound:
        rgb_conditions.append(f"{color.upper()} values are between ideal conditions.")
    elif user_conditions[color] < lower_bound:
        rgb_conditions.append(f"Increase {color.upper()}ish values for better focus.")
    elif user_conditions[color] > upper_bound:
        rgb_conditions.append(f"Decrease {color.upper()}ish values for better focus.")
    else:
        pass

# Combine conditions for display
all_conditions = best_working_conditions + rgb_conditions
print("\nUser's Best Working Conditions:")
for condition in all_conditions:
    print(condition)

# Step 7: Model Evaluation
y_pred = rf_model.predict(X_test)

print("\nModel Evaluation:")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
