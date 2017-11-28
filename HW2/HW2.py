# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 10:12:19 2017

@author: roco33
"""

import pandas as pd
import numpy as np



def importData():
    
    # asset names set
    asset = ['Russell 1000', 'Russell 2000', 'BAML US Corporate Master', 
             'BAML US High Yield', '3-Month Treasury Bill', 'CPI', 
             'MSCI EAFE', 'MSCI EM']
    # file name
    file = 'Data for HW 2 Fall 2017.csv'
    # skip rows
    skip = [i for i in range(9)]
    # read csv into dataframe
    rawData = pd.read_csv(file,skiprows = skip,usecols = [i for i in range(9)])
    rawData.columns = ['year'] + asset
    rawData = rawData.set_index('year')
    # inflation
    inflation = rawData['CPI']/rawData['CPI'].shift(1) - 1
    inflation = inflation[1:]
    rawData = rawData.drop('CPI', axis = 1)
    #return
    returnData = np.log(rawData/rawData.shift(1))
    returnData['3-Month Treasury Bill'] = rawData['3-Month Treasury Bill'] / 100
    returnData = returnData[1:]
    
    return returnData, inflation



def GK(inflation):
    GK_data = {'Russell 1000': [0.025, 23, 19, 0.06], 
      'Russell 2000': [0.016, 32, 23, 0.07], 
      'MSCI EAFE': [0.035, 19, 21, 0.07],
      'MSCI EM': [0.025, 16, 15, 0.1]}
    GK_index = ['Dividend Yield', 'PE Current', 'PE Median', 'EPS Growth']
    GK_input = pd.DataFrame(GK_data, index = GK_index)
    Exp_inflation = inflation.mean()
    
    Exp_Ret_E = (GK_input.loc['Dividend Yield',:] + Exp_inflation + GK_input.loc['EPS Growth',:]/10) * (GK_input.loc['PE Current',:] / GK_input.loc['PE Median',:]).pow(1/10)
    
    return Exp_Ret_E



[data, inflation] = importData()

Exp_Ret_E = GK(inflation)

sd = data.std()
corr = data.corr()




