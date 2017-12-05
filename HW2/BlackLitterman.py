# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 12:21:22 2017

@author: roco33
"""



import pandas as pd
import numpy as np
from numpy.linalg import inv


def BL_exp_ret(exp_ret,cov):
    asset = ['Russell 1000', 'Russell 2000', 'BAML US Corporate Master', 
             'BAML US High Yield', 'MSCI EAFE', 'MSCI EM']
    sharp = 0.3
    tau = 0.05
    
    # 1-D Series B-L expected return
    exp_ret_BL = exp_ret[asset]
    
    # 6*6 DataFrame coriance
    cov_BL = cov.loc[asset,asset]
    
    # 1-D Series
    weight = pd.Series([24,2.5,5.1,1.3,22,5.5],index=asset)
    weight = weight/weight.sum()
    
    # Lambda = sharp / sqrt(w' sigma w)
    Lambda = sharp / np.sqrt(np.dot(np.dot(weight,cov_BL),np.transpose([weight])))
    
    # implied excess equilibrium return (1-D array)
    Pi = Lambda * np.dot(cov_BL, weight)
    
    # view vector (1-D array k*1)
    Q = np.array(exp_ret_BL)

    # indentify assets involves in the view (k*n)
    P = np.identity(6)
    
        
    # uncertainty in each view (k*k)
#    t_cov = tau * cov_BL
    Omega = np.diag(np.diag(np.dot(np.dot(P,tau * cov_BL),np.transpose(P))))
    
    return inv(inv(tau*cov_BL) + P.T @ inv(Omega) @ P) @ (inv(tau*cov_BL)@Pi+P.T@inv(Omega)@Q)
