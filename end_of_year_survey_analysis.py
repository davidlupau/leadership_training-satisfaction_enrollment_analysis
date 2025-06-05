import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
from functions import load_dataset, transform_categorical_to_numerical

# Company colors to be used for charts as per branding rules
# Blue, dark blue, light blue, green, violet, pink, orange
ppg_colors = ['#0078A9', '#0033A0', '#3EC7F4', '#00B149', '#8F1A95', '#D0006F', '#FFB81C']

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

# Computing ratings related to training impact
columns_to_mean = ['acquired_skills_mod_1',
                  'acquired_skills_mod_2',
                  'acquired_skills_mod_3',
                  'acquired_skills_mod_4',
                  'acquired_skills_mod_5',
                  'acquired_skills_mod_6',
]

i = 1
for col in columns_to_mean:
    mean = df[col].mean()
    print(f"Skills and tools of module {i} helped me to lead my team more efficiently: {round(mean, 2)}/5")
    i = i + 1

# Plotting results
# List to store means and module labels
module_means = []
module_labels = []

# Loop through columns and collect means
for i, col in enumerate(columns_to_mean, start=1):
    mean = df[col].mean()
    module_means.append(round(mean, 2))
    module_labels.append(f"Module {i}")

# Create a bar chart
plt.figure(figsize=(10, 5))
plt.bar(module_labels, module_means, color=ppg_colors[4])

plt.title("Average Rating: Skills Acquired are Useful by Module")
plt.xlabel("Module")
plt.ylabel("Average Rating (1–5)")
plt.ylim(0, 5)

# Add value labels on bars
for i, v in enumerate(module_means):
    plt.text(i, v + 0.1, str(v), ha='center', fontweight='bold')

plt.tight_layout()
plt.show()

# Computing average ratings related to logistics
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

# Plotting the results
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

# Computing average ratings according to participant guide availability
print("Participant satisfaction depending on participant's guide use/availability... \n")
columns_guide_impact = ['informed_rollout',
                        'info_received',
                        'easy_access_materials',
                        'easy_process_enrollment'
]

# Creating visualisation
# Group and calculate the mean
average_ratings_by_guide = df.groupby('participant_guide_useful')[columns_guide_impact].mean().round(2)

# Reset index to make 'participant_guide' a column again
average_ratings_by_guide = average_ratings_by_guide.reset_index()

# Melt the DataFrame to long format
melted_df = average_ratings_by_guide.melt(id_vars='participant_guide_useful',
                                           var_name='Question',
                                           value_name='Average Rating')

# Set plot style
sns.set(style="whitegrid")

# Set colors
color_df = pd.DataFrame({
    'ppg_colors': ['#3EC7F4', '#0033A0', '#00B149', '#FF7C13', '#D0006F']
})
custom_palette = color_df['ppg_colors'].tolist()

# Create the grouped bar plot
plt.figure(figsize=(12, 6))
sns.barplot(data=melted_df,
            x='Question',
            y='Average Rating',
            hue='participant_guide_useful',
            palette=custom_palette)

# Add labels and title
plt.title("Average Ratings by Participant Guide Usage", fontsize=14)
plt.xlabel("Survey Question", fontsize=12)
plt.ylabel("Average Rating (1–5)", fontsize=12)
plt.ylim(0, 5)
plt.xticks(rotation=45)
plt.legend(title="Used Participant Guide", bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.show()

# Correlation Matrix
# One hot encoding
print("One hot encoding participant_guide_useful column... \n")

# One hot encoding of participant_guide_useful into 2 features: used the guide, didn't use it
# Step 1: Create guide_used (1 if "Yes", else 0)
df['guide_used'] = df['participant_guide_useful'].apply(lambda x: 1 if x == "Yes" else 0)

# Step 2: Create guide_not_used (1 if not "Yes", else 0)
df['guide_not_used'] = df['participant_guide_useful'].apply(lambda x: 1 if x != "Yes" else 0)

# Dropping participant_guide_useful
df = df.drop(columns=['participant_guide_useful'])

# Creating an Excel file to visually check the output
df.to_excel('df_cleaned.xlsx', index=False)

print("One hot encoding completed \n")

# Generating and visualising matrix
correlation_matrix = df.corr(numeric_only=True)

plt.figure(figsize=(14, 10))
sns.heatmap(correlation_matrix,
            annot=True,
            cmap='coolwarm',
            vmin=-1,
            vmax=1,
            fmt=".2f",
            annot_kws={"size": 9})

plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.title("Correlation Matrix (All Numerical Columns)", fontsize=16)
plt.tight_layout()
plt.show()

# Comparing results by year
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