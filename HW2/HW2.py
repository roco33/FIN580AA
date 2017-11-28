# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 10:12:19 2017

@author: roco33
"""

import pandas as pd
import numpy as np



def import_data():
    
    # asset names set
    asset = ['Russell 1000', 'Russell 2000', 'BAML US Corporate Master', 
             'BAML US High Yield', '3-Month Treasury Bill', 'CPI', 
             'MSCI EAFE', 'MSCI EM']
    # file name
    file = 'Data for HW 2 Fall 2017.csv'
    # skip rows
    skip = [i for i in range(9)]
    # read csv into dataframe
    raw_data = pd.read_csv(file,skiprows = skip,usecols = [i for i in range(9)])
    raw_data.columns = ['year'] + asset
    raw_data = raw_data.set_index('year')
    # inflation
    inflation = raw_data['CPI']/raw_data['CPI'].shift(1) - 1
    inflation = inflation[1:]
    raw_data = raw_data.drop('CPI', axis = 1)
    #return
    return_data = np.log(raw_data/raw_data.shift(1))
    return_data['3-Month Treasury Bill'] = raw_data['3-Month Treasury Bill'] / 100
    return_data = return_data[1:]
    
    return return_data, inflation



def GK(): # expected return of equity index
    
    GK_data = {'Russell 1000': [0.025, 23, 19, 0.06], 
      'Russell 2000': [0.016, 32, 23, 0.07], 
      'MSCI EAFE': [0.035, 19, 21, 0.07],
      'MSCI EM': [0.025, 16, 15, 0.1]}
    GK_index = ['Dividend Yield', 'PE Current', 'PE Median', 'EPS Growth']
    GK_input = pd.DataFrame(GK_data, index = GK_index)
    exp_inflation = 0.02
    
    exp_ret_e = (GK_input.loc['Dividend Yield',:] + exp_inflation + GK_input.loc['EPS Growth',:]/10) * ((GK_input.loc['PE Current',:] / GK_input.loc['PE Median',:]-1)/10+1)
    
    return exp_ret_e



def RP(): # expected return of fixed income index
    
    RP_data = {'BAML US Corporate Master':[0.02,0.045,0.01,0.01,0.01,0.6],
               'BAML US High Yield': [0.02,0.045,0.035,0.05,0.04,0.6]}
    RP_index = ['Treasury Yield', 'Target Yield', 'Spread', 'Target Spread',
                'Default Rate', 'Recovery Rate']
    RP_input = pd.DataFrame(RP_data, index = RP_index)
    
    exp_ret_f = (RP_input.loc['Target Yield',:] - RP_input.loc['Treasury Yield',:])/10 + RP_input.loc['Treasury Yield',:] + (RP_input.loc['Target Spread',:] - RP_input.loc['Spread',:])/10 + RP_input.loc['Spread',:] + RP_input.loc['Default Rate',:] * RP_input.loc['Recovery Rate',:]
    
    return exp_ret_f
    



exp_ret = GK()
exp_ret = exp_ret.append(RP())
exp_ret = exp_ret.append(pd.Series([0.02], index = ['3-Month Treasury Bill']))



[data, inflation] = import_data()
sd = data.std()
corr = data.corr()




