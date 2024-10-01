
import pandas as pd
import numpy as np


class Converter:
    def category_converter(dataframe, column,medium,low):
        for i, row in dataframe.iterrows():
            if row[column] <= low:
                dataframe.at[i,column] = 'low'
            elif row[column] > low and row[column] <= medium:
                dataframe.at[i,column] = 'medium'
            elif row[column] > medium:
                dataframe.at[i,column] = 'high'
    
    def binary_converter(dataframe, column, threshold):
        dataframe[column] = dataframe[column].apply(lambda x: 1 if x >= threshold else 0)
        return dataframe[column]
    
    def convert_to_decimal(number):
        if pd.isna(number):
            return 0.0

        int_number = int(number)
        if number == 0:
            return 0.0
        elif int_number == 0:
            return number
        else:
            return number / 100