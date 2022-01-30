import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point

# Open the shapefile
counties = gpd.GeoDataFrame.from_file('/home/martin/Dropbox/codigo/MatecDev/geopandas/benchmarks/us-counties/cb_2018_us_county_20m.shp')

# Generate random points
N = 100000
lat = np.random.uniform(23,51,N)
lon = np.random.uniform(-126,-64,N)

# Create geodataframe from numpy arrays
df = pd.DataFrame({'lon':lon, 'lat':lat})
df['coords'] = list(zip(df['lon'],df['lat']))
df['coords'] = df['coords'].apply(Point)
points = gpd.GeoDataFrame(df, geometry='coords', crs=counties.crs)

# Perform spatial join to match points and polygons
pointInPolys = gpd.tools.sjoin(points, counties, op="within", how='left')

# Example use: get points in Los Angeles, CA.
pnt_LA = points[pointInPolys.NAME=='Los Angeles']

# Plot map with points in LA in red
base = counties.boundary.plot(linewidth=1, edgecolor="black")
points.plot(ax=base, linewidth=1, color="blue", markersize=1)
pnt_LA.plot(ax=base, linewidth=1, color="red", markersize=8)
plt.show()


points_sindex = points
counties_sindex = counties
