#%%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import vaex as vx
import numpy as np
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
    df["logslope"] = np.log(df.slope)
    df = vx.from_pandas(df)
    df.viz.heatmap('slope', 'albedo', what=np.log(vx.stat.count()), show=True,
                    vmin=0, vmax=5, xlabel="slope (" + u'\N{DEGREE SIGN}' + ')', ylabel="albedo")

def topo_aspe_plot(basin):
    df = pd.read_csv("/data/shunan/data/topography/basin/" + basin + "_annual.csv")
    df = vx.from_pandas(df)
    df.viz.heatmap('aspect', 'albedo', what=np.log(vx.stat.count()), show=True,
                    vmin=0, vmax=2.5, xlabel="aspect (" + u'\N{DEGREE SIGN}' + ')', ylabel="albedo")                    

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