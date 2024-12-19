import pandas as pd
from google.colab import drive

# Mount Google Drive
drive.mount('/content/drive')

# Load the spreadsheet
df = pd.read_excel('/content/drive/MyDrive/Book1.xlsx')

# Display the first few rows to understand the structure
print(df.head())

# Replace 'Citizenship', 'Gender', 'Cohort', 'Disability', and 'Area' with the actual column names from your spreadsheet
citizenship_column = 'Citizenship'  # Replace with the actual column name for citizenship
gender_column = 'Gender'  # Replace with the actual column name for gender
cohort_column = 'Cohort'  # Replace with the actual column name for cohort
disability_column = 'Disability'  # Replace with the actual column name for disability
area_column = 'Area'  # Replace with the actual column name for area

# Convert the 'Disability' column to lowercase and ensure all 'yes' values are consistent
df[disability_column] = df[disability_column].str.lower().replace({'yes': 'yes', 'YES': 'yes'})
df[gender_column] = df[gender_column].str.lower().replace({'female:female', 'FEMALE:female', 'male:male', 'MALE:male'})

# Split the Area column into Kampala_column and Nakivale_column with counts
df['Kampala_column'] = df[area_column].apply(lambda x: 1 if x == 'Kampala' else 0)
df['Nakivale_column'] = df[area_column].apply(lambda x: 1 if x == 'Nakivale' else 0)

"""#Split gender column into male and female with columns
#df['Male_column'] = df[gender_column].apply(lambda x: 1 if x == 'male' else 0)
#df['Female_column'] = df[gender_column].apply(lambda x: 1 if x == 'female' else 0)

#SPlit cohort column into 1, 2, 3, 4 with their columns
df['cohort1_column'] = df[cohort_column].apply(lambda x: 1 if x == 'cohort 1' else 0)
df['cohort2_column'] = df[cohort_column].apply(lambda x: 1 if x == 'cohort 2' else 0)
df['cohort3_column'] = df[cohort_column].apply(lambda x: 1 if x == 'cohort 3' else 0)
df['cohort4_column'] = df[cohort_column].apply(lambda x: 1 if x == 'cohort 4' else 0)"""


# Display the DataFrame with new columns
print("\nDataFrame with split Area columns and counts:")
print(df.head())

# Group the data by citizenship, gender, cohort, and area columns to get the total counts
total_grouped_data = df.groupby([citizenship_column, gender_column, cohort_column, 'Kampala_column', 'Nakivale_column']).size().reset_index(name='Total Count')

# Group the data by citizenship, gender, cohort, area columns, and disability to get the counts of disabled individuals
disability_grouped_data = df[df[disability_column] == 'yes'].groupby([citizenship_column, gender_column, cohort_column, 'Kampala_column', 'Nakivale_column']).size().reset_index(name='Disability Count')

# Merge the total counts with disability counts
merged_data = pd.merge(total_grouped_data, disability_grouped_data, on=[citizenship_column, gender_column, cohort_column, 'Kampala_column', 'Nakivale_column'], how='left')

# Replace NaN values with 0 in the Disability Count column
merged_data['Disability Count'] = merged_data['Disability Count'].fillna(0)

# Calculate the count of individuals without disabilities
merged_data['Without Disability Count'] = merged_data['Total Count'] - merged_data['Disability Count']

# Print the merged data
print("Grouped data by citizenship, gender, cohort, area, with disability and without disability counts:")
print(merged_data)

# Calculate the overall totals
overall_totals = {
    citizenship_column: 'Total',
    gender_column: '',
    cohort_column: '',
    """'cohort1_column': merged_data['cohort1_column'].sum(),
    'cohort2_column': merged_data['cohort2_column'].sum(),
    'cohort3_column': merged_data['cohort3_column'].sum(),
    'cohort4_column': merged_data['cohort4_column'].sum(),
    'Male_column': merged_data['Male_column'].sum(),
    'Female_column': merged_data['Female_column'].sum(),"""
    'Kampala_column': merged_data['Kampala_column'].sum(),
    'Nakivale_column': merged_data['Nakivale_column'].sum(),
    'Total Count': merged_data['Total Count'].sum(),
    'Disability Count': merged_data['Disability Count'].sum(),
    'Without Disability Count': merged_data['Without Disability Count'].sum()
}

# Append the overall totals to the merged data
merged_data = pd.concat([merged_data, pd.DataFrame([overall_totals])], ignore_index=True)

# Print the merged data with overall totals
print("Grouped data by citizenship, gender, cohort, area, with disability and without disability counts, including overall totals:")
print(merged_data)

# Save the merged data to a new Excel file
merged_data.to_excel('NEW_merged_data_with_disability_and_without_counts_with_totals.xlsx', index=False)
