# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 21:58:25 2017

@author: roco3
"""


from cvxopt import matrix, solvers
import numpy as np


def optimize_portfolio(exp_ret, cov, r_min):
    
    n = len(exp_ret)
    P = matrix(np.array(cov))
    q = matrix(np.zeros((n, 1)), tc = 'd')
    
    G = matrix(np.concatenate(
            (-np.array([exp_ret]), -np.identity(n)), 0))
    h = matrix(np.concatenate(
            (-np.ones((1,1))*r_min, np.zeros((n,1))), 0))
    
    A = matrix(1.0, (1,n))
    b = matrix(1.0)
    sol = solvers.qp(P, q, G, h, A, b)
    
    return sol


#exp_ret = 
#cov = 
r_min = 0.04

weight = np.array(optimize_portfolio(exp_ret,cov,r_min)['x'])
mu = np.dot(np.transpose(weight),np.array(exp_ret))
std = np.sqrt(np.dot(np.dot(np.transpose(weight),np.array(cov)),weight))
