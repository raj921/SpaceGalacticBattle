import pandas as pd

# Load the file
cps_df = pd.read_csv('cps.csv')

# Create a function from "Grades_Offered_All" column
cps_df['Lowest_Grade'] = cps_df['Grades_Offered_All'].apply(lambda x: x.split(',')[0].strip()[0] if x.split(',')[0].strip()[0].isdigit() else 'PK')

# Extract the highest grade without using a function
cps_df['Highest_Grade'] = cps_df['Grades_Offered_All'].str.findall(r'(\d+)').apply(lambda x: max([int(grade) for grade in x]) if x else None)

# For each column, substitute the mean instead of missing numerical values.
cps_df['College_Enrollment_Rate_School'].fillna(cps_df['College_Enrollment_Rate_School'].mean(), inplace=True)
cps_df['Student_Count_Total'].fillna(cps_df['Student_Count_Total'].mean(), inplace=True)

# Starting Hour to integer conversion
cps_df['School_Start_Hour'] = cps_df['School_Hours'].str.extract(r'(\d+)').astype(float)

# Create a new DataFrame
cps_df_filtered = cps_df[['School_ID', 'Short_Name', 'Is_High_School', 'Zip', 'Student_Count_Total',
                      'College_Enrollment_Rate_School', 'Lowest_Grade', 'Highest_Grade', 'School_Start_Hour']]

pd.set_option('display.width', None)

# Display all columns in the filtered DataFrame in a single line
print(cps_df_filtered.head(9))

# Average and standard deviation of high school students' college enrollment rates
mean = cps_df_filtered[cps_df_filtered['Is_High_School'] == True]['College_Enrollment_Rate_School'].mean()
count_std = cps_df_filtered[cps_df_filtered['Is_High_School'] == True]['College_Enrollment_Rate_School'].std()

# Student_Count_Total average and standard deviation for non-high schools
student_count_mean = cps_df_filtered[cps_df_filtered['Is_High_School'] == False]['Student_Count_Total'].mean()
student_count_std = cps_df_filtered[cps_df_filtered['Is_High_School'] == False]['Student_Count_Total'].std()

# beginning times for all schools distributed
starting_hours_distribution = cps_df_filtered['School_Start_Hour'].value_counts()

exclude_zip = ['60601', '60602', '60603', '60604', '60605', '60606', '60607', '60616']

# Number of schools outside of the Loop Neighborhood, excluding specified zip codes
schools_outside_loop = df_filtered[~df_filtered['Zip'].astype(str).isin(exclude_zip)].shape[0]



# Display the  information
print(f"College Enrollment Rate for high schools = {mean:.2f} (sd={count_std:.2f})")
print(f"Total Student_Count_Total for non-high schools = {student_count_mean:.2f} (sd={count_std:.2f})")
print("Distribution of starting hours for all schools:")
print(starting_hours_distribution)
print(f"Number of schools outside Loop = {schools_outside_loop}")
