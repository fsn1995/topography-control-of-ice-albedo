#%%
import pandas as pd
from scipy.stats import ranksums
from scipy import stats
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

#%%
'''
Linear regression annual:
'''
df = pd.read_csv("/data/shunan/data/topography/basin/SE_annual.csv")
df["distance"] = df.dist/1000
df["datetime"] = pd.to_datetime(df.time_x, unit="ms")
df["year"] = df.datetime.dt.year
index = df.albedo < 0.45 
df["ice_class"] = "bare ice"
df.ice_class[index] = "dark ice"
index = df.year>2009
df = df[index]
df = df.groupby(["year", "ice_class"]).mean().reset_index()

dfstat = df[df.ice_class == "dark ice"]
slope, intercept, r_value, p_value, std_err = stats.linregress(dfstat.distance.values, dfstat.albedo.values)
print('distance: \ny={0:.4f}x+{1:.4f}\nOLS_r:{2:.2f}, p:{3:.2f}'.format(slope,intercept,r_value,p_value))

slope, intercept, r_value, p_value, std_err = stats.linregress(dfstat.elevation.values, dfstat.albedo.values)
print('elevation: \ny={0:.4f}x+{1:.4f}\nOLS_r:{2:.2f}, p:{3:.2f}'.format(slope,intercept,r_value,p_value))

slope, intercept, r_value, p_value, std_err = stats.linregress(dfstat.slope.values, dfstat.albedo.values)
print('slope: \ny={0:.4f}x+{1:.4f}\nOLS_r:{2:.2f}, p:{3:.2f}'.format(slope,intercept,r_value,p_value))

slope, intercept, r_value, p_value, std_err = stats.linregress(dfstat.aspect.values, dfstat.albedo.values)
print('aspect: \ny={0:.4f}x+{1:.4f}\nOLS_r:{2:.2f}, p:{3:.2f}'.format(slope,intercept,r_value,p_value))

slope, intercept, r_value, p_value, std_err = stats.linregress(dfstat.duration.values, dfstat.albedo.values)
print('duration: \ny={0:.4f}x+{1:.4f}\nOLS_r:{2:.2f}, p:{3:.2f}'.format(slope,intercept,r_value,p_value))



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
