################################################
# This file is a program for creating an open
# paragraph of a city that present the data
# that was collected on the city, and several
# fact on the city, using data mining tool.
################################################
import pandas as pd

################ constans ######################
CITY_MERGED_DF_PATH = f'./data/CITY_merged_dataset_07'
CITIES_PARAGRAPH_PATH = f'./cities_paragraph/'


def data_explanation(df, curr_city):
    """
    a method for creating a paragraph on the current city, using all the data we have collected.
    :param df: DataFrame of the cities characteristics.
    :param curr_city: the current chosen city to write the paragraph on
    :return: index of the city in the df and the text describes it.
    """
    # params = ['overall_population_2020', 'district_name', 'job_demands', 'nature_rate', 'pollution']
    textual_rate = ['גבוהה', 'בינונית', 'נמוכה']
    nature, job, pollution, crime = '', '', '', ''
    # get the city index
    index = df.index
    condition = df['settlement'] == curr_city
    city_idx = index[condition].tolist()[0]

    # get the textual level of the city in parameters: nature_rate, pollution, crime
    df_nature = df['nature_rate'][city_idx]
    if df_nature < 1:
        nature = textual_rate[2]
    elif df_nature > 2:
        nature = textual_rate[0]
    else:
        nature = textual_rate[1]

    mean_pollution = df['pollution'].mean(skipna=True)
    if df['pollution'][city_idx]:  # not NaN
        if df['pollution'][city_idx] > mean_pollution:
            pollution = textual_rate[0]
        else:
            pollution = textual_rate[2]
    if df['crime_score_percent'][city_idx]:
        normalize_crime = (df['crime_score_percent'] - df['crime_score_percent'].min(skipna=True)) / (
                    df['crime_score_percent'].max(skipna=True) - df['crime_score_percent'].min(skipna=True))
    if normalize_crime[city_idx] > 2 / 10:
        crime = textual_rate[0]
    elif normalize_crime[city_idx] < 1 / 10:
        crime = textual_rate[2]
    else:
        crime = textual_rate[1]
    # get the most demanding occupation
    job_letters = ['A', 'B-C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']
    job_titles = ['חקלאות,ייעור ודיג', 'תעשייה, כרייה וחציבה', 'אספקת חשמל', 'אספקת מים, שירותי ביוב וטיהור וטיפול',
                  'בינוי',
                  'מסחר סיטוני וקמעונאי ותיקון כלי רכב', 'שירותי תחבורה, אחסנה, דואר ובלדרות', 'שירותי אירוח ואוכל',
                  'מידע ותקשורת', 'שירותים פיננססים ושירותי ביטוח', 'פעילויות בנדלן',
                  'שירותים מקצועיים, מדעיים וטכניים',
                  'שירותי ניהול ותמיכה', 'מינהל מקומי, ציבורי וביטחון וביטוח לאומי', 'חינוך',
                  'שירותי בריאות, רווחה וסעד',
                  'אמנות, בידור ופנאי', 'שירותים אחרים', 'משקי בית כמעסיקים']
    max_job_demand = 0
    i = -1
    for letter in job_letters:
        if df[letter][city_idx] > max_job_demand:
            max_job_demand = df[letter][city_idx]
            i += 1
    job = job_titles[i]

    # combine the paragraph
    text_to_return = curr_city + f" היא עיר במחוז " + df['district_name'][city_idx] + ", המונה כ-" + str(
        df['overall_population_2020'][
            city_idx]) + " תושבים." + "\n" + " לפי הנתונים שאספנו, תחום העבודה המבוקשת ביותר ב" + curr_city + " היא " + job + ". \n"
    if len(crime) > 0:
        text_to_return += curr_city + " נמנית בדרגת פשיעה " + crime + ". \n"
    text_to_return += "קרבתה לאזורי טבע היא " + nature + ". \n"
    if len(pollution) > 0:
        text_to_return += "רמת זיהום האוויר בעיר היא " + pollution
    return city_idx, text_to_return


if __name__ == '__main__':
    df = pd.read_csv(f'{CITY_MERGED_DF_PATH}.csv', encoding="utf8")
    for city in df.loc[:, 'settlement']:
        city_idx, text = data_explanation(df, city)
        with open(CITIES_PARAGRAPH_PATH + str(df.iloc[city_idx, 1]) + '_paragraph.txt', 'w', encoding="utf-8") as f:
            f.write(text)
