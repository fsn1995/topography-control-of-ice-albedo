#%%
# import vaex as vx
import pandas as pd
import numpy as np
import geopandas as gpd
import os
import glob
import tarfile
#%%

'''
DEM
'''
#%% dem
dfhp = pd.read_csv("/data/shunan/data/topography/hp/dem.csv", skiprows=np.arange(1,28067))
dffield = pd.read_csv("/data/shunan/data/topography/field/dem.csv")
dfserver = pd.read_csv("/data/shunan/data/topography/server/dem.csv", skiprows=np.arange(1,28067))

#%%
basinpoly = gpd.read_file("basin/GrISBasinDissolved.shp").to_crs("EPSG:4326")
basinpoly.plot()

#%%
df = pd.concat([dffield, dfserver, dfhp]).drop(columns=['datetime'])
df["basin"] = "basin"
df.head()


gdfpoint = gpd.GeoDataFrame(
    df, geometry=gpd.points_from_xy(df.longitude, df.latitude), crs="EPSG:4326"
)

for i in range(len(basinpoly.SUBREGION1)):
    index = gpd.sjoin(
        gdfpoint, basinpoly.iloc[[i]].to_crs("EPSG:4326"), 
        how="inner", 
        op="within"
    )
    df["basin"].loc[index.index] = basinpoly.SUBREGION1[i]

df.to_csv("/data/shunan/data/topography/dem.csv", index=False, mode="w")

# dfvx = vx.from_pandas(df)
# dfvx.export_hdf5("/data/shunan/data/topography/dem.hdf5", progress=True)

'''
Albedo
'''
# %% albedo
dfhp = pd.read_csv("/data/shunan/data/topography/hp/albedo.csv", skiprows=np.arange(1,19976))
dffield = pd.read_csv("/data/shunan/data/topography/field/albedo.csv")
dfserver = pd.read_csv("/data/shunan/data/topography/server/albedo.csv", skiprows=np.arange(1,19976))


#%%
df = pd.concat([dffield, dfserver, dfhp]).drop(columns=['datetime'])
df["basin"] = "basin"
df = df.rename(columns={"visnirAlbedo": "albedo"})
df.head()


gdfpoint = gpd.GeoDataFrame(
    df, geometry=gpd.points_from_xy(df.longitude, df.latitude), crs="EPSG:4326"
)


for i in range(len(basinpoly.SUBREGION1)):
    index = gpd.sjoin(
        gdfpoint, basinpoly.iloc[[i]].to_crs("EPSG:4326"), 
        how="inner", 
        op="within"
    )
    df["basin"].loc[index.index] = basinpoly.SUBREGION1[i]

df.to_csv("/data/shunan/data/topography/albedo.csv", index=False, mode="w")

# dfvx = vx.from_pandas(df)
# dfvx.export_hdf5("/data/shunan/data/topography/albedo.hdf5", progress=True)

'''
join dem and albedo
'''
#%%
dfdem = pd.read_csv("/data/shunan/data/topography/dem.csv")
dfalbedo = pd.read_csv("/data/shunan/data/topography/albedo.csv")
dfdem["datetime"] = pd.to_datetime(dfdem.time_end, unit="ms")
dfalbedo["datetime"] = pd.to_datetime(dfalbedo.time, unit="ms")

uniquei = dfdem.id.unique()
# %% join by datetime

randomPoints = gpd.read_file("shp/randamSample.shp")

for i in uniquei:
    print("Processing No. %d" % i)
    index = dfdem.id == i
    dfdemsub = dfdem[index]
    index = dfalbedo.id == i
    dfalbedosub = dfalbedo[index]
    dfalbedosub["dist"] = randomPoints.iloc[i].NEAR_DIST

    dfmerge = pd.merge_asof(
        dfalbedosub.sort_values('datetime'), 
        dfdemsub.sort_values('datetime'), 
        on='datetime',
        allow_exact_matches=False, 
        tolerance=pd.Timedelta(days=3),
        direction='nearest'
    )#.dropna()
    dfmerge = dfmerge.drop(columns=['datetime', 'geometry_x', 'longitude_y',
                                    'latitude_y','id_y', 'basin_y', 'geometry_y'])
    dfmerge = dfmerge.rename(columns={
        "longitude_x": "longitude",
        "latitude_x": "latitude",
        "id_x": "id",
        "basin_x": "basin"
    })                    
                
    if i == 0:
        dfmerge.to_csv("/data/shunan/data/topography/topomerge.csv", 
                        mode="w", index=False, header=True)
    else:
        dfmerge.to_csv("/data/shunan/data/topography/topomerge.csv", 
                        mode="a", index=False, header=False)

#%% estimate duration of bare ice
df = pd.read_csv("/data/shunan/data/topography/topomerge.csv")
df["datetime"] = pd.to_datetime(df.time_x, unit="ms")
df["year"] = df.datetime.dt.year
df["month"] = df.datetime.dt.month
df["duration"] = np.nan

uniquei = df.id.unique()

for i in uniquei:
    print("Processing No. %d" % i)
    dfsub = df[df.id == i]
    for y in dfsub.year.unique():
        index = (dfsub.month>6) & (dfsub.month<9) & (dfsub.albedo<0.65)  & (dfsub.year == y)
        if sum(index) == 0:
            continue
        dfsub.duration[index] = (dfsub[index].datetime.iloc[-1] - dfsub[index].datetime.iloc[0]).days

    dfsub = dfsub.drop(columns = ['datetime', 'year', 'month'])
    if i == 0:
        dfsub.to_csv("/data/shunan/data/topography/topodata.csv", 
                        mode="w", index=False, header=True)   
    else:
        dfsub.to_csv("/data/shunan/data/topography/topodata.csv", 
                        mode="a", index=False, header=False)  

#%% keep bare ice surface only
df = pd.read_csv("/data/shunan/data/topography/topodata.csv")
df["datetime"] = pd.to_datetime(df.time_x, unit="ms")
df["year"] = df.datetime.dt.year
df["month"] = df.datetime.dt.month


index = (df.albedo < 0.65) & (df.elevation > 0) # keep only ice surface
df = df[index]

#%%
index = df.basin.unique()
for i in index:
    print(i)
    dfbasin = df[df.basin == i].groupby(["id", "year", "month"]).mean()
    dfbasin["basin"] = i
    dfbasin.to_csv("/data/shunan/data/topography/basin/" + i + ".csv", mode="w")
    
    dfbasin = df[df.basin == i]
    monthindex = (dfbasin.month>6) & (dfbasin.month<9)
    dfbasin = dfbasin[monthindex].groupby(["id", "year"]).mean()
    dfbasin["basin"] = i
    dfbasin.to_csv("/data/shunan/data/topography/basin/" + i + "_annual.csv", mode="w")


# %%
'''
extract arctic dem from .tar.gz
'''
# inputpath = r"H:\AU\topography\dem\zip\SW"
# outputpath = r"H:\AU\topography\dem\unzip\SW"
# os.chdir(inputpath)

# filepath = glob.glob('*.{}'.format('gz'))
# # %%
# for f in filepath:
#     # open file
#     file = tarfile.open(f)
#     # extracting file
#     file.extractall(outputpath)
#     file.close()
# %%
