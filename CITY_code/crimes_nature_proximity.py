################################################
# This file contain methods that help creating
# the rates for two of the data arguments in
# the city-recommendation tool, in particular,
# method for rating the city by the number
# of crimes that recorded in it (in 2021),
# and method for rating the closeness of the
# city to nature by looking at the nature
# reserves around it, their area size and the
# distance from the city.
################################################

import math
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

########### constants ###########

crimes_path = f'./data/raw/Crime-map-2021'
crimes_rate_path = f'./data/rated/Crime-map-2021_rate'
# data from: https://www.gov.il/he/departments/general/nature_reserves_2
nature_path = f'./data/raw/שמורות-וגנים-בתוכניות-מפורטות-11_01_2022/respark_meforat_11-01-22'
city_10_figure_coors_path = f'./data/raw/city_coors_ITM_10_figures'
nature_rate_path = f'./data/rated/nature_rate'


def sum_crimes(dataset):
    """
    a method to sum over all types of crimes in one city,
    and extract a dictionary of {city: number of crimes recorded (TIKIM opened)}
    :param dataset: csv file of shape:

                        crimes
                city1   34
                city1   6
                city2   92
                ...
    :return: dictionary of {city: number of crimes recorded (TIKIM opened)}
    """
    cities_and_crimes = dict()
    num_of_crimes = 0
    city_name = dataset.iloc[0, 0]
    i = 0
    for row, col in dataset.iterrows():
        if len(dataset.iloc[row, 0]) < 2 or dataset.iloc[row, 0] == 'מקום אחר':
            continue
        if city_name != dataset.iloc[row, 0]:
            if city_name not in cities_and_crimes:
                cities_and_crimes[city_name] = 0
            cities_and_crimes[city_name] += num_of_crimes
            city_name = dataset.iloc[row, 0]
            num_of_crimes = 0
        num_of_crimes += int(dataset.iloc[i, 1])
        i += 1

    return cities_and_crimes


def get_crimes():
    """
    a method that create a rate for crimes in a city,
    from data of number of crimes in each city (csv file).
    """
    # get all info from the filtered dataset
    crimes_dataset = pd.read_csv(f'{crimes_path}.csv', encoding="utf8")

    # sum the crimes in each city
    city_crimes = sum_crimes(crimes_dataset)

    # extract dictionary to dataset
    pd.DataFrame.from_dict(city_crimes, orient='index', columns=['crimes']).to_csv(f'{crimes_rate_path}.csv',
                                                                                   encoding="utf-8-sig")


def convert_10_figures_coors_to_ITM(dataset):
    """
    method for convert 10-figures coordinate system into ITM (Israel Transverse Mercator)
    :param dataset: csv file of shape:
                        coordinates
                city1   abcdefghij
                city2   klmnopqrst
                ...
    :return: dictionary of {city: (x,y)} where (x,y) is the coordinate of the city in ITM
    """
    city_coors_ITM_dict = dict()
    for row, col in dataset.iterrows():
        if math.isnan(dataset.iloc[row, 1]): continue
        xy_coors = int(dataset.iloc[row, 1])  # of shape xxxxxyyyyy
        x = (xy_coors // 100000) * 10  # convert to xxxxx0
        y = (xy_coors % 100000) * 10  # convert to yyyyy0
        city_coors_ITM_dict[dataset.iloc[row, 0]] = (x, y)

    return city_coors_ITM_dict


def get_nature_rate():
    """
    a method that create a rate for cities closeness to nature,
    from geographic data of the nature reserves in israel (shape files)
    ands coordinates of cities in Israel (csv file).
    """
    nature_points = gpd.read_file(f'{nature_path}.shp')
    city_10_figure_coors = pd.read_csv(f'{city_10_figure_coors_path}.csv', encoding="utf8")
    city_ITM_dict = convert_10_figures_coors_to_ITM(city_10_figure_coors)

    # for each city coors, calculate its closeness to nature reserves
    city_rate_dict = dict()

    for city in city_ITM_dict:
        city_point = Point(city_ITM_dict[city])
        city_rate = 0
        for row, poi in nature_points.iterrows():
            curr_point = nature_points.loc[row].geometry.centroid   # center of the nature reserve
            curr_dist = city_point.distance(curr_point)     # distance from the nature reserve and the city
            curr_area = nature_points.loc[row].geometry.area      # area of the nature reserve
            city_rate += curr_area/math.pow(curr_dist, 2)
        print(city + ", " + str(city_rate))
        print(city + ", " + str(math.log10(math.pow(city_rate, 2))))
        city_rate_dict[city] = math.log10(math.pow(city_rate, 2))      # normalize values between 0-3

    # extract dictionary into csv
    pd.DataFrame.from_dict(city_rate_dict, orient='index', columns=['nature_rate']).to_csv(f'{nature_rate_path}.csv',
                                                                                   encoding="utf-8-sig")


if __name__ == '__main__':
    ## get the crimes
    get_crimes()
    get_nature_rate()
