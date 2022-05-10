################################################
# CITY project: Preprocess and Merge data
# This file contains extraction of CBS features
# as well as occupation features, nature proximity,
# crime rate and pollution created from other scripts.
# all data is merged into one dataframe (n = 175)
# features requiring integration and manipulation are
# preprocessed/engineered here.
################################################



import pandas as pd
import numpy as np
import itertools

import collections

# constants

occupations_by_letter = {"A": "חקלאות,ייעור ודיג", "B-C": "תעשייה, כרייה וחציבה", "D": "אספקת חשמל", "E": "אספקת מים, שירותי ביוב וטיהור וטיפול", "F": "בינוי", "G": "מסחר סיטוני וקמעונאי ותיקון כלי רכב",
                         "H": "שירותי תחבורה, אחסנה, דואר ובלדרות", "I": "שירותי אירוח ואוכל", "J": "מידע ותקשורת", "K": "שירותים פיננססים ושירותי ביטוח", "L": "פעילויות בנדלן", "M": "שירותים מקצועיים, מדעיים וטכניים",
                         "N": "שירותי ניהול ותמיכה", "O": "מינהל מקומי, ציבורי וביטחון וביטוח לאומי", "P": "חינוך", "Q": "שירותי בריאות, רווחה וסעד", "R": "אמנות, בידור ופנאי", "S": "שירותים אחרים", "T": "משקי בית כמעסיקים"}

religion_by_num = {1: "יהודי", 2: "לא יהודי", 3: "שבט בדווי", 4: "ישוב מעורב"}

# read tables, adjust column names
edu_table = pd.read_csv(r"../Data/education_2019_selected_features.csv", encoding="UTF-8", na_values = ["..", "", "-"])
# 201 settlements
edu_table.columns = ['settlement_num', 'settlement',
       'avg_class_size', # lower = better education conditions
       'dropout_students_percent', # lower = better education performances
       'bagrut_elig_percent', # higher = better education performances
        'academy_acceptance_elig_percent', # higher = better education performances
       'academy_grad_percent_35_55_age_group', # higher = more educated population
       'seniors_enter_academy_last_8_years', # higher = better education performances
       'students_in_population_percent', # higher = more educated population
       'education_workers_abs', # higher = better education conditions
       'education_workers_Wmaster_percent', # higher = better education conditions
       'avg_students_per_teacher', # lower = better education conditions
       'avg_teacher_hours_per_student'] # higher = better education conditions

# 176 settlements
economic_social_table = pd.read_csv(r"../Data/economic_social_small_final.csv", encoding="UTF-8", na_values = ["..", "", "-"])
economic_social_table.columns = ['settlement', 'edu_years_avg_norm', 'academy_manager_workers_norm',
       'academy_graduates_norm', 'Salary_norm', 'Internet_norm', 'work_10_norm',
       'periphery_value_norm']

# 89 settlements
pollution_table = pd.read_csv(r"../Data/israel_cities_air_pollution.csv", encoding="UTF-8", na_values = ["..", "", "-"])
pollution_table.columns = ["settlement", "value_of_pollution"]

# for pollution: choose max pollution value for each settlement
pollution_table_unique = pd.DataFrame(set(pollution_table["settlement"]))
pollution_table_unique.columns = ["settlement"]
pollution_table_unique["pollution"] = 0
pollution_table_unique.index = pollution_table_unique["settlement"]
for stlmt in pollution_table_unique["settlement"]:
    pollution_table_unique.loc[stlmt, "pollution"] = np.max(pollution_table.loc[pollution_table["settlement"] == stlmt, "value_of_pollution"])

# 1482 settlements
settlement_district_population_religion_altitude_coord = pd.read_csv(r"../Data/settlements_population_district_religion_altitude_coordinates.csv", encoding="UTF-8", na_values=["..", "", "-"])
settlement_district_population_religion_altitude_coord.columns = ["settlement", "settlement_num", "district",
                                                                  "dist_num", "religion_num", "overall_population_2020",
                                                                  "coordinates", "altitude_avg"]

# 257 settlements
crime_table = pd.read_csv(r"../Data/Crime-map-2021_minimized.csv", encoding="UTF-8", na_values = ["..", "", "-"])
crime_table.columns = ["settlement", "crime_score_abs"]

# 175 settlements
job_demand_table = pd.read_csv(r"../Data/job_demands_jobmaster_co_il.csv", encoding="UTF-8", na_values = ["..", "", "-"])


# occupation per district table
occupation_district_table = pd.read_csv(r"../Data/occupation_by_district_israel.csv", encoding="UTF-8",
                                        na_values = ["..", "", "-", "..  ", "-  "])
occupation_district_table.columns = ['T', 'S', 'R', 'Q', 'P', 'O', 'N', 'M', 'L', 'K', 'J', '  I', '  H',
       'G', 'F', 'E', 'D', 'B-C', 'A', 'overall_Thousands', 'district_name']

# district name to district number (for merge)
district_numbers_table = pd.read_csv(r"../Data/settlement_to_district.csv")
district_numbers_table.columns = ["district_name", "dist_num"]

# Proximity to nature
nature_table = pd.read_csv(r"../Data/nature_rate.csv", encoding="UTF-8", na_values = ["..", "", "-"])
nature_table.columns = ["settlement", "nature_rate"]

# input: column
# output: normalized between 0-1, nan gets column mean value
def NormalizeData(data):
    data[np.isnan(data)] = np.nanmean(data)
    return (data - np.nanmin(data)) / (np.nanmax(data) - np.nanmin(data))

def remove_redundant_chars(stlmt):
    return stlmt.replace(" ", "").replace("י", "").replace("ו", "").replace(".", "").replace("-", "").replace("*", "").replace("(", "").replace(")", "").replace("'", "").replace("\"", "")
# Merge data

# create dummy variable to reduce settlement name to its core.
# used for merging, to allow greatest possible intersections
edu_table["stlmt_temp"] = [remove_redundant_chars(stlmt) for stlmt in edu_table["settlement"]]
economic_social_table["stlmt_temp"] = [remove_redundant_chars(stlmt) for stlmt in economic_social_table["settlement"]]
economic_social_table=economic_social_table.drop(columns=["settlement"])
crime_table["stlmt_temp"] = [remove_redundant_chars(stlmt) for stlmt in crime_table["settlement"]]
crime_table=crime_table.drop(columns=["settlement"])
pollution_table_unique["stlmt_temp"] = [remove_redundant_chars(stlmt) for stlmt in pollution_table_unique["settlement"]]
pollution_table_unique=pollution_table_unique.drop(columns=["settlement"])

# check intersection of different dataframes
# i=0
# j=0
# for df in [crime_table, pollution_table_unique, economic_social_table, edu_table, nature_table]:
#     i += 1
#     for df2 in [crime_table, pollution_table_unique, economic_social_table, edu_table, nature_table]:
#         j +=1
#         if j <= i: continue
#         print("dfs: " + str(i) + ", " + str(j) + ": " + str(len([stlmt for stlmt in df2["stlmt_temp"].values if stlmt in df["stlmt_temp"].values])))
#     j = 0


# Merge dataframes
merged_df = pd.merge(edu_table, economic_social_table, left_index=False, right_index=False, on="stlmt_temp", how= "left")
merged_df = pd.merge(merged_df, crime_table, left_index=False, right_index=False, on="stlmt_temp", how= "left")
merged_df = pd.merge(merged_df, pollution_table_unique, left_index=False, right_index=False, on="stlmt_temp", how= "left")
merged_df = pd.merge(merged_df, settlement_district_population_religion_altitude_coord, left_index=False, right_index=False, on="settlement", how= "inner")
print(set(merged_df.isnull().sum(axis=1)))
print(sum(merged_df.isnull().sum(axis=1)>7))
# remove settlements with too many missing values
merged_df = merged_df.loc[merged_df.isnull().sum(axis=1)<8,:]


# give these a negative weight in the algorithm
neg_parameters_for_algorithm = ['avg_class_size', 'dropout_students_percent','avg_students_per_teacher',
                                'pollution', 'crime_score_percent']
### Data adjustments and engineering
# combine education scores with high correlations
edu_features = ['bagrut_elig_percent',
       'academy_acceptance_elig_percent', 'academy_grad_percent_35_55_age_group',
       'seniors_enter_academy_last_8_years', 'students_in_population_percent', 'academy_manager_workers_norm',
       'education_workers_Wmaster_percent', 'avg_teacher_hours_per_student', 'edu_years_avg_norm',
       'academy_graduates_norm', 'avg_class_size', 'dropout_students_percent','avg_students_per_teacher']

# engineering education features
edu_df = merged_df.loc[:,edu_features]
for col in edu_features:
    edu_df[col] = NormalizeData(edu_df[col].values)
merged_df["education_quality_measures"] = (-1)*edu_df['avg_students_per_teacher'] + edu_df['avg_teacher_hours_per_student'] + (-1)*edu_df['avg_class_size']+edu_df['education_workers_Wmaster_percent']
merged_df["education_success"] = edu_df['seniors_enter_academy_last_8_years']+edu_df['academy_acceptance_elig_percent']+(-1)*edu_df['dropout_students_percent']+edu_df['bagrut_elig_percent']
merged_df["educated_population"] = edu_df['academy_grad_percent_35_55_age_group']+edu_df['students_in_population_percent']+edu_df['edu_years_avg_norm'] + edu_df['academy_graduates_norm'] + edu_df['academy_manager_workers_norm']

# Adjust crime score using population size
# crime preprocessing of cases for each city was calculated in
merged_df["crime_score_percent"] = merged_df.crime_score_abs/merged_df.overall_population_2020*100
# Change religion from number to string
merged_df["religion"] = merged_df.replace({"religion_num":religion_by_num})["religion_num"].values

# Occupation per district
occupation_district_table.index = range(occupation_district_table.shape[0])
occupation_district_table.replace(np.nan, 0)
merged_df = pd.merge(merged_df, district_numbers_table, left_index=False, right_index=False, on="dist_num")
merged_df = pd.merge(merged_df, occupation_district_table,  left_index=False, right_index=False, on="district_name")

# nature proximity, job demand tables (see different code files for extraction methodology)
merged_df = pd.merge(merged_df, nature_table, left_index=False, right_index=False, on="settlement", how= "left")
merged_df = pd.merge(merged_df, job_demand_table, left_index=False, right_index=False, on="settlement", how= "left")


# put settlement as index, remove unnecessary columns and save to csv
merged_df.index = merged_df.settlement
# remove unnecessary columns
merged_df = merged_df.drop(columns=['settlement', 'stlmt_temp','periphery_value_norm', 'crime_score_abs', 'coordinates', 'settlement_num_y', 'district',
                        'overall_Thousands'])
# for occupation collumns- if there's no value, consider as 0
merged_df.iloc[:,27:46] = merged_df.iloc[:,27:46].fillna(0)

# check ourselves
# print(set(merged_df.isnull().sum(axis=1)))
# print(merged_df.isnull().sum(axis=0))

# calculate log of population, to reduce effect of population size extremeties
merged_df["log_population"] = np.log(merged_df.overall_population_2020)

# to fit crime feature:
modified_cols = [str(col).replace(" ", "") for col in merged_df.columns]
merged_df.columns = modified_cols
merged_df = merged_df.drop("דאלית אל-כרמל")
merged_df = merged_df.sort_values("overall_population_2020", ascending=False)

# get key if value is in list of large_districts dictionary
def get_key(val):
    for key, value_list in large_districts.items():
         if val in value_list:
             return key

large_districts = {"center":["פתח תקווה", "השרון","רחובות","רמלה","תל אביב"], "south":["אשקלון", "באר שבע"],
                   "jerusalem":["יהודה ושומרון", "ירושלים"], "north_west":["חדרה", "חיפה", "עכו"],
                   "far_east_north":["גולן", "כנרת","צפת","יזרעאל"]}
merged_df["large_district"] = [get_key(dist) for dist in merged_df["district_name"]]



merged_df.to_csv(r"../Data/CITY_merged_dataset_09.csv" ,encoding="utf-8-sig")
# check for NAN values for every settlement


print("done")



