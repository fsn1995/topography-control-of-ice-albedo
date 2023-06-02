# %% [markdown]
# # 02 GEE Map Greenland_b
# This is a simple exerciese of mapping Greenland with Google Earth Engine.

# %%
import ee
from ee_plugin import Map

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# ee.Initialize()

# %% [markdown]
# ## Greenland: Arctic DEM

# %%
# Map = geemap.Map()
# Map # comment this line if in colab

# %% [markdown]
# ## Greenland: ArcticDEM terrain palette

# %%
greenlandmask = ee.Image('OSU/GIMP/2000_ICE_OCEAN_MASK') \
                   .select('ice_mask').eq(1); #'ice_mask', 'ocean_mask'
arcticDEM = ee.Image('UMN/PGC/ArcticDEM/V3/2m_mosaic')

arcticDEMgreenland = arcticDEM.updateMask(greenlandmask)

arcticDEMtopo = ee.Terrain.products(arcticDEMgreenland)

visPara = {'min': 0,  'max': 3000.0, 'palette': ['0d13d8', '60e1ff', 'ffffff']}
# visPara = {'min': 0,  'max': 3000.0, 'palette': palette}

Map.addLayer(arcticDEMgreenland, visPara, 'Arctic DEM')
slope_cmap = plt.cm.get_cmap('viridis')
Map.addLayer(arcticDEMtopo.select('slope'), {'min': 0, 'max': 20, 'palette': [mpl.colors.rgb2hex(slope_cmap(i))[1:] for i in range(slope_cmap.N)]}, 'Arctic DEM slope')
aspect_cmap = plt.cm.get_cmap('twilight')
Map.addLayer(arcticDEMtopo.select('aspect'), {'min': 0, 'max': 360, 'palette': [mpl.colors.rgb2hex(aspect_cmap(i))[1:] for i in range(aspect_cmap.N)]}, 'Arctic DEM aspect')
Map.setCenter(-41.0, 74.0, 3)
# Map.add_colorbar(visPara, label="Elevation (m)", discrete=False, orientation="vertical", layer_name="Arctic DEM terrain")

# %% [markdown]
# ## Greenland: ArcticDEM contour
# ref: https://twitter.com/jstnbraaten/status/1372958857266229252

# %%
greenlandmask = ee.Image('OSU/GIMP/2000_ICE_OCEAN_MASK') \
                   .select('ocean_mask').eq(0); #'ice_mask', 'ocean_mask'
arcticDEM = ee.Image('UMN/PGC/ArcticDEM/V3/2m_mosaic')

arcticDEMgreenland = arcticDEM.updateMask(greenlandmask)
Map.setCenter(-41.0, 74.0, 3)

mask = arcticDEMgreenland.gt(0)

elevZones = arcticDEMgreenland.expression(
  "(b('elevation') > 2500) ? 10" + \
  ": (b('elevation') > 2250) ? 9" + \
  ": (b('elevation') > 2000) ? 8" + \
  ": (b('elevation') > 1750) ? 7" + \
  ": (b('elevation') > 1500) ? 6" + \
  ": (b('elevation') > 1250) ? 5" + \
  ": (b('elevation') > 1000) ? 4" + \
  ": (b('elevation') > 750) ? 3" + \
  ": (b('elevation') > 500) ? 2" + \
  ": (b('elevation') > 250) ? 1" + \
  ": 0"
).mask(mask)


cmap = plt.cm.get_cmap("terrain", 12)
palette = [mpl.colors.rgb2hex(cmap(i))[1:] for i in range(cmap.N)]

visPara = {'min': 0,  'max': 3000.0, 'palette': palette}


# Make a height layer from the binned elevation.
height = elevZones.multiply(175)

# Cast shadows based on elevation bin height.
shadow = (ee.Terrain.hillShadow(
  height.updateMask(mask).unmask(0), 310, 70, 30, False).Not().selfMask()) \
  .visualize(**{'min': 1, 'max': 1, 'palette': '000', 'opacity': 0.9})

# Add a palette to the elevation bins.
elevZonesVis = elevZones.visualize(**{'min': 0, 'max': 10, 'palette': palette})
bg = ee.Image(0).visualize(**{'palette': 'FFF'})
paper = ee.Terrain.hillshade(
  ee.Image.random(0).reproject('EPSG:4326', None, 500).multiply(1000)) \
  .visualize(**{'palette': ['A0A0A0', 'fff'], 'opacity': 0.07})


composite = bg.blend(elevZonesVis).blend(shadow).blend(paper)

Map.setCenter(-41.0, 74.0, 3)
Map.addLayer(composite, name='ArcticDEM contour')
# Map.add_colorbar(visPara, label="Elevation (m)", discrete=True, orientation="vertical", layer_name="ArcticDEM contour")


#%% make colorbar
# ref https://matplotlib.org/stable/tutorials/colors/colorbar_only.html
# import matplotlib.pyplot as plt
# import matplotlib as mpl
# from matplotlib.colors import ListedColormap#, LinearSegmentedColormap


# fig, ax = plt.subplots(figsize=(6, 1))
# fig.subplots_adjust(bottom=0.5)
fig, ax = plt.subplots(figsize=(0.5, 6))
# fig.subplots_adjust(bottom=0.5)

# blue_fluorite = ['#291b32', '#2a1b34', '#2b1b34', '#2d1c36', '#2f1c38', '#301c39', '#301d3a', '#321d3b', '#331d3d', '#351d3f', '#351e40', '#371e41', '#381e43', '#3a1e45', '#3b1f45', '#3c1f46', '#3e1f48', '#3f1f4a', '#401f4c', '#42204d', '#43204e', '#44204f', '#462051', '#472052', '#482054', '#4a2056', '#4a2157', '#4c2158', '#4e215a', '#4f215b', '#50215d', '#52215e', '#532160', '#552162', '#552263', '#562264', '#582265', '#592267', '#5b2268', '#5c226b', '#5e226c', '#5f226e', '#60226f', '#622271', '#632272', '#642274', '#662276', '#672277', '#692278', '#6a227a', '#6c227b', '#6e227d', '#6e237e', '#6f247f', '#702480', '#712581', '#722681', '#732683', '#742783', '#752884', '#762985', '#772987', '#792a87', '#792b88', '#7a2c89', '#7b2c8a', '#7c2d8a', '#7d2d8c', '#7e2e8d', '#7f2f8d', '#80308e', '#813190', '#823191', '#833292', '#843292', '#863393', '#863494', '#873595', '#893596', '#8a3697', '#8b3798', '#8b3899', '#8c389a', '#8e399b', '#8e3a9c', '#8f3b9c', '#8f3d9d', '#8f3e9e', '#903f9e', '#90419e', '#90439f', '#9044a0', '#9046a0', '#9047a1', '#9049a1', '#914aa2', '#914ca2', '#914ca3', '#914ea3', '#9150a4', '#9151a5', '#9153a5', '#9154a6', '#9156a6', '#9157a7', '#9258a7', '#9259a8', '#925aa8', '#925ba9', '#925da9', '#925faa', '#9260ab', '#9260ab', '#9263ac', '#9264ac', '#9265ad', '#9266ae', '#9268ae', '#9269ae', '#926aaf', '#926bb0', '#926cb0', '#926eb1', '#926fb1', '#9270b2', '#9271b2', '#9273b3', '#9274b3', '#9275b4', '#9277b5', '#9277b5', '#9278b6', '#927ab6', '#927bb7', '#927cb7', '#927eb8', '#927fb8', '#9280b9', '#9281ba', '#9282ba', '#9284bb', '#9285bb', '#9285bc', '#9187bc', '#9188bd', '#918abd', '#918bbe', '#918cbf', '#918dbf', '#918ec0', '#918fc0', '#9191c1', '#9092c2', '#9094c2', '#9094c2', '#9095c3', '#9096c3', '#8f99c4', '#8f9ac5', '#8f9ac5', '#8f9bc6', '#8f9cc6', '#8f9dc7', '#8e9fc8', '#8ea0c8', '#8ea2c9', '#8ea3c9', '#8da5ca', '#8da5ca', '#8da6cb', '#8da7cb', '#8ca9cc', '#8caacc', '#8caccd', '#8bacce', '#8badce', '#8baecf', '#8ab0d0', '#8ab2d0', '#8ab2d1', '#8ab4d1', '#89b4d1', '#89b5d2', '#89b7d2', '#88b8d3', '#88bad4', '#87bad4', '#87bbd5', '#86bdd6', '#86bed6', '#86c0d7', '#85c0d7', '#85c1d8', '#84c3d8', '#84c4d9', '#83c5d9', '#83c6da', '#82c8da', '#82c8db', '#81cadc', '#81cbdc', '#80ccdd', '#81cddd', '#84cfdd', '#85cfdd', '#87d0dd', '#8ad0de', '#8dd1de', '#8fd2de', '#90d2de', '#92d4de', '#95d5de', '#97d5de', '#98d6de', '#9bd7de', '#9dd7df', '#a0d8df', '#a1d9df', '#a2dadf', '#a5dadf', '#a7dbdf', '#aadcdf', '#abdddf', '#acdde0', '#afdfe0', '#b1dfe0', '#b3e0e0', '#b4e1e0', '#b7e2e0', '#bae2e1', '#bae3e1', '#bee3e2', '#c0e4e3', '#c1e5e3', '#c4e6e3', '#c6e6e4', '#c8e7e4', '#cbe7e5', '#cde8e5', '#cee9e6', '#d2e9e7', '#d3eae7', '#d5eae7', '#d8ebe8', '#d9ece8', '#dcece9', '#deedea', '#dfeeea', '#e2eeea', '#e5efeb', '#e6f0eb', '#e9f0ec', '#ebf1ed', '#ecf2ed', '#eff3ee', '#f1f3ee']
# cmp = ListedColormap(blue_fluorite)

# norm = mpl.colors.Normalize(vmin=0, vmax=3500)
bounds = np.linspace(0, 2500, 11)
norm = mpl.colors.BoundaryNorm(bounds, cmap.N, extend='max')


cb1 = mpl.colorbar.ColorbarBase(ax, cmap=cmap,
                                norm=norm,
                                orientation='vertical')
cb1.set_label('Elevation (m a.s.l)')
# fig.show()
fig.savefig("colorbar.svg", dpi=300, transparent=True)
# %%
