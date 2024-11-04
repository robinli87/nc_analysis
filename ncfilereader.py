from netCDF4 import Dataset
import numpy as np
import os
import xarray as xr

import matplotlib.pyplot as plt

def extract(io):
    nc_file = Dataset(io, mode='r',format='NETCDF4_CLASSIC') 
    
    print(nc_file.variables.keys())
    data = dict(nc_file.variables)
    # latitudes = np.array(nc_file.variables["latitude"])
    # latitudes = np.array(nc_file.variables["latitude"])
    # time = np.array(nc_file.variables["time"])
    # u10 = np.array(nc_file.variables["u10"])
    
    # print(latitudes)
    # print(longitudes)
    # print(time)
    # print(u10)
    
    return(data)

folderpath = "/network/group/aopp/met_data/MET001_ERA5/data/ps/1hr/"
folderpath = "."
files = []


for result in os.scandir(folderpath):
    if result.is_file() and str(result.name).endswith(".nc"):
        #this is a datafile
        #print(result.name)
        files.append(os.path.join(folderpath, result.name))
        
# test case: select the last one of the list, which is data from 2019
data = extract(files[-1])
print(files[-1])

for i in list(data.keys()):
    this = np.array(data[i])
    print(i, " shape: ", this.shape)

ps = np.array(data['ps'])
latitudes = list(data["latitude"])
longitudes = list(data["longitude"])
times = list(data['time'])

for t in range(0, len(times)):
    times[t] = int(times[t])

# look at the arctic pole:
lat = 89
lon = 0

#get corresponding indices
i = latitudes.index(lat)
j = longitudes.index(lon)

print(len(ps))

localpressure = []

for t in range(0, len(ps)):
    localpressure.append(ps[t][i][j])

localpressure2 = []
for t in range(0, len(ps)):
    localpressure2.append(ps[t][i+2][j])

def pearson(x, y):
    mean_x = sum(x)/len(x)
    mean_y = sum(y)/len(y)
    
    numerator = 0
    for i in range(0, len(x)):
        numerator += (x[i]-mean_x)*(y[i]-mean_y)
    
    denominator1 = 0
    for i in range(0, len(x)):
        denominator1 += (x[i] - mean_x) ** 2
        
    denominator2 = 0
    for i in range(0, len(x)):
        denominator2 += (y[i] - mean_y) ** 2
        
    r = numerator * (denominator1 * denominator2) ** -0.5
    return(r)
        
    
    
# ~ print(len(localpressure))
# ~ print(localpressure)
# ~ print(times)

print(pearson(localpressure, localpressure2))
plt.scatter(localpressure2, localpressure)
plt.show()
