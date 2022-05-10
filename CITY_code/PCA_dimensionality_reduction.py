################################################
# This file is a program for creating a
# clustering representation of cities, using
# their properties.
# Clustering is done using the PCA method
# (Principal Component Analysis).
################################################
import pandas as pd
from sklearn.decomposition import PCA
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource
import numpy as np

################ constans ######################
CITY_MERGED_DF_PATH = f'./data/CITY_merged_dataset_06'
CITIES_PCA_PATH = f'./cities_pca/'
SETTLEMENT_NUM_X = 1

def df_to_pca(df):
    """
    a method creating a PCA transform from dataframe,
    while choosing the most relevant properties columns of all
    the cities in the dataframe.
    :param df: DataFrame of the cities characteristics.
    :return: PCA transform of the most significant 2 components
    """
    # select the columns that are relevant for applying pca to
    columns_to_pca = ['edu_years_avg_norm', 'Salary_norm', 'Internet_norm', 'religion_num',
                      'log_population', 'dist_num', 'nature_rate', 'job_demands']
    df_col_reduce = df[columns_to_pca]
    X = df_col_reduce.iloc[:, 1:]  # all rows, without the cities names

    # Normalize the data before applying the fit method
    df_normalized = (X - X.mean()) / X.std()
    pca = PCA(n_components=2)
    transform = pca.fit_transform(df_normalized)
    return transform



def create_plot(df, transform, curr_city):
    """
    a method for creating the plot that representing the cities cluster,
    by a PCA transform. In the plot one can find related cities to the current city
    (highlighted by color) from the closest cities in the plot.
    :param df: DataFrame of the cities characteristics.
    :param transform: the PCA transform of the relevant dada
    :param curr_city: the current chosen city to highlight in the plot
    """
    # Reformat and view results
    p = figure(plot_width=1400, plot_height=700, title='באפשרותך לבחון ערים בעלות מאפיינים דומים ל' + curr_city)
    p.title.text_color = '#FF00FF60'
    p.title.text_font_size = '20pt'
    p.title.align = 'right'
    # Highlight the current city
    index = df.index
    condition = df['settlement'] == curr_city
    city_idx = index[condition].tolist()[0]
    numpy_array_of_colors = np.full(len(df.loc[:, 'settlement']), 0xFFFF0040, dtype=np.uint32)
    numpy_array_of_colors[city_idx] = 0xFF00FF60    # color the current city in different color

    source = ColumnDataSource(data = {'pca1': transform[:, 0],
                                      'pca2': transform[:, 1],
                                      'radius': df.loc[:, 'log_population'].pow(2) / 1500,  # reduce the circles size
                                      # so it associative reflect the population size
                                      'city': df.loc[:, 'settlement'],
                                      'colors': numpy_array_of_colors})

    p.circle(x='pca1', y='pca2', source=source, radius='radius', fill_color='colors', alpha=0.7)

    # Add hover tool with the names of the cities in the plot
    hover = HoverTool(
        tooltips=[
            ("city", "@city")
        ])
    p.add_tools(hover)
    #
    output_file(filename=CITIES_PCA_PATH + df.iloc[city_idx, 1] + '.html')
    # show(p)

if __name__ == '__main__':
    df = pd.read_csv(f'{CITY_MERGED_DF_PATH}.csv', encoding="utf8")
    transform = df_to_pca(df)
    # for city in df.loc[:, 'settlement']:
    #     create_plot(df, transform, city)
