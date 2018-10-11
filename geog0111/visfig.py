import numpy as np
from nsat import nsat
import pylab as plt

'''
Code to produce figure for section 2.2.4
'''

# sum the data over all months (axis 0)
sum_per_year = (nsat().data.sum(axis=0))

high = sum_per_year>=1000
low  = sum_per_year<=300
sum_per_year = np.log(sum_per_year)

a = np.array([sum_per_year,high.astype(float)*8,low.astype(float)*8])
plt.figure(figsize=(10,2))
plt.imshow(a)
plt.colorbar(orientation='horizontal')
plt.xlabel('sample number')
plt.savefig('arrayviz.jpg')
