/***
 * This is an experiment script that calculates the surface roughenss from DEM.
 * It is defined as the largest inter-cell difference of a central pixel and its 
 * surrounding cells (https://www.usna.edu/Users/oceano/pguth/md_help/html/roughness.html)
 * 
 * Shunan Feng (shunan.feng@envs.au.dk)
 */


var dataset = ee.Image('UMN/PGC/ArcticDEM/V3/2m_mosaic');
var greenlandmask = ee.Image('OSU/GIMP/2000_ICE_OCEAN_MASK')
                   .select('ice_mask').eq(1); // #'ice_mask', 'ocean_mask'  
var elevation = dataset.select('elevation').updateMask(greenlandmask);

var palettes = require('users/gena/packages:palettes');
var palette = palettes.cmocean.Thermal[7].reverse();

var imVis = {
  min: 0,
  max: 100.0,
  palette: palette,
};
var kernel = ee.Kernel.square({radius: 1});
var maxDiff = elevation.focalMax({kernel:kernel, iterations:1}).subtract(elevation);
var minDiff = elevation.subtract(elevation.focalMin({kernel:kernel, iterations:1}));

var roughness = ee.ImageCollection([maxDiff, minDiff]).max().rename('roughness');

Map.setCenter(-49.3, 67.029, 7);
Map.addLayer(roughness, imVis, 'roughness');