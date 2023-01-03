#%% import
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import vaex as vx
import numpy as np
import rasterio 
sns.set_theme(style="darkgrid", font="Arial", font_scale=2)


#%% 
'''
topo plot by basin
'''

basin = ['NW', 'SW', 'NO', 'SE', 'NE', 'CW', 'CE'] 

def topo_dist_plot(basin):
    df = pd.read_csv("/data/shunan/data/topography/basin/" + basin + "_annual.csv")
    df["distance"] = df.dist/1000
    df = vx.from_pandas(df)
    df.viz.heatmap('distance', 'albedo', what=np.log(vx.stat.count()), show=True,
                    vmin=0, vmax=4, xlabel="distance (km)", ylabel="albedo")

def topo_elev_plot(basin):
    df = pd.read_csv("/data/shunan/data/topography/basin/" + basin + "_annual.csv")
    df = vx.from_pandas(df)
    df.viz.heatmap('elevation', 'albedo', what=np.log(vx.stat.count()), show=True,
                    vmin=0, vmax=3, xlabel="elevation (m a.s.l)", ylabel="albedo")

def topo_slop_plot(basin):
    df = pd.read_csv("/data/shunan/data/topography/basin/" + basin + "_annual.csv")
    # df["logslope"] = np.log(df.slope)
    df = vx.from_pandas(df)
    df.viz.heatmap('slope', 'albedo', what=np.log(vx.stat.count()), show=True,
                    vmin=0, vmax=5, xlabel="slope (" + u'\N{DEGREE SIGN}' + ')', ylabel="albedo")

def topo_aspe_plot(basin):
    df = pd.read_csv("/data/shunan/data/topography/basin/" + basin + "_annual.csv")
    df = vx.from_pandas(df)
    df.viz.heatmap('aspect', 'albedo', what=np.log(vx.stat.count()), show=True,
                    vmin=0, vmax=2.5, xlabel="aspect (" + u'\N{DEGREE SIGN}' + ')', ylabel="albedo")       

def topo_dura_plot(basin):
    df = pd.read_csv("/data/shunan/data/topography/basin/" + basin + "_annual.csv")
    df = vx.from_pandas(df)
    df.viz.heatmap('duration', 'albedo', what=np.log(vx.stat.count()), show=True,
                    vmin=0, vmax=4.5, xlabel="duration (days)" , ylabel="albedo")                                      

for i in basin:
    fig, ax = plt.subplots(figsize=(6,4))
    ax.annotate(i, xy=(0.7, 0.1),  xycoords='axes fraction')
    ax.axhline(0.45, ls='--', linewidth=3)
    plt.xlim(0, 100)
    plt.ylim(0, 0.65)
    topo_dist_plot(i)
    fig.savefig("print/basin/" + i + "_dist.png", dpi=300, bbox_inches="tight")
    
for i in basin:
    fig, ax = plt.subplots(figsize=(6,4))
    ax.annotate(i, xy=(0.7, 0.1),  xycoords='axes fraction')
    ax.axhline(0.45, ls='--', linewidth=3)
    plt.xlim(0, 2000)
    plt.ylim(0, 0.65)
    topo_elev_plot(i)
    fig.savefig("print/basin/" + i + "_elev.png", dpi=300, bbox_inches="tight")

for i in basin:
    fig, ax = plt.subplots(figsize=(6,4))
    ax.annotate(i, xy=(0.7, 0.1),  xycoords='axes fraction')
    ax.axhline(0.45, ls='--', linewidth=3)
    plt.xlim(0, 50)
    plt.ylim(0, 0.65)
    topo_slop_plot(i)
    fig.savefig("print/basin/" + i + "_slop.png", dpi=300, bbox_inches="tight")

for i in basin:
    fig, ax = plt.subplots(figsize=(6,4))
    ax.annotate(i, xy=(0.7, 0.1),  xycoords='axes fraction')
    ax.axhline(0.45, ls='--', linewidth=3)
    plt.xlim(0, 360)
    plt.ylim(0, 0.65)
    topo_aspe_plot(i)
    fig.savefig("print/basin/" + i + "_aspe.png", dpi=300, bbox_inches="tight")        

for i in basin:
    fig, ax = plt.subplots(figsize=(6,4))
    ax.annotate(i, xy=(0.7, 0.1),  xycoords='axes fraction')
    ax.axhline(0.45, ls='--', linewidth=3)
    plt.xlim(0, 61)
    plt.ylim(0, 0.65)
    topo_dura_plot(i)
    fig.savefig("print/basin/" + i + "_dura.png", dpi=300, bbox_inches="tight")     

#%%
'''
topo histogram by basin
'''
df = pd.read_csv("/data/shunan/data/topography/basin/SW_annual.csv")
df = pd.concat([df, pd.read_csv("/data/shunan/data/topography/basin/SE_annual.csv")])
df["distance"] = df.dist/1000
index = df.albedo < 0.45 
df["ice_class"] = "bare ice"
df.ice_class[index] = "dark ice"

fig, ax = plt.subplots(figsize=(6,3))
sns.boxplot(
    data=df,
    x="slope",
    hue="ice_class",
    y="basin"
)
plt.legend(bbox_to_anchor=(1.04, 1.31), ncol=2)
ax.set(ylabel="", xlabel="slope (" + u'\N{DEGREE SIGN}' + ')')
fig.savefig("print/basin/box_slop.png", dpi=300, bbox_inches="tight")

fig, ax = plt.subplots(figsize=(6,3))
sns.boxplot(
    data=df,
    x="elevation",
    hue="ice_class",
    y="basin"
)
plt.legend(bbox_to_anchor=(1.04, 1.31), ncol=2)
ax.set(ylabel="", xlabel="elevation (m a.s.l)" )
fig.savefig("print/basin/box_elev.png", dpi=300, bbox_inches="tight")

fig, ax = plt.subplots(figsize=(6,3))
sns.boxplot(
    data=df,
    x="distance",
    hue="ice_class",
    y="basin"
)
plt.legend(bbox_to_anchor=(1.04, 1.31), ncol=2)
ax.set(ylabel="", xlabel="distance (km)" )
fig.savefig("print/basin/box_dist.png", dpi=300, bbox_inches="tight")

fig, ax = plt.subplots(figsize=(6,3))
sns.boxplot(
    data=df,
    x="aspect",
    hue="ice_class",
    y="basin"
)
plt.legend(bbox_to_anchor=(1.04, 1.31), ncol=2)
ax.set(ylabel="", xlabel="aspect (" + u'\N{DEGREE SIGN}' + ')' )
fig.savefig("print/basin/box_aspe.png", dpi=300, bbox_inches="tight")

fig, ax = plt.subplots(figsize=(6,3))
sns.boxplot(
    data=df,
    x="duration",
    hue="ice_class",
    y="basin"
)
plt.legend(bbox_to_anchor=(1.04, 1.31), ncol=2)
ax.set(ylabel="", xlabel="duration (days)")
fig.savefig("print/basin/box_dura.png", dpi=300, bbox_inches="tight")


#%%
'''
ice at margin and inland comparison (SW)
'''

df = pd.read_csv("/data/shunan/data/topography/basin/SW_annual.csv")
df["distance"] = df.dist/1000
index = df.albedo < 0.45 
df["ice_class"] = "bare ice"
df.ice_class[index] = "dark ice"

index = df.distance> 9.57041446875
df["dist_class"] = 'margin'
df.dist_class[index] = 'inland'

fig, ax = plt.subplots(1, 3, figsize=(12,3))
sns.boxenplot(ax=ax[0], data=df, x="elevation", y="dist_class", hue="ice_class")
ax[0].set(xlabel="elevation (m a.s.l)", ylabel="")
ax[0].get_legend().remove()
ax[0].annotate("a)", xy=(-0.15, 0.9),  xycoords='axes fraction')
ax[0].set_xticks([0, 1000, 2000]);  # Set text labels.
sns.boxenplot(ax=ax[1], data=df, x="slope", y="dist_class", hue="ice_class")
ax[1].set(xlabel="slope (" + u'\N{DEGREE SIGN}' + ')', ylabel="", yticklabels=[])
sns.move_legend(ax[1], "upper center", bbox_to_anchor=(0.5, 1.35), ncol=2, title=None)
ax[1].annotate("b)", xy=(-0.15, 0.9),  xycoords='axes fraction')
# plt.legend(bbox_to_anchor=(1.04, 1.31), ncol=2)
# plt.yticks(rotation="vertical", ha="right")
sns.boxenplot(ax=ax[2], data=df, x="aspect", y="dist_class", hue="ice_class")
ax[2].set(xlabel="aspect (" + u'\N{DEGREE SIGN}' + ')', ylabel="", yticklabels=[])
ax[2].get_legend().remove()
ax[2].annotate("c)", xy=(-0.15, 0.9),  xycoords='axes fraction')
ax[2].set_xticks([0, 90, 180, 270, 360]);  # Set text labels.
fig.savefig("print/SW_classdist_box.pdf", dpi=300, bbox_inches="tight")

#%%
'''
bare ice, duration and albedo, linear regression at SW
'''
df = pd.read_csv("/data/shunan/data/topography/basin/SW_annual.csv")
# df = pd.concat([df, pd.read_csv("/data/shunan/data/topography/basin/SE_annual.csv")])
df["distance"] = df.dist/1000
df["datetime"] = pd.to_datetime(df.time_x, unit="ms")
df["year"] = df.datetime.dt.year
index = df.albedo < 0.45 
df["ice_class"] = "bare ice"
df.ice_class[index] = "dark ice"
index = df.year>2009
df = df[index]

index = df.distance <= 9.57041446875
# index = df.distance > 9.57041446875
df = df[index]

fig, ax = plt.subplots(5, 1, figsize=(4,12))
# sns.lineplot(ax=ax[0], data=df, x="year", y="albedo", hue="ice_class")
# ax[0].legend(bbox_to_anchor=(0.9, 1.31), ncol=2)
# ax[0].set(xlabel="", ylabel="albedo", xticklabels=[])
# fig, ax = plt.subplots(figsize=(8,4))
sns.lineplot(ax=ax[0], data=df, x="year", y="elevation", hue="ice_class")
ax[0].set(xlabel="", ylabel="elevation (m a.s.l)", xticklabels=[])
ax[0].legend(bbox_to_anchor=(1.1, 1.35), ncol=2)
# fig, ax = plt.subplots(figsize=(8,4))
sns.lineplot(ax=ax[3], data=df, x="year", y="distance", hue="ice_class", legend=False)
ax[3].set(xlabel="", ylabel="distance (km)", xticklabels=[])
# fig, ax = plt.subplots(figsize=(8,4))
sns.lineplot(ax=ax[1], data=df, x="year", y="slope", hue="ice_class", legend=False)
ax[1].set(xlabel="", ylabel="slope (" + u'\N{DEGREE SIGN}' + ')', xticklabels=[])
# fig, ax = plt.subplots(figsize=(8,4))
sns.lineplot(ax=ax[2], data=df, x="year", y="aspect", hue="ice_class", legend=False)
ax[2].set(xlabel="", ylabel="aspect (" + u'\N{DEGREE SIGN}' + ')', xticklabels=[])
# fig, ax = plt.subplots(figsize=(8,4))
sns.lineplot(ax=ax[4], data=df, x="year", y="duration", hue="ice_class", legend=False)
ax[4].set(xlabel="", ylabel="duration (days)")
fig.savefig("print/basin/SW_margin_lineplot.png", dpi=300, bbox_inches="tight")

df = df.groupby(["year", "ice_class"]).mean().reset_index()

g=sns.lmplot(data=df, x="distance", y="albedo", hue="ice_class", legend=False, height=2.4, aspect=1.2)
ax=g.axes.flat
ax[0].set(xlabel="distance (km)", ylabel="albedo")
g.savefig("print/basin/SW_margin_linear_dist.png", dpi=300, bbox_inches="tight")

g=sns.lmplot(data=df, x="elevation", y="albedo", hue="ice_class", legend=False, height=2.4, aspect=1.2)
ax=g.axes.flat
ax[0].set(xlabel="elevation (m a.s.l)", ylabel="albedo")
g.savefig("print/basin/SW_margin_linear_elev.png", dpi=300, bbox_inches="tight")

g=sns.lmplot(data=df, x="slope", y="albedo", hue="ice_class", legend=False, height=2.4, aspect=1.2)
ax=g.axes.flat
ax[0].set(xlabel="slope (" + u'\N{DEGREE SIGN}' + ')', ylabel="albedo")
g.savefig("print/basin/SW_margin_linear_slop.png", dpi=300, bbox_inches="tight")

g=sns.lmplot(data=df, x="aspect", y="albedo", hue="ice_class", legend=False, height=2.4, aspect=1.2)
ax=g.axes.flat
ax[0].set(xlabel="aspect (" + u'\N{DEGREE SIGN}' + ')', ylabel="albedo")
g.savefig("print/basin/SW_margin_linear_aspe.png", dpi=300, bbox_inches="tight")

g=sns.lmplot(data=df, x="duration", y="albedo", hue="ice_class", legend=False, height=2.4, aspect=1.2)
ax=g.axes.flat
ax[0].set(xlabel="duration (days)", ylabel="albedo")
g.savefig("print/basin/SW_margin_linear_dura.png", dpi=300, bbox_inches="tight")
#%%
'''
bare ice, duration and albedo, linear regression at SE
'''
df = pd.read_csv("/data/shunan/data/topography/basin/SE_annual.csv")
# df = pd.concat([df, pd.read_csv("/data/shunan/data/topography/basin/SE_annual.csv")])
df["distance"] = df.dist/1000
df["datetime"] = pd.to_datetime(df.time_x, unit="ms")
df["year"] = df.datetime.dt.year
index = df.albedo < 0.45 
df["ice_class"] = "bare ice"
df.ice_class[index] = "dark ice"
index = df.year>2009
df = df[index]

fig, ax = plt.subplots(5, 1, figsize=(8,16))
# sns.lineplot(ax=ax[0], data=df, x="year", y="albedo", hue="ice_class")
# ax[0].legend(bbox_to_anchor=(0.9, 1.31), ncol=2)
# ax[0].set(xlabel="", ylabel="albedo", xticklabels=[])
# fig, ax = plt.subplots(figsize=(8,4))
sns.lineplot(ax=ax[0], data=df, x="year", y="elevation", hue="ice_class")
ax[0].set(xlabel="", ylabel="elevation (m a.s.l)", xticklabels=[])
ax[0].legend(bbox_to_anchor=(0.9, 1.31), ncol=2)
# fig, ax = plt.subplots(figsize=(8,4))
sns.lineplot(ax=ax[3], data=df, x="year", y="distance", hue="ice_class", legend=False)
ax[3].set(xlabel="", ylabel="distance (km)", xticklabels=[])
# fig, ax = plt.subplots(figsize=(8,4))
sns.lineplot(ax=ax[1], data=df, x="year", y="slope", hue="ice_class", legend=False)
ax[1].set(xlabel="", ylabel="slope (" + u'\N{DEGREE SIGN}' + ')', xticklabels=[])
# fig, ax = plt.subplots(figsize=(8,4))
sns.lineplot(ax=ax[2], data=df, x="year", y="aspect", hue="ice_class", legend=False)
ax[2].set(xlabel="", ylabel="aspect (" + u'\N{DEGREE SIGN}' + ')', xticklabels=[])
# fig, ax = plt.subplots(figsize=(8,4))
sns.lineplot(ax=ax[4], data=df, x="year", y="duration", hue="ice_class", legend=False)
ax[4].set(xlabel="", ylabel="duration (days)")
fig.savefig("print/basin/SE_lineplot.png", dpi=300, bbox_inches="tight")

df = df.groupby(["year", "ice_class"]).mean().reset_index()

g=sns.lmplot(data=df, x="distance", y="albedo", hue="ice_class", legend=False, height=4, aspect=1)
ax=g.axes.flat
ax[0].set(xlabel="distance (km)", ylabel="albedo")
g.savefig("print/basin/SE_linear_dist.png", dpi=300, bbox_inches="tight")

g=sns.lmplot(data=df, x="elevation", y="albedo", hue="ice_class", legend=False, height=4, aspect=1)
ax=g.axes.flat
ax[0].set(xlabel="elevation (m a.s.l)", ylabel="albedo")
g.savefig("print/basin/SE_linear_elev.png", dpi=300, bbox_inches="tight")

g=sns.lmplot(data=df, x="slope", y="albedo", hue="ice_class", legend=False, height=4, aspect=1)
ax=g.axes.flat
ax[0].set(xlabel="slope (" + u'\N{DEGREE SIGN}' + ')', ylabel="albedo")
g.savefig("print/basin/SE_linear_slop.png", dpi=300, bbox_inches="tight")

g=sns.lmplot(data=df, x="aspect", y="albedo", hue="ice_class", legend=False, height=4, aspect=1)
ax=g.axes.flat
ax[0].set(xlabel="aspect (" + u'\N{DEGREE SIGN}' + ')', ylabel="albedo")
g.savefig("print/basin/SE_linear_aspe.png", dpi=300, bbox_inches="tight")

g=sns.lmplot(data=df, x="duration", y="albedo", hue="ice_class", legend=False, height=4, aspect=1)
ax=g.axes.flat
ax[0].set(xlabel="duration (days)", ylabel="albedo")
g.savefig("print/basin/SE_linear_dura.png", dpi=300, bbox_inches="tight")


#%%
'''
DEM analysis and plot
'''
src = rasterio.open("/data/shunan/data/topography/dem/clip/Clip_OutRaster_SW_tif.tif")
swdem = src.read(1)
src.close()
index = swdem < 0
swdem[index] = np.nan
swdem = swdem.flatten()

src = rasterio.open("/data/shunan/data/topography/dem/clip/Clip_OutRaster_SE_tif.tif")
sedem = src.read(1)
src.close()
index = sedem < 0
sedem[index] = np.nan
sedem = sedem.flatten()
df = pd.DataFrame({'swdem': pd.Series(swdem), 'sedem': pd.Series(sedem)})
df = vx.from_pandas(df)

fig, ax = plt.subplots(figsize=(6, 4))
df.viz.histogram('sedem', what=vx.stat.count()*32*32/1000000, label='SE', linewidth=2)
df.viz.histogram('swdem', what=vx.stat.count()*32*32/1000000, label='SW', linewidth=2)
ax.axvline(1453, ls='--', linewidth=2, color=(0.2980392156862745, 0.4470588235294118, 0.6901960784313725))
ax.axvline(1550, ls='--', linewidth=2, color=(0.8666666666666667, 0.5176470588235295, 0.3215686274509804))
plt.legend()
ax.set(xlabel="elevation (m a.s.l)", ylabel="area (km$^2$)")
sns.move_legend(ax, "upper left", bbox_to_anchor=(-0.03, 1))
fig.savefig("print/elevhist.svg", dpi=300, bbox_inches="tight")


src = rasterio.open("/data/shunan/data/topography/dem/clip/Clip_OutRaster_SW_slope_tif.tif")
swdem = src.read(1)
src.close()
index = swdem < 0
swdem[index] = np.nan
swdem = swdem.flatten()

src = rasterio.open("/data/shunan/data/topography/dem/clip/Clip_OutRaster_SE_slope_tif.tif")
sedem = src.read(1)
src.close()
index = sedem < 0
sedem[index] = np.nan
sedem = sedem.flatten()
df = pd.DataFrame({'swdem': pd.Series(swdem), 'sedem': pd.Series(sedem)})
df = vx.from_pandas(df)

fig, ax = plt.subplots(figsize=(6, 4))
df.viz.histogram('sedem', label='SE')
df.viz.histogram('swdem', label='SW')
plt.legend()
ax.set(xlabel="slope (" + u'\N{DEGREE SIGN}' + ')')
fig.savefig("print/slophist.pdf", dpi=300, bbox_inches="tight")

src = rasterio.open("/data/shunan/data/topography/dem/clip/Clip_OutRaster_SW_aspect_tif.tif")
swdem = src.read(1).astype(np.float32)
src.close()
index = swdem < 0
swdem[index] = np.nan
swdem = swdem.flatten()

src = rasterio.open("/data/shunan/data/topography/dem/clip/Clip_OutRaster_SE_aspect_tif.tif")
sedem = src.read(1).astype(np.float32)
src.close()
index = sedem < 0
sedem[index] = np.nan
sedem = sedem.flatten()
df = pd.DataFrame({'swdem': pd.Series(swdem), 'sedem': pd.Series(sedem)})
df = vx.from_pandas(df)

fig, ax = plt.subplots(figsize=(6, 4))
df.viz.histogram('sedem', label='SE')
df.viz.histogram('swdem', label='SW')
plt.legend()
ax.set(xlabel="aspect (" + u'\N{DEGREE SIGN}' + ')')
fig.savefig("print/aspehist.pdf", dpi=300, bbox_inches="tight")



#%%
'''
play with dark ice at SW
'''
df = pd.read_csv("/data/shunan/data/topography/basin/SW_annual.csv")
df["distance"] = df.dist/1000

df = df[df.albedo < 0.45]
df["tan"] = df.elevation / df.dist
df["arctan"] = np.rad2deg(np.arctan2(df.elevation, df.dist))

dfvx = vx.from_pandas(df)

fig, ax = plt.subplots(figsize=(6,5))
ax.annotate("SW", xy=(0.8, 0.8),  xycoords='axes fraction')
ax.axvline(9.57041446875, ls='--', linewidth=3)
# ax.axhline(673.3710066, ls='--', linewidth=3)
plt.xlim(0,90)
plt.ylim(0,90)
dfvx.viz.heatmap('distance', 'slope', what=np.log(vx.stat.count()), show=True,
                 vmin=0, vmax=6, xlabel="distance (km)", ylabel="slope (" + u'\N{DEGREE SIGN}' + ')' )
fig.savefig("print/basin/SW_dark_dist_slop.png", dpi=300, bbox_inches="tight")

fig, ax = plt.subplots(figsize=(6,5))
ax.annotate("SW", xy=(0.8, 0.1),  xycoords='axes fraction')
ax.axvline(9.57041446875, ls='--', linewidth=3)
# ax.axhline(673.3710066, ls='--', linewidth=3)
plt.xlim(0,90)
plt.ylim(0,2000)
dfvx.viz.heatmap('distance', 'elevation', what=np.log(vx.stat.count()), show=True,
                 vmin=0, vmax=4, xlabel="distance (km)", ylabel="elevation (m a.s.l)")
fig.savefig("print/basin/SW_dark_dist_elev.png", dpi=300, bbox_inches="tight")


fig, ax = plt.subplots(figsize=(6,5))   
ax.axvline(9.57041446875, ls='--', linewidth=3)
ax.annotate("SW", xy=(0.8, 0.8),  xycoords='axes fraction')
plt.xlim(0, 90)
plt.ylim(0, 360)
dfvx.viz.heatmap('distance', 'aspect', what=np.log(vx.stat.count()), show=True,
                  vmin=0, vmax=3, xlabel="distance (km)", ylabel="aspect (" + u'\N{DEGREE SIGN}' + ')')
fig.savefig("print/basin/SW_dark_dist_aspe.png", dpi=300, bbox_inches="tight")

#%%
'''
play with dark ice at SE
'''
df = pd.read_csv("/data/shunan/data/topography/basin/SE_annual.csv")
df["distance"] = df.dist/1000

df = df[df.albedo < 0.45]
df["tan"] = df.elevation / df.dist
df["arctan"] = np.rad2deg(np.arctan2(df.elevation, df.dist))

dfvx = vx.from_pandas(df)

fig, ax = plt.subplots(figsize=(6,5))
ax.annotate("SE", xy=(0.8, 0.8),  xycoords='axes fraction')
ax.axvline(2.63818006441, ls='--', linewidth=3)
# ax.axhline(673.3710066, ls='--', linewidth=3)
plt.xlim(0,90)
plt.ylim(0,90)
dfvx.viz.heatmap('distance', 'slope', what=np.log(vx.stat.count()), show=True,
                 vmin=0, vmax=6, xlabel="distance (km)", ylabel="slope (" + u'\N{DEGREE SIGN}' + ')' )
fig.savefig("print/basin/SE_dark_dist_slop.png", dpi=300, bbox_inches="tight")

fig, ax = plt.subplots(figsize=(6,5))
ax.annotate("SE", xy=(0.8, 0.1),  xycoords='axes fraction')
ax.axvline(2.63818006441, ls='--', linewidth=3)
# ax.axhline(673.3710066, ls='--', linewidth=3)
plt.xlim(0,90)
plt.ylim(0,2000)
dfvx.viz.heatmap('distance', 'elevation', what=np.log(vx.stat.count()), show=True,
                 vmin=0, vmax=4, xlabel="distance (km)", ylabel="elevation (m a.s.l)")
fig.savefig("print/basin/SE_dark_dist_elev.png", dpi=300, bbox_inches="tight")


fig, ax = plt.subplots(figsize=(6,5))   
ax.axvline(2.63818006441, ls='--', linewidth=3)
ax.annotate("SE", xy=(0.8, 0.8),  xycoords='axes fraction')
plt.xlim(0, 90)
plt.ylim(0, 360)
dfvx.viz.heatmap('distance', 'aspect', what=np.log(vx.stat.count()), show=True,
                  vmin=0, vmax=3, xlabel="distance (km)", ylabel="aspect (" + u'\N{DEGREE SIGN}' + ')')
fig.savefig("print/basin/SE_dark_dist_aspe.png", dpi=300, bbox_inches="tight")

#%%
# fig, ax = plt.subplots(figsize=(6,5))
# # ax.annotate("SW", xy=(0.8, 0.1),  xycoords='axes fraction')
# # ax.axvline(9.57041446875, ls='--', linewidth=3)
# plt.xlim(0,90)
# plt.ylim(0,2000)
# dfvx.viz.heatmap('distance', 'elevation', what=np.log(vx.stat.count()), show=True,
#                  vmin=0, vmax=4, xlabel="distance (km)", ylabel="elevation (m)")
# fig.savefig("print/basin/SW_bare_dist_elev.png", dpi=300, bbox_inches="tight")

# fig, ax = plt.subplots(figsize=(6,5))
# # ax.annotate("SW", xy=(0.8, 0.1),  xycoords='axes fraction')
# ax.axvline(9.57041446875, ls='--', linewidth=3)
# plt.xlim(0,90)
# plt.ylim(0,90)
# dfvx.viz.heatmap('distance', 'slope', what=np.log(vx.stat.count()), show=True,
#                  vmin=0, vmax=6, xlabel="distance (km)", ylabel="slope (" + u'\N{DEGREE SIGN}' + ')')
# fig.savefig("print/basin/SW_bare_dist_slop.png", dpi=300, bbox_inches="tight")

# index = df.distance> 9.57041446875
# df["dist_class"] = 'margin'
# df.dist_class[index] = 'inland'
# fig, ax = plt.subplots(figsize=(6,5))
# sns.boxplot(
#     data=df,
#     x="slope",
#     y="dist_class"
# )

#%%
# df = pd.read_csv("/data/shunan/data/topography/basin/SW_annual.csv")
# df["distance"] = df.dist/1000
# index = df.albedo < 0.45 
# df["ice_class"] = "bare ice"
# df.ice_class[index] = "dark ice"
# df["tan"] = df.elevation / df.dist
# df["arctan"] = np.rad2deg(np.arctan2(df.elevation, df.dist))

# dfvx = df[index]
# dfvx = vx.from_pandas(dfvx)

# fig, ax = plt.subplots(figsize=(6,5))
# ax.annotate("SW", xy=(0.8, 0.8),  xycoords='axes fraction')
# plt.xlim(0,70)
# plt.ylim(0,90)
# dfvx.viz.heatmap('distance', 'arctan', what=np.log(vx.stat.count()), show=True,
#                   vmin=0, vmax=6, xlabel="distance (km)", ylabel="slope (" + u'\N{DEGREE SIGN}' + ')' )

# fig, ax = plt.subplots(figsize=(6,5))
# ax.annotate("SW", xy=(0.8, 0.1),  xycoords='axes fraction')
# plt.xlim(0,50)
# plt.ylim(0,2000)
# dfvx.viz.heatmap('distance', 'elevation', what=np.log(vx.stat.count()), show=True,
#                  vmin=0, vmax=4, xlabel="distance (km)", ylabel="elevation (m)")
# fig.savefig("print/basin/SW_dist_elev.png", dpi=300, bbox_inches="tight")


# dfvx = df[~index]
# dfvx = vx.from_pandas(dfvx)    
# fig, ax = plt.subplots(figsize=(6,5))   
# ax.annotate("SW", xy=(0.8, 0.8),  xycoords='axes fraction')
# plt.xlim(0, 70)
# plt.ylim(0, 90)
# dfvx.viz.heatmap('distance', 'arctan', what=np.log(vx.stat.count()), show=True,
#                   vmin=0, vmax=6, xlabel="distance (km)", ylabel="slope (" + u'\N{DEGREE SIGN}' + ')')

# fig, ax = plt.subplots(figsize=(6,5))
# ax.annotate("SW", xy=(0.8, 0.1),  xycoords='axes fraction')
# plt.xlim(0,100)
# plt.ylim(0,2000)
# dfvx.viz.heatmap('distance', 'elevation', what=np.log(vx.stat.count()), show=True,
#                     xlabel="distance (km)", ylabel="elevation (m)")

# #%%
# df = pd.read_csv("/data/shunan/data/topography/basin/SE_annual.csv")
# df["distance"] = df.dist/1000
# index = df.albedo < 0.45 
# df["ice_class"] = "bare ice"
# df.ice_class[index] = "dark ice"
# df["tan"] = df.elevation / df.dist
# df["arctan"] = np.rad2deg(np.arctan2(df.elevation, df.dist))

# dfvx = df[index]
# dfvx = vx.from_pandas(dfvx)

# fig, ax = plt.subplots(figsize=(6,5))
# ax.annotate("SE", xy=(0.8, 0.8),  xycoords='axes fraction')
# plt.xlim(0,70)
# plt.ylim(0,30)
# dfvx.viz.heatmap('distance', 'arctan', what=np.log(vx.stat.count()), show=True,
#                   vmin=0, vmax=6, xlabel="distance (km)", ylabel="slope (" + u'\N{DEGREE SIGN}' + ')' )


# fig, ax = plt.subplots(figsize=(6,5))
# ax.annotate("SE", xy=(0.8, 0.1),  xycoords='axes fraction')
# plt.xlim(0,50)
# plt.ylim(0,2000)
# dfvx.viz.heatmap('distance', 'elevation', what=np.log(vx.stat.count()), show=True,
#                  vmin=0, vmax=4, xlabel="distance (km)", ylabel="elevation (m)")
# fig.savefig("print/basin/SE_dist_elev.png", dpi=300, bbox_inches="tight")


# dfvx = df[~index]
# dfvx = vx.from_pandas(dfvx)    
# fig, ax = plt.subplots(figsize=(6,5))   
# ax.annotate("SE", xy=(0.8, 0.8),  xycoords='axes fraction')
# plt.xlim(0, 70)
# plt.ylim(0, 30)
# dfvx.viz.heatmap('distance', 'slope', what=np.log(vx.stat.count()), show=True,
#                   vmin=0, vmax=6, xlabel="distance (km)", ylabel="slope (" + u'\N{DEGREE SIGN}' + ')')

# fig, ax = plt.subplots(figsize=(6,5))
# ax.annotate("SE", xy=(0.8, 0.1),  xycoords='axes fraction')
# plt.xlim(0,100)
# plt.ylim(0,2000)
# dfvx.viz.heatmap('distance', 'elevation', what=np.log(vx.stat.count()), show=True,
#                     xlabel="distance (km)", ylabel="elevation (m)")

#%%
# df = pd.read_csv("/data/shunan/data/topography/basin/SE_annual.csv")
# df["distance"] = df.dist/1000
# index = df.albedo < 0.45 
# df["ice_class"] = "bare ice"
# df.ice_class[index] = "dark ice"

# sns.histplot(data=df, x="distance", y="elevation", hue="ice_class")

# g = sns.JointGrid(data=df, x="distance", y="slope", hue="ice_class")
# g.plot_joint(sns.scatterplot, alpha=.3, s=50,)
# g.plot_marginals(sns.boxplot)

# #%%
# g = sns.PairGrid(df, hue="ice_class", vars=["elevation", "slope", "aspect", "distance"])
# g.map_diag(sns.histplot)
# g.map_offdiag(sns.histplot)
# g.add_legend()

# # sns.pairplot(
#     data=df,
#     hue="ice_class",
#     vars={"elevation", "slope", "aspect", "distance"}
# )
# sns.displot(
#     data=df,
#     x="distance",
#     y="slope",
#     hue="ice_class",

# )

#%%

# def topo_violin_plot(df, min_month, max_month, basin):
#     index = (df.month>min_month) & (df.month<max_month)
#     fig, ax = plt.subplots(figsize=(6,4))
#     sns.violinplot(
#         data=df[index],
#         x="month",
#         y="elevation",
#         hue="ice_class",
#         split=True,
#         inner="quart"
#     )
#     plt.legend(bbox_to_anchor=(1, 1.5), ncol=2)
#     ax.set(title=basin)

#     fig, ax = plt.subplots(figsize=(6,4))
#     sns.violinplot(
#         data=df[index],
#         x="month",
#         y="slope",
#         hue="ice_class",
#         split=True,
#         inner="quart"
#     )
#     plt.legend(bbox_to_anchor=(1, 1.5), ncol=2)
#     ax.set(title=basin)

#     fig, ax = plt.subplots(figsize=(6,4))
#     sns.violinplot(
#         data=df[index],
#         x="month",
#         y="aspect",
#         hue="ice_class",
#         split=True,
#         inner="quart"
#     )
#     plt.legend(bbox_to_anchor=(1, 1.5), ncol=2)
#     ax.set(title=basin)

# # %% SW
# df = pd.read_csv("/data/shunan/data/topography/basin/SW.csv")

# index = df.albedo < 0.45 
# df["ice_class"] = "bare ice"
# df.ice_class[index] = "dark ice"

# topo_violin_plot(df, 6, 9, "SW")
# # sns.histplot(
# #     data=df,
# #     x="elevation",
# #     hue="ice_class"
# # )
# # %% SE
# df = pd.read_csv("/data/shunan/data/topography/basin/SE.csv")

# index = df.albedo < 0.45 
# df["ice_class"] = "bare ice"
# df.ice_class[index] = "dark ice"

# topo_violin_plot(df, 6, 9, "SE")

# # %% NW
# df = pd.read_csv("/data/shunan/data/topography/basin/NW.csv")

# index = df.albedo < 0.45 
# df["ice_class"] = "bare ice"
# df.ice_class[index] = "dark ice"

# topo_violin_plot(df, 6, 9, "NW")

# # %% NO
# df = pd.read_csv("/data/shunan/data/topography/basin/NO.csv")

# index = df.albedo < 0.45 
# df["ice_class"] = "bare ice"
# df.ice_class[index] = "dark ice"

# topo_violin_plot(df, 6, 9, "NO")

# # %% NE
# df = pd.read_csv("/data/shunan/data/topography/basin/NE.csv")

# index = df.albedo < 0.45 
# df["ice_class"] = "bare ice"
# df.ice_class[index] = "dark ice"

# topo_violin_plot(df, 6, 9, "NE")

# # %% CW
# df = pd.read_csv("/data/shunan/data/topography/basin/CW.csv")

# index = df.albedo < 0.45 
# df["ice_class"] = "bare ice"
# df.ice_class[index] = "dark ice"

# topo_violin_plot(df, 6, 9, "CW")

# # %% CE
# df = pd.read_csv("/data/shunan/data/topography/basin/CE.csv")

# index = df.albedo < 0.45 
# df["ice_class"] = "bare ice"
# df.ice_class[index] = "dark ice"

# topo_violin_plot(df, 6, 9, "CE")


# #%%
# '''
# topo plot by basin
# '''

# basin = ['NW', 'SW', 'NO', 'SE', 'NE', 'CW', 'CE'] 

# def topo_dist_plot(min_month, max_month, basin):
#     df = pd.read_csv("/data/shunan/data/topography/basin/" + basin + ".csv")
#     df["distance"] = df.dist/1000

#     index = (df.month>min_month) & (df.month<max_month)
#     df = vx.from_pandas(df[index])
#     df.viz.heatmap('distance', 'albedo', what=np.log(vx.stat.count()), show=True,
#                     vmin=0, vmax=4, xlabel="distance (km)", ylabel="albedo")

# def topo_elev_plot(min_month, max_month, basin):
#     df = pd.read_csv("/data/shunan/data/topography/basin/" + basin + ".csv")

#     index = (df.month>min_month) & (df.month<max_month)
#     df = vx.from_pandas(df[index])
#     df.viz.heatmap('elevation', 'albedo', what=np.log(vx.stat.count()), show=True,
#                     vmin=0, vmax=3, xlabel="elevation (m a.s.l)", ylabel="albedo")

# def topo_slop_plot(min_month, max_month, basin):
#     df = pd.read_csv("/data/shunan/data/topography/basin/" + basin + ".csv")
#     df["logslope"] = np.log(df.slope)
#     index = (df.month>min_month) & (df.month<max_month)
#     df = vx.from_pandas(df[index])
#     df.viz.heatmap('slope', 'albedo', what=np.log(vx.stat.count()), show=True,
#                     vmin=0, vmax=5, xlabel="slope (" + u'\N{DEGREE SIGN}' + ')', ylabel="albedo")

# def topo_aspe_plot(min_month, max_month, basin):
#     df = pd.read_csv("/data/shunan/data/topography/basin/" + basin + ".csv")

#     index = (df.month>min_month) & (df.month<max_month)
#     df = vx.from_pandas(df[index])
#     df.viz.heatmap('aspect', 'albedo', what=np.log(vx.stat.count()), show=True,
#                     vmin=0, vmax=2.5, xlabel="aspect (" + u'\N{DEGREE SIGN}' + ')', ylabel="albedo")                    

# for i in basin:
#     fig, ax = plt.subplots(figsize=(6,4))
#     ax.annotate(i, xy=(0.7, 0.1),  xycoords='axes fraction')
#     ax.axhline(0.45, ls='--', linewidth=3)
#     plt.xlim(0, 100)
#     plt.ylim(0, 0.65)
#     topo_dist_plot(6, 9, i)
#     fig.savefig("print/basin/" + i + "_dist.png", dpi=300, bbox_inches="tight")
    
# for i in basin:
#     fig, ax = plt.subplots(figsize=(6,4))
#     ax.annotate(i, xy=(0.7, 0.1),  xycoords='axes fraction')
#     ax.axhline(0.45, ls='--', linewidth=3)
#     plt.xlim(0, 2000)
#     plt.ylim(0, 0.65)
#     topo_elev_plot(6, 9, i)
#     fig.savefig("print/basin/" + i + "_elev.png", dpi=300, bbox_inches="tight")

# for i in basin:
#     fig, ax = plt.subplots(figsize=(6,4))
#     ax.annotate(i, xy=(0.7, 0.1),  xycoords='axes fraction')
#     ax.axhline(0.45, ls='--', linewidth=3)
#     plt.xlim(0, 50)
#     plt.ylim(0, 0.65)
#     topo_slop_plot(6, 9, i)
#     fig.savefig("print/basin/" + i + "_slop.png", dpi=300, bbox_inches="tight")

# for i in basin:
#     fig, ax = plt.subplots(figsize=(6,4))
#     ax.annotate(i, xy=(0.7, 0.1),  xycoords='axes fraction')
#     ax.axhline(0.45, ls='--', linewidth=3)
#     plt.xlim(0, 360)
#     plt.ylim(0, 0.65)
#     topo_aspe_plot(6, 9, i)
#     fig.savefig("print/basin/" + i + "_aspe.png", dpi=300, bbox_inches="tight")  