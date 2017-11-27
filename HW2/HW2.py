# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 10:12:19 2017

@author: roco33
"""

import pandas as pd
import numpy as np



def importData():
    # asset names set
    asset = ['Russell 1000', 'Russell 2000', 'BofA Merrill Lynch US Corp Master', 'BofA Merrill Lynch US High Yield', '3-Month Treasury Bill', 'Consumer Price Index for All Urban Consumers', 'EAFE Standard (Large+Mid Cap)', 'EM (EMERGING MARKETS) Standard (Large+Mid Cap)']
    # file name
    file = 'Data for HW 2 Fall 2017.csv'
    # skip rows
    skip = [i for i in range(9)]
#    skip.append(10)
    # read csv into dataframe
    rawData = pd.read_csv(file,skiprows = skip,usecols = [i for i in range(1,9,1)])
    rawData.columns = asset
    return rawData


data = importData()
