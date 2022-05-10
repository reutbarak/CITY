################################################
# CITY project: Recommendation algorithm
# This file contains the algorithm built to recommend
# a city based on user preferences
################################################

import pandas as pd
import numpy as np



# constants

occupations_by_letter = {"A": "חקלאות,ייעור ודיג", "B-C": "תעשייה, כרייה וחציבה", "D": "אספקת חשמל", "E": "אספקת מים, שירותי ביוב וטיהור וטיפול", "F": "בינוי", "G": "מסחר סיטוני וקמעונאי ותיקון כלי רכב",
                         "H": "שירותי תחבורה, אחסנה, דואר ובלדרות", "I": "שירותי אירוח ואוכל", "J": "מידע ותקשורת", "K": "שירותים פיננססים ושירותי ביטוח", "L": "פעילויות בנדלן", "M": "שירותים מקצועיים, מדעיים וטכניים",
                         "N": "שירותי ניהול ותמיכה", "O": "מינהל מקומי, ציבורי וביטחון וביטוח לאומי", "P": "חינוך", "Q": "שירותי בריאות, רווחה וסעד", "R": "אמנות, בידור ופנאי", "S": "שירותים אחרים", "T": "משקי בית כמעסיקים"}


religion_by_num = {"יהודי":1, "לא יהודי":2, "שבט בדווי":3, "ישוב מעורב":4}
district_options = ["center", "jerusalem", "south", "north_west", "far_east_north"]
# parameters for calculation
parameters_for_algorithm = ['education_quality_measures', "education_success", "educated_population", 'Salary_norm', 'Internet_norm','nature_rate',
       'job_demands', 'pollution', 'crime_score_percent']
# # give these a negative weight in the algorithm
# neg_parameters_for_algorithm = ['avg_class_size', 'dropout_students_percent','avg_students_per_teacher',
#                                 'pollution', 'crime_score_percent']

# input: column
# output: normalized between 0-1, nan gets column mean value
def NormalizeData(data):
    data[np.isnan(data)] = np.nanmean(data)
    return (data - np.nanmin(data)) / (np.nanmax(data) - np.nanmin(data))

# input: The merged CITY dataset.
# output: only settlements in district pref. with religion pref.
#           only features relevant for calculation, normalized between 0-1
#           chosen parameters multiplied by their ranking after normalization
def generate_algorithm_table(religion_pref, district_pref, param1, param1_rank, param2, param2_rank,  param3, param3_rank):
    # read data
    # relative path
    CITY_merged_dataset = pd.read_csv(r"../Data/CITY_merged_dataset_09.csv", encoding="UTF-8",
                                      na_values=["..", "", "-"], index_col=0)
    # # absolute path
    # CITY_merged_dataset = pd.read_csv(PATH_data + "/CITY_merged_dataset_09.csv", encoding="UTF-8",
    #                                   na_values=["..", "", "-"], index_col = 0)
    CITY_merged_dataset["religion_num"] = [religion_by_num[rel] for rel in CITY_merged_dataset["religion"]]
    # normalize
    for col in parameters_for_algorithm:
        CITY_merged_dataset[col] = NormalizeData(CITY_merged_dataset[col].values)

    # reduce by district and religion
    if religion_pref != 0:
        algorithm_table = CITY_merged_dataset.loc[CITY_merged_dataset["religion_num"] == religion_pref, :]
    if district_pref != 0:
        algorithm_table = algorithm_table.loc[algorithm_table["large_district"] == district_pref, :]

    # reduce to calculation features
    algorithm_table = algorithm_table.loc[:, parameters_for_algorithm]

    # multiply selected parameters by their rank
    algorithm_table[param1] = algorithm_table[param1] * param1_rank**2
    algorithm_table[param2] = algorithm_table[param2] * param2_rank**2
    algorithm_table[param3] = algorithm_table[param3] * param3_rank**2
    return algorithm_table

def recommend_CITY(religion_pref, district_pref, param1, param1_rank, param2, param2_rank,  param3, param3_rank):
    # Consider in recommendation:
    # the three parameters and their rank
    # all other parameters with a smaller value
    # compute final score for each settlement, recommend first 1-3

    algorithm_table = generate_algorithm_table(religion_pref, district_pref,
                                               param1, param1_rank,
                                               param2, param2_rank,
                                               param3, param3_rank)
    # for col in neg_parameters_for_algorithm:
    #     algorithm_table[col] = algorithm_table[col]*-1
    # if algorithm_table.shape[0] == 0:
    #     return 0, 0
    algorithm_table["algorithm_score"] = algorithm_table.sum(axis=1)
    return algorithm_table['algorithm_score'].idxmax()
