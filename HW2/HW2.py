# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 10:12:19 2017

@author: roco33
"""

import pandas as pd


file = 'Data for HW 2 Fall 2017.csv'
skip = [i for i in range(9)]
skip.append(10)
data = pd.read_csv(file,skiprows = skip,usecols = [i for i in range(9,17,1)] )