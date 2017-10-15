# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 15:04:53 2017

@author: roco33
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


# Stocks, bonds, cash
# model fix
# Expected Return
r = np.array([0.07,0.03,0.02]).reshape((3,1))
# Correlation matrx
corr = np.array([1,0.4,0.1,0.4,1,0.3,0.1,0.3,1]).reshape((3,3))
# Standard deviations
sd = np.array([0.2,0.07,0.02]).reshape((3,1))
# Number of simulations
n_sim = 10000

# search range
xmin = 0
xmax = 1
ymin = 0
ymax = 1
# search step
xstep = 0.1
ystep = 0.1


# variable
# Remaining life 95-30
T = 65
t = 30
# Initial balance
intBlnc = 100000
# Cash infloe
cashIn = 20000
# Withdraw after retirement
withdraw = 30000
# Asset allocation
Alloc = np.array([0.4,0.5,0.1]).reshape((3,1))
    

# calculations
# covariance matrix
cov = np.dot(sd, np.transpose(sd)) * corr
nCol=cov.shape[1]
# Generate a matrix of simulated normal standard returns
SimRet = np.random.normal(loc=0,scale=1,size=(int(n_sim/2*T),nCol))
# variance reduction technique
TempRet = -SimRet
SimRet = np.concatenate((SimRet,TempRet),axis=0)
# Make data lognormal
SimRet = np.exp(SimRet)
# Change variance and covariance of random numbers
SDMat = np.linalg.cholesky(cov)
SimRet = SimRet@SDMat
# Change mean of random numbers
ColAvg = np.mean(SimRet,axis=0)
SimRet = SimRet - ColAvg
SimRet = SimRet + r.T


def Sim1(SimRet,n_sim,T,t,intBlnc,cashIn,withdraw,Alloc):
    # Assuming annual rebalancing, multiply random returns by allocation and obtain a vector of portfolio returns
    SimRet = SimRet@Alloc
    # Reshape the vector into a matrix of T rows
    SimRet = SimRet.reshape(T,n_sim)
    # Allocate a matrix with results
    SimLives = np.zeros([T+1,n_sim])
    SimLives[0,] = intBlnc
    for i in range(1,T+1):
        if i <= t:
            SimLives[i,] = SimLives[i-1,]*(1+SimRet[i-1,])+cashIn*np.ones(n_sim)
        else:
            SimLives[i,] = SimLives[i-1,]*(1+SimRet[i-1,])-withdraw*np.ones(n_sim)
#            SimLives[i,] = SimLives[i-1,]*(1+SimRet[i-1,])
    return(sum(SimLives[T,:]>0)/n_sim)
#    return(np.percentile(SimLives[T,:],10))

#plt.plot(np.arange(30,96),SimLives)
#plt.title('Simulation of future wealth')
#plt.xlabel('Age')
#plt.ylabel('Portfolio value')
#plt.show()


xn = int((xmax-xmin)/xstep+1)
yn = int((ymax-ymin)/ystep+1)
x = np.linspace(xmin, xmax, xn)
y = np.linspace(ymin, ymax, yn)
xv, yv = np.meshgrid(x, y)
z = np.zeros((xn,yn))
for k in range(xn):
    for l in range(yn):
        Alloc = np.array([xv[k,l],yv[k,l],1-xv[k,l]-yv[k,l]])
        z[k,l] = Sim1(SimRet,n_sim,T,t,intBlnc,cashIn,withdraw,Alloc)
z[xv+yv>1] = np.nan

fig = plt.figure()
ax = fig.gca(projection='3d')
surf = ax.plot_surface(xv, yv, z ,cmap=cm.OrRd,vmin=np.nanmin(z), vmax=np.nanmax(z))
ax.set_xlabel('Stock')
ax.set_ylabel('Bond')
ax.set_zlabel('Probability of non-negative wealth')
plt.show()