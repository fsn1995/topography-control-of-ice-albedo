#%%
import vaex as vx
import pandas as pd
import numpy as np
import geopandas as gpd

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

dfvx = vx.from_pandas(df)
dfvx.export_hdf5("/data/shunan/data/topography/dem.hdf5", progress=True)

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

dfvx = vx.from_pandas(df)
dfvx.export_hdf5("/data/shunan/data/topography/albedo.hdf5", progress=True)

'''
join dem and albedo
'''
#%%
dfdem = pd.read_csv("/data/shunan/data/topography/dem.csv")
dfalbedo = pd.read_csv("/data/shunan/data/topography/albedo.csv")
dfdem["datetime"] = pd.to_datetime(dfdem.time_end, unit="ms")
dfalbedo["datetime"] = pd.to_datetime(dfalbedo.time, unit="ms")

uniquei = dfdem.id.unique()
# %%
for i in uniquei:
    print("Processing No. %d" % i)
    index = dfdem.id == i
    dfdemsub = dfdem[index]
    index = dfalbedo.id == i
    dfalbedosub = dfalbedo[index]

    dfmerge = pd.merge_asof(
        dfalbedosub.sort_values('datetime'), 
        dfdemsub.sort_values('datetime'), 
        on='datetime',
        allow_exact_matches=False, 
        tolerance=pd.Timedelta(days=3),
        direction='nearest'
    ).dropna()
    dfmerge = dfmerge.drop(columns=['datetime', 'geometry_x', 'longitude_y',
                                    'latitude_y','id_y', 'basin_y', 'geometry_y'])
    dfmerge = dfmerge.rename(columns={
        "longitude_x": "longitude",
        "latitude_x": "latitude",
        "id_x": "id",
        "basin_x": "basin"
    })                    
                
    if i == 0:
        dfmerge.to_csv("/data/shunan/data/topography/topomerge1.csv", 
                        mode="w", index=False, header=True)
    else:
        dfmerge.to_csv("/data/shunan/data/topography/topomerge1.csv", 
                        mode="a", index=False, header=False)


# %%
