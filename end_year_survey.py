import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
from functions import transform_categorical_to_numerical

# Load dataset into dataframe
print("Loading data... \n")
if os.path.exists('end_of_year_participants_feedback.xlsx'):
    try:
        df = pd.read_excel('end_of_year_participants_feedback.xlsx')
        print("Data loaded successfully.")
    except Exception as e:
        print(f"Error loading file: {e}")
else:
    print("File not found")

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

# Calculating average ratings according to participant guide availability
print("Participant satisfaction depending on participant's guide use/availability... \n")
columns_guide_impact = ['informed_rollout',
                        'info_received',
                        'easy_access_materials',
                        'easy_process_enrollment'
]

# Creating visualisation
# Group and calculate the mean as before
average_ratings_by_guide = df.groupby('participant_guide_useful')[columns_guide_impact].mean().round(2)

# Reset index to make 'participant_guide' a column again
average_ratings_by_guide = average_ratings_by_guide.reset_index()

# Melt the DataFrame to long format
melted_df = average_ratings_by_guide.melt(id_vars='participant_guide_useful',
                                           var_name='Question',
                                           value_name='Average Rating')

# Set plot style
sns.set(style="whitegrid")

# Create the grouped bar plot
plt.figure(figsize=(12, 6))
sns.barplot(data=melted_df,
            x='Question',
            y='Average Rating',
            hue='participant_guide_useful',
            palette='Set2')

# Add labels and title
plt.title("Average Ratings by Participant Guide Usage", fontsize=14)
plt.xlabel("Survey Question", fontsize=12)
plt.ylabel("Average Rating (1–5)", fontsize=12)
plt.ylim(0, 5)
plt.xticks(rotation=45)
plt.legend(title="Used Participant Guide")

plt.tight_layout()
#plt.show()

print(df['participant_guide_useful'].mean().round(2))