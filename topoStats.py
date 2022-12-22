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
df = pd.read_csv("/data/shunan/data/topography/basin/SW_annual.csv")
df["distance"] = df.dist/1000
df["datetime"] = pd.to_datetime(df.time_x, unit="ms")
df["year"] = df.datetime.dt.year
index = df.albedo < 0.45 
df["ice_class"] = "bare ice"
df.ice_class[index] = "dark ice"
index = df.year>2009
df = df[index]
# index = df.distance <= 9.57041446875
index = df.distance > 9.57041446875
df = df[index]

df = df.groupby(["year", "ice_class"]).mean().reset_index()

dfstat = df[df.ice_class == "dark ice"]

slope, intercept, r_value, p_value, std_err = stats.linregress(dfstat.elevation.values, dfstat.albedo.values)
print('elevation: \ny={0:.4f}x+{1:.4f}\nOLS_r:{2:.2f}, p:{3:.2f}'.format(slope,intercept,r_value,p_value))

slope, intercept, r_value, p_value, std_err = stats.linregress(dfstat.slope.values, dfstat.albedo.values)
print('slope: \ny={0:.4f}x+{1:.4f}\nOLS_r:{2:.2f}, p:{3:.2f}'.format(slope,intercept,r_value,p_value))

slope, intercept, r_value, p_value, std_err = stats.linregress(dfstat.aspect.values, dfstat.albedo.values)
print('aspect: \ny={0:.4f}x+{1:.4f}\nOLS_r:{2:.2f}, p:{3:.2f}'.format(slope,intercept,r_value,p_value))

slope, intercept, r_value, p_value, std_err = stats.linregress(dfstat.distance.values, dfstat.albedo.values)
print('distance: \ny={0:.4f}x+{1:.4f}\nOLS_r:{2:.2f}, p:{3:.2f}'.format(slope,intercept,r_value,p_value))

slope, intercept, r_value, p_value, std_err = stats.linregress(dfstat.duration.values, dfstat.albedo.values)
print('duration: \ny={0:.4f}x+{1:.4f}\nOLS_r:{2:.2f}, p:{3:.2f}'.format(slope,intercept,r_value,p_value))



#%% SW dist-ice class stats
'''
Are slopes of inland and margin ice different?
'''
df = pd.read_csv("/data/shunan/data/topography/basin/SW_annual.csv")
df["distance"] = df.dist/1000
index = df.albedo < 0.45 
df["ice_class"] = "bare ice"
df.ice_class[index] = "dark ice"

index = df.distance> 9.57041446875
df["dist_class"] = 'margin'
df.dist_class[index] = 'inland'

# slope of inland ice
dftest = df[df.dist_class == "inland"]

ranksums(
    x=dftest.slope[dftest.ice_class == "dark ice"], 
    y=dftest.slope[dftest.ice_class == "bare ice"]   ,
    alternative='greater'
)
ranksums(
    x=dftest.aspect[dftest.ice_class == "dark ice"], 
    y=dftest.aspect[dftest.ice_class == "bare ice"]   ,
    alternative='greater'
)

# slope of margin ice
dftest = df[df.dist_class == "margin"]

print("Compute the Wilcoxon rank-sum statistic for margin ice \n")
ranksums(
    x=dftest.slope[dftest.ice_class == "dark ice"], 
    y=dftest.slope[dftest.ice_class == "bare ice"]   ,
    alternative='greater'
)
ranksums(
    x=dftest.aspect[dftest.ice_class == "dark ice"], 
    y=dftest.aspect[dftest.ice_class == "bare ice"]   ,
    alternative='less'
)
# %%
'''
how many random points generated?
'''
df = pd.read_csv("/data/shunan/data/topography/topomerge.csv")

print("total number of SW basin is: %d"% len(df[df.basin == "SW"].id.unique()))
print("total number of SE basin is: %d"% len(df[df.basin == "SE"].id.unique()))
# %%
'''
percentage of dark ice per region?
'''

df = pd.read_csv("/data/shunan/data/topography/basin/SW_annual.csv")
index = df.albedo < 0.45 
df["ice_class"] = "bare ice"
df.ice_class[index] = "dark ice"
print("percentage of dark ice at SW is %.4f"% (sum(index)/len(index)))

df = pd.read_csv("/data/shunan/data/topography/basin/SE_annual.csv")
index = df.albedo < 0.45 
df["ice_class"] = "bare ice"
df.ice_class[index] = "dark ice"
print("percentage of dark ice at SE is %.4f"% (sum(index)/len(index)))
# %% 
'''
statistics of toporelation fig
'''
df = pd.read_csv("/data/shunan/data/topography/basin/SW_annual.csv")
df = pd.concat([df, pd.read_csv("/data/shunan/data/topography/basin/SE_annual.csv")])
df["distance"] = df.dist/1000
index = df.albedo < 0.45 
df["ice_class"] = "bare ice"
df.ice_class[index] = "dark ice"

# slope
ranksums(
    x=df.slope[(df.ice_class == "dark ice") & (df.basin == "SE")], 
    y=df.slope[(df.ice_class == "dark ice") & (df.basin == "SW")]   ,
    alternative='greater'
)
ranksums(
    x=df.slope[(df.ice_class == "bare ice") & (df.basin == "SE")], 
    y=df.slope[(df.ice_class == "bare ice") & (df.basin == "SW")]   ,
    alternative='greater'
)
ranksums(
    x=df.slope[(df.ice_class == "bare ice") & (df.basin == "SW")], 
    y=df.slope[(df.ice_class == "dark ice") & (df.basin == "SW")]   ,
    alternative='less'
)

# aspect
ranksums(
    x=df.aspect[(df.ice_class == "dark ice") & (df.basin == "SE")], 
    y=df.aspect[(df.ice_class == "dark ice") & (df.basin == "SW")]   ,
    alternative='less'
)
ranksums(
    x=df.aspect[(df.ice_class == "bare ice") & (df.basin == "SE")], 
    y=df.aspect[(df.ice_class == "bare ice") & (df.basin == "SW")]   ,
    alternative='less'
)
ranksums(
    x=df.aspect[(df.ice_class == "bare ice") & (df.basin == "SW")], 
    y=df.aspect[(df.ice_class == "dark ice") & (df.basin == "SW")]   ,
    alternative='greater'
)
ranksums(
    x=df.aspect[(df.ice_class == "bare ice") & (df.basin == "SE")], 
    y=df.aspect[(df.ice_class == "dark ice") & (df.basin == "SE")]   ,
    alternative='greater'
)


#duration
ranksums(
    x=df.duration[(df.ice_class == "dark ice") & (df.basin == "SE")], 
    y=df.duration[(df.ice_class == "dark ice") & (df.basin == "SW")]   ,
    alternative='two-sided'
)
stat, p = stats.levene(
    df.duration[(df.ice_class == "dark ice") & (df.basin == "SE")],
    df.duration[(df.ice_class == "dark ice") & (df.basin == "SW")]
)
# %%
