import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from random import gauss, randint, random
from functools import reduce
from sklearn.cluster import DBSCAN
import csv

class SyntheticData:
    def __init__(self, 
                 start, 
                 main_size, 
                 main_spread, 
                 cl_size, 
                 cl_spread, 
                 noise_to_start_ratio=0.001,
                 line_frequency=0.01):
                 
        self.start = start
        self.current_loc = start
        self.main_size = main_size
        self.main_spread = main_spread
        self.cl_size = cl_size
        self.cl_spread = cl_spread
        self.noise_to_start_ratio = noise_to_start_ratio
        self.line_frequency = line_frequency
        self.noise_spread = start * noise_to_start_ratio
        self.horizontal_steps = 0
        self.previous_main_max = 0
        self.previous_horizontal_max = 0

    def main_trend(self, day):
        # number of noise points
        nn = randint(int(0.15*self.main_size), int(0.30*self.main_size))
        # return just noise on a weekend
        weekend = day % 7
        if weekend == 0 or weekend+1 == 0:
            return self.noise(nn)
        # create main trend cluster
        size = int(abs(gauss(self.main_size, self.main_spread)))
        x = self.create_cluster(self.current_loc, size, self.main_spread)
        # update main trend locations
        self.current_loc = 2*self.main_spread + max(x)
        self.previous_main_max = max(x)
        # horizontal line stuff
        if self.horizontal_steps:
            h = self.create_cluster(self.previous_horizontal_max, 
                                    self.cl_size, self.cl_spread)
            # set the h-line location to the max or previous h-line
            self.previous_horizontal_max = max(h)
            x.extend(h)
            self.horizontal_steps -= 1
        else:
            self.trigger_horizontal()
            # if we are not in an h-line, update to the main trend max
            self.previous_horizontal_max = self.previous_main_max
        # add noise
        x.extend(self.noise(nn))
        # add random clusters
        nc = randint(0,10)
        for cl in range(nc):
            loc = int(gauss(self.current_loc, self.noise_spread)) 
            cluster = self.create_cluster(loc, self.cl_size, self.cl_spread)
            x.extend(cluster)
        return sorted(x)
            
    def create_cluster(self, loc, size, spread):
        x = np.random.gamma(2.5, spread, size=size).astype(int)
        return sorted(set(x + loc))
        
    def trigger_horizontal(self):
        # 1% chance or horizontal group
        if random() < self.line_frequency:
            self.horizontal_steps = randint(10,20)
    
    def noise(self, n):
        return [int(gauss(self.current_loc, self.noise_spread)) for _ in range(n)]


        
sd = SyntheticData(123456789, 100, 30, 30, 10, 0.002, 0.02)
data = np.array([(d,z) for d in range(2000) for z in sd.main_trend(d)])

plt.scatter(data[:,0], data[:,1], s=2, alpha=0.02)
plt.show()
        
df = pd.DataFrame(data, columns=['day','ID'])
n_days = df.day.max() - df.day.min()
v_bins = 10 * n_days
c, bx, by = np.histogram2d(df.day, df.ID, bins=(n_days, v_bins))
cc, edges, p = plt.hist(c.ravel(), bins=int(c.max()), log=True)
plt.show()
xx, yy = np.meshgrid(bx, by)
hist_cut = 6

delta_y = np.ceil(np.diff(by))[0]
ixi, ixj = np.where(c>=hist_cut, xx[:-1,:-1].T, 0).nonzero()

z = zip(bx[ixi], by[ixj], by[ixj]+delta_y)
# takes a few minutes:
b = reduce(np.logical_or, (df.day.eq(d) & df.ID.ge(id1) & df.ID.le(id2) for d,id1,id2 in z))

plt.scatter(data[:,0], data[:,1], s=2, alpha=0.15)
plt.scatter(data[b,0], data[b,1], s=2, alpha=0.02)
plt.show()
