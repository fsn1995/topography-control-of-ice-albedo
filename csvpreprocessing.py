#%%
import vaex as vx
import pandas as pd
import numpy as np


#%% dem
dfhp = pd.read_csv("randomPoints/hp/dem.csv", skiprows=np.arange(1,28067))
dffield = pd.read_csv("randomPoints/field/dem.csv")
dfserver = pd.read_csv("randomPoints/server/dem.csv", skiprows=np.arange(1,28067))


#%%
df = pd.concat([dffield, dfserver, dfhp]).drop(columns=['datetime'])
df.head()
df.to_csv("randomPoints/dem.csv", index=False)

dfvx = vx.from_pandas(df)
dfvx.export_hdf5("randomPoints/dem.hdf5", progress=True)


# %% albedo
dfhp = pd.read_csv("randomPoints/hp/albedo.csv", skiprows=np.arange(1,19976))
dffield = pd.read_csv("randomPoints/field/albedo.csv")
dfserver = pd.read_csv("randomPoints/server/albedo.csv", skiprows=np.arange(1,19976))


#%%
df = pd.concat([dffield, dfserver, dfhp]).drop(columns=['datetime'])
df = df.rename(columns={"visnirAlbedo": "albedo"})
df.head()
df.to_csv("randomPoints/albedo.csv", index=False)

dfvx = vx.from_pandas(df)
dfvx.export_hdf5("randomPoints/albedo.hdf5", progress=True)
# %%
