import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
from functions import load_dataset, transform_categorical_to_numerical

# Company colors to be used for charts as per branding rules
# Blue, dark blue, light blue, green, violet, pink, orange
ppg_colors = ['#0078A9', '#0033A0', '#3EC7F4', '#000B149', '#8F1A95', '#D0006F', '#FFB81C']

# Loading dataset
def load_dataset(file_name):
    print("Loading data... \n")
    if os.path.exists(file_name):
        try:
            df = pd.read_excel(file_name)
            print("Data loaded successfully.")
            return df
        except Exception as e:
            print(f"Error loading file: {e}")
            return None
    else:
        print("File not found")
        return None

file_name = 'end_of_year_participants_feedback.xlsx'
df = load_dataset(file_name)

# Preparing dataset for analysis
# Removing useless columns
columns_to_remove = [
    "language", "comments"
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

# Columns to compare across years
columns_to_compare = [
    'acquired_skills_mod_1',
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

# Group by year and calculate the mean for the selected columns
yearly_comparison = df.groupby('year')[columns_to_compare].mean().round(2)

# Display the comparison table
print("\nAverage Ratings by Year:\n")
print(yearly_comparison)

# Transpose for plotting (years as bars, questions as x-axis)
plot_df = yearly_comparison.T

# Set colors
color_df = pd.DataFrame({
    'ppg_colors': ['#3EC7F4', '#00B149', '#D0006F']
})
custom_palette = color_df['ppg_colors'].tolist()

# Plot
plot_df.plot(kind='bar', figsize=(14, 6), color=custom_palette)

plt.title("Average Ratings per Question by Year", fontsize=14)
plt.ylabel("Average Rating (1–5)")
plt.xlabel("Question")
plt.ylim(0, 5)
plt.xticks(rotation=45)
plt.legend(title="Year", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
