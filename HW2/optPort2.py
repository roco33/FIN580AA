# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 11:54:47 2017

@author: roco33
"""

import numpy as np


def stats(x,exp_ret,cov): 
    exp_ret = np.array(exp_ret)
    cov = np.array([cov])
    x = np.array([x]).T
    mu = x.T @ exp_ret
    std = np.sqrt(
            x.T @ cov @ x
            )
    return np.array([mu, std , mu/std])



# constraints, weights sum up to 1
cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})



n = len(exp_ret)
bnds = tuple((0,1) for x in range(n))


