# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 21:58:25 2017

@author: roco3
"""


from cvxopt import matrix, solvers
import numpy as np


"""
with cvxopt, solve quandratic programing

min   x'Px + q'x
s.t   Gx <= h
      ax  = b
      
where x = [[x1],
           [x2],
           ...,
           [xn]], 
      P = sigma, covariance matrix n*n
      q = 0, zeros matrix n*1
      G = [[-r1, -r2, ..., -rn],
           [-1,  0, ...   ,  0],
           [ 0, -1, ...   ,  0],
           [...           , -1]]
      h = [[-r_min],
           [0],
           ...,
           [0]]
      a = [1, 1, ..., 1]
      b = 1

input: expected return, covariance, minimum return
output: cvxopt solution      

"""

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
#r_min = 0


def stats(x,exp_ret,cov,r_min):
    x_cum = x
    mu = np.dot(np.transpose(x),np.array(exp_ret))
    std = np.sqrt(np.dot(np.dot(np.transpose(x),np.array(cov)),x))
    for n in range(1,len(exp_ret),1):
        x_cum[n] = x_cum[n-1]+x[n]
    
    return mu,std,x_cum



def efficient_frontier(exp_ret, cov, r_min):
    
    mu_list = np.array([])
    std_list = np.array([])
    w_list = np.array([])
    
    for r in r_min:
        try:
            x = np.array(optimize_portfolio(exp_ret,cov,r)['x'])
            [mu,std,w] = stats(x,exp_ret,cov,r)
            mu_list = np.append(mu_list, mu)
            std_list = np.append(std_list, std)
            w_list = np.append(w_list, w)
        except:
            break        
    
    w_list = np.reshape(w_list,(-1,len(exp_ret)))    
    
    return mu_list, std_list, w_list




