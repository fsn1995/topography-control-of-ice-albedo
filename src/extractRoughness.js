var roi = ee.FeatureCollection("projects/ee-deeppurple/assets/icePoly");
var greenlandmask = ee.Image('OSU/GIMP/2000_ICE_OCEAN_MASK')
                   .select('ice_mask').eq(1); // #'ice_mask', 'ocean_mask'    

var elevation = ee.ImageCollection('UMN/PGC/ArcticDEM/V3/2m')
                  .select("elevation")
                //   .filterDate("2015-07-01", "2015-07-15")
                  .filterBounds(roi);
// var topoCol = elevation.map(function(img) {
//   var topo = img.updateMask(greenlandmask);
//   var demproduct = ee.Terrain.products(topo);
//   return demproduct
// });
var poi = ee.FeatureCollection("projects/ee-deeppurple/assets/topography/randomELA2000");       

function calculate_surface_roughness(img) {
    var kernel = ee.Kernel.square({radius: 1});
    var maxDiff = img.focalMax({kernel:kernel, iterations:1}).subtract(img);
    var minDiff = img.subtract(img.focalMin({kernel:kernel, iterations:1}));
    var roughness = ee.ImageCollection([maxDiff, minDiff]).max().rename('roughness');
    return img.addBands(roughness).copyProperties(img, img.propertyNames());
}

var topo_roughness = elevation.map(calculate_surface_roughness);
var dataset = topo_roughness.select("roughness").toBands();
  
var poiTopo = poi.map(function(feature) {
  return feature.set(dataset.reduceRegion({
    reducer: ee.Reducer.mean(),
    scale: 30,
    tileScale:16,
    // crs: "EPSG:3411",
    geometry: feature.geometry()
  }));
});

Export.table.toDrive({
  collection: poiTopo,
  folder: "gee",
  description:'SurfaceRoughness',
  fileFormat: 'CSV'
});

