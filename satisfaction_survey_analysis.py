import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
import statistics
from functions import transform_categorical_to_numerical, load_dataset

# Setting color palette to match company's branding rules
ppg_colors = ['#0078A9', '#0033A0', '#3EC7F4', '#00B149', '#8F1A95', '#D0006F', '#FFB81C']

# Load dataset into dataframe
file_name = 'satisfaction_survey_results.xlsx'
df = load_dataset(file_name)

# Removing useless columns
columns_to_remove = [
    "year", "language", "region", "comments"
]
print("\nRemoving non-essential columns... \n")
df = df.drop(columns=columns_to_remove)
print("Columns removed \n")

print("Replacing categorical values by numerical values... \n")
mapping = {
    'Strongly disagree': 1,
	'Disagree': 2,
	'Neutral': 3,
	'Agree': 4,
	'Strongly agree': 5,
	'I didn\'t attend this module': np.nan,
}

columns_to_map = ['acquired_skills_mod_1',
                  'acquired_skills_mod_2',
                  'acquired_skills_mod_3',
                  'acquired_skills_mod_4',
                  'acquired_skills_mod_5',
                  'acquired_skills_mod_6',
                  'informed_rollout',
                  'info_received',
                  'easy_access_materials',
                  'easy_process_enrollment'
]

for col in columns_to_map:
    transform_categorical_to_numerical(df, col, mapping)

print("Numerical values transformed... \n")

columns_to_mean = ['informed_rollout',
                   'info_received',
                   'easy_access_materials',
                   'easy_process_enrollment',
]

i = 0
for col in columns_to_mean:
    mean = df[col].mean()
    print(f"Average rating for {columns_to_mean[i]}: {round(mean, 2)}/5")
    i = i + 1

# List to store means and labels
logistic_means = []
logistic_labels = []

# Loop through columns and collect means
for i, col in enumerate(columns_to_mean, start=0):
    mean = df[col].mean()
    logistic_means.append(round(mean, 2))
    logistic_labels.append(f"{columns_to_mean[i]}")

# Create a bar chart
plt.figure(figsize=(10, 5))
plt.bar(logistic_labels, logistic_means, color=ppg_colors[5])

plt.title("Average Rating: Learning experience around the classes")
plt.ylabel("Average Rating (1–5)")
plt.ylim(0, 5)

# Add value labels on bars
for i, v in enumerate(logistic_means):
    plt.text(i, v + 0.1, str(v), ha='center', fontweight='bold')

plt.tight_layout()
plt.show()