#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 15:53:29 2022

@author: karthigeyansambandan
"""


import pandas as pd
import os
import numpy as np
os.chdir('/Users/karthigeyansambandan/Desktop/OVO/')

filename_men = 'WPP2019_POP_F07_2_POPULATION_BY_AGE_MALE.xlsx'
filename_women = 'WPP2019_POP_F07_3_POPULATION_BY_AGE_FEMALE.xlsx'


def get_population(filename, name, table_name):
    xls = pd.ExcelFile(filename)
    df = pd.read_excel(xls, 'ESTIMATES')
    header = df.iloc[15]
    df_population = df.iloc[16:,]
    df_population.columns = header
    df_population.set_index('Index')
    data_country = df_population.loc[(df_population['Type']=="Country/Area") & (df_population['Reference date (as of 1 July)']==2020)]
    data_country[name]=data_country.iloc[:,8:].sum(axis=1)
    data_country.columns = [table_name + '.' + str(col) for col in data_country.columns]
    return data_country

data_men = get_population(filename_men, 'Population Men', 'Men')
data_women = get_population(filename_women, 'Population Women', 'Women')
data_all = pd.concat([data_men, data_women], axis=1)
population_data = data_all.filter(['Men.Index', 'Men.Variant', 'Men.Region, subregion, country or area *','Men.Country code', 'Men.Type','Men.Reference date (as of 1 July)', 'Men.Population Men', 'Women.Population Women'], axis=1)
population_data['Total Population'] = population_data['Men.Population Men'] + population_data['Women.Population Women']
population_data['Total Population']=population_data['Total Population'].multiply(1000).round(1)
print(list(population_data.columns))
data = population_data.loc[population_data['Total Population'] >= 5]

replace_values = {"Iran (Islamic Republic of)": "Iran", 
                  "Dem. People's Republic of Korea": "North Korea", 
                  "Republic of Korea":"South Korea",
                  "Bolivia (Plurinational State of)":"Bolivia",
                  "Venezuela (Bolivarian Republic of)":"Venezuela",
                  "United States of America":"United States",
                  "Hong Kong SAR":"Hong Kong",
                  "Russian Federation":"Russia"}

data['Men.Region, subregion, country or area *'].replace(replace_values, inplace=True)
data['Men.Region, subregion, country or area *'].unique()
len(data['Men.Region, subregion, country or area *'].unique())
data.to_csv('filtered_population_data.csv')
