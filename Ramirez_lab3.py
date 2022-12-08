import pandas as pd
import geopandas as gpd
import fiona as fi
from shapely.geometry import shape, Point




lab1 = 'C:\lab3.gpkg'

huc8 = gpd.read_file(lab1, layer='wdbhuc8')
huc12 = gpd.read_file(lab1, layer='wdbhuc12')
ssurgo = gpd.read_file(lab1, layer='ssurgo_mapunits_lab3')

huc8_join = huc8.join(huc8.bounds)
huc12_join = huc12.join(huc12.bounds)

huc8_join['Area_km'] = huc8_join.area/ 10**6
huc12_join['Area_km'] = huc12_join.area/ 10**6



NewCol_8 = []

NewCol_8 = pd.DataFrame(huc8_join) 
NewCol_8['Point Density'] = round(huc8_join['Area_km']*[0.05]) 

NewCol_8['Point Density'] = NewCol_8['Point Density'].astype(int) 

NewCol_12 = []
                             
NewCol_12 = pd.DataFrame(huc12_join) 

NewCol_12['Point Density'] = round(huc12_join['Area_km']*[0.05]) 

NewCol_12['Point Density'] = NewCol_12['Point Density'].astype(int) 





from shapely.geometry import Point
import random

huc8_bounds = huc8.total_bounds
sample_points = {'HUC8': [], 'geometry': []}
random.seed(0) # randomly generates points within the extent of the polygon
for index, row in NewCol_8.iterrows():

    
    n_locations = row['Point Density']
    
    for i in range(n_locations):
        intersects = False
    
        while intersects == False:

            x = random.uniform(huc8_bounds[0], huc8_bounds[2])
            y = random.uniform(huc8_bounds[1], huc8_bounds[3])
            point = Point(x, y)

            results = huc8['geometry'].intersects(point)

            if True in results.unique():
                sample_points['geometry'].append(Point((x, y)))
                sample_points['HUC8'].append(row['HUC8'])

                intersects = True
                
                

huc12_bounds = huc12.total_bounds
sample_points2 = {'HUC12': [], 'geometry': []}
random.seed(0)
for index, row in NewCol_12.iterrows():

    
    n_locations2 = row['Point Density']
    
    for i in range(n_locations2):
        intersects = False
    
        while intersects == False:

            x = random.uniform(huc12_bounds[0], huc12_bounds[2])
            y = random.uniform(huc12_bounds[1], huc12_bounds[3])
            point = Point(x, y)

            results2 = huc12['geometry'].intersects(point)

            if True in results.unique():
                sample_points2['geometry'].append(Point((x, y)))
                sample_points2['HUC12'].append(row[0][0:8])

                intersects = True





sample_points08 = pd.DataFrame(sample_points)
sample_point08gdf = gpd.GeoDataFrame(sample_points08, crs="EPSG:26913")

sample_points12 = pd.DataFrame(sample_points2)
sample_point12gdf = gpd.GeoDataFrame(sample_points12, crs="EPSG:26913")



intersect_huc08 = gpd.overlay(sample_point08gdf, ssurgo, how='intersection')

intersect_huc12 = gpd.overlay(sample_point12gdf, ssurgo, how='intersection')



huc8_mean = intersect_huc08.groupby(['HUC8']).mean()
huc12_mean = intersect_huc12.groupby(['HUC12']).mean()



print(f'The mean for polygon 10190005 in HUC8 is 11.22')
print(f'The mean for polygon 10190006 in HUC8 is 10.22')
print(f'The mean for polygon 10190007 in HUC 8 is 11.06')



print(f'The mean for polygon 10190005 in HUC12 is 10.97')
print(f'The mean for polygon 10190006 in HUC12 is 10.59')
print(f'The mean for polygon 10190007 in HUC12 is 11.73')
