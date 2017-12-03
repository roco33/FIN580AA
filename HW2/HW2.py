# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 10:12:19 2017

@author: roco33
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from optPort import efficient_frontier,stats



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



#def GK_e(): # expected return of equity index
#    
#    GK_data = np.array([[0.025, 23, 19, 0.06], 
#               [0.016, 32, 23, 0.07], 
#               [0.035, 19, 21, 0.07],
#               [0.025, 16, 15, 0.1]]).T
#    GK_index = ['Dividend Yield', 'PE Current', 'PE Median', 'EPS Growth']
#    GK_col = ['Russell 1000', 'Russell 2000', 'MSCI EAFE', 'MSCI EM']
#    GK_input = pd.DataFrame(GK_data, index = GK_index, columns = GK_col)
#    exp_inflation = 0.02
#    
#    exp_ret_e = ((GK_input.loc['Dividend Yield',:] 
#                 + exp_inflation
#                 + GK_input.loc['EPS Growth',:]/10) 
#                 * ((GK_input.loc['PE Current',:] 
#                 / GK_input.loc['PE Median',:]-1)/10+1))
#    
#    return exp_ret_e
#
#
#
#def GK_f(): # expected return of fixed income index
#    
#    RP_data = np.array([[0.02,0.045,0.01,0.01,0.01,0.6],
#               [0.02,0.045,0.035,0.05,0.04,0.6]]).T
#    RP_index = ['Treasury Yield', 'Target Yield', 'Spread', 'Target Spread',
#                'Default Rate', 'Recovery Rate']
#    RP_col = ['BAML US Corporate Master', 'BAML US High Yield']
#    RP_input = pd.DataFrame(RP_data, index = RP_index, columns = RP_col)
#    # duration of 3
#    exp_ret_fi = ((RP_input.loc['Target Yield',:] 
#                 - RP_input.loc['Treasury Yield',:])/10 # use compounded return
#                 + RP_input.loc['Treasury Yield',:] 
#                 + (RP_input.loc['Target Spread',:] 
#                 - RP_input.loc['Spread',:])/10 # use compunded return
#                 + RP_input.loc['Spread',:] 
#                 + RP_input.loc['Default Rate',:] 
#                 * RP_input.loc['Recovery Rate',:])
#    
#    return exp_ret_fi
    


def main():
    # expected return
#    exp_ret_e = GK_e()
#    exp_ret = exp_ret_e[['Russell 1000','Russell 2000']].append(GK_f())
#    exp_ret = exp_ret.append(pd.Series([0.02], index = ['3-Month Treasury Bill']))
#    exp_ret = exp_ret.append(exp_ret_e[['MSCI EAFE', 'MSCI EM']])
    
    # input expected return
    exp_ret_data = np.array([0.1051,0.0732,0.0297,0.0769,0.0185,0.1351,0.1386])
    exp_ret_index = ['Russell 1000', 'Russell 2000', 'BAML US Corporate Master', 
             'BAML US High Yield', '3-Month Treasury Bill', 'MSCI EAFE', 
             'MSCI EM']
    exp_ret = pd.Series(exp_ret_data,index = exp_ret_index)
    
    
    # covariance
    [data, inflation] = import_data()
    sd = data.std()
    cov = data.cov()
    
    # optimization
    r_min = np.linspace(0,0.2,100)
    
    [mu,std,w_cum] = efficient_frontier(exp_ret, cov, r_min)
    std_lower = np.amin(std)
    std_upper = np.amax(std)
    
    
    plt.plot(std,mu)
    plt.show()
#    plt.figure()
#    plt.plot(std_list,w_list)
    
    stat = np.zeros([1,9]) # 1 + 1 + n
    
    for i in range(50):
        # add randomness
        exp_ret1 = exp_ret + np.random.standard_normal(size = sd.shape) * sd /10
        # optimization
        [mu, std, w] = efficient_frontier(exp_ret1, cov, r_min)
        stat_1 = np.concatenate((np.array([mu]).T,np.array([std]).T,w),axis = 1)
        stat = np.concatenate((stat, stat_1), axis = 0)
#        plt.plot(std,mu)

    stat = stat[1:,:]
    stat = stat[np.argsort(stat[:,1])]
    stat = stat[(stat[:,1]<=std_upper) & (stat[:,1]>=std_lower)]
    
    std_space = np.geomspace(std_lower, std_upper,30)

    
    w = np.array([]) # n
    for i in range(len(std_space)-1):
        w_1 = np.mean(stat[(stat[:,1]>= std_space[i]) & (stat[:,1] < std_space[i+1]),2:],axis=0)
#        print(w_1)
        w = np.append(w,w_1)
        
    w = np.reshape(w, (-1,7))
    mu = np.array([])
    std = np.array([])
    
    for j in range(w.shape[0]):
        [mu_1,std_1,w_1] = stats(w[j,:],exp_ret,cov)
        mu = np.append(mu,mu_1)
        std = np.append(std,std_1)
    
    plt.plot(std, mu, 'r--')
    
    plt.figure()
    plt.stackplot(std,w.T)
    plt.legend(['Russell 1000', 'Russell 2000', 'BAML US Corporate Master', 
             'BAML US High Yield', '3-Month Treasury Bill', 'MSCI EAFE', 
             'MSCI EM'])
    plt.show()
    

    





if __name__ == '__main__':
    main()

