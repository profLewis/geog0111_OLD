import requests
import numpy as np
from io import StringIO
from dateutil import parser
import matplotlib.pylab as plt

url = 'https://waterservices.usgs.gov/nwis/dv/?sites=08220000&format=rdb&startDT=2001-01-01&parameterCd=00060'
data = np.loadtxt(StringIO(requests.get(url).text),skiprows=30,\
           usecols=(2,3),unpack=True,dtype=str)
# parser.parse() is useful for string to date conversion
date = [parser.parse(d) for d in data[0]]
flow = data[1].astype(float)
plt.figure(figsize=(10,3))
plt.plot(date,flow)
plt.xlim(date[0],date[-1])
plt.title('Discharge, cubic feet per second (Mean) at Del Norte')
plt.savefig('images/discharge.jpg')
