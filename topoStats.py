#%%
import pandas as pd
from scipy.stats import ranksums

#%%
'''
South GrIS statistics
'''
df = pd.read_csv("/data/shunan/data/topography/basin/SW_annual.csv")
df = pd.concat([df, pd.read_csv("/data/shunan/data/topography/basin/SE_annual.csv")])
df["distance"] = df.dist/1000
index = df.albedo < 0.45 
df["ice_class"] = "bare ice"
df.ice_class[index] = "dark ice"

print("SW bare ice: \n")
index = (df.basin=="SW") & (df.ice_class == "bare ice")
df[index].describe().to_csv("stat/Sbasin_stat.csv", mode="w")
print("SW dark ice: \n")
index = (df.basin=="SW") & (df.ice_class == "dark ice")
df[index].describe().to_csv("stat/Sbasin_stat.csv", mode="a")
print("SE bare ice: \n")
index = (df.basin=="SE") & (df.ice_class == "bare ice")
df[index].describe().to_csv("stat/Sbasin_stat.csv", mode="a")
print("SE dark ice: \n")
index = (df.basin=="SE") & (df.ice_class == "dark ice")
df[index].describe().to_csv("stat/Sbasin_stat.csv", mode="a")

#%% SW dist-ice class stats
'''
inland ice slope
'''
df = pd.read_csv("/data/shunan/data/topography/basin/SW_annual.csv")
df["distance"] = df.dist/1000
index = df.albedo < 0.45 
df["ice_class"] = "bare ice"
df.ice_class[index] = "dark ice"

index = df.distance> 6.02642477064999
df["dist_class"] = 'margin'
df.dist_class[index] = 'inland'

dftest = df[df.dist_class == "inland"]

print("Compute the Wilcoxon rank-sum statistic for inland ice \n")
ranksums(
    x=dftest.slope[dftest.ice_class == "dark ice"], 
    y=dftest.slope[dftest.ice_class == "bare ice"]   ,
    alternative='less'
)
# %%
