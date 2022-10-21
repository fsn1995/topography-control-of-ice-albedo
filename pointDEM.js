var roi = ee.FeatureCollection("projects/ee-deeppurple/assets/icePoly");
var greenlandmask = ee.Image('OSU/GIMP/2000_ICE_OCEAN_MASK')
                   .select('ice_mask').eq(1); // #'ice_mask', 'ocean_mask'    

var elevation = ee.ImageCollection('UMN/PGC/ArcticDEM/V3/2m')
                  .select("elevation")
                  .filterBounds(roi);
var topoCol = elevation.map(function(img) {
  var topo = img.updateMask(greenlandmask);
  var demproduct = ee.Terrain.products(topo);
  return demproduct
});
var poi = ee.FeatureCollection("projects/ee-deeppurple/assets/topography/randomELA2000");       


// var pointElevation = ee.FeatureCollection(elevation.map(function (img) {
//   return img.sampleRegions({collection: poi, scale: 30, geometries: true})
// })).flatten()

// print(pointElevation.limit(50));


function bufferPoints(radius, bounds) {
  return function(pt) {
    pt = ee.Feature(pt);
    return bounds ? pt.buffer(radius).bounds() : pt.buffer(radius);
  };
}

function zonalStats(ic, fc, params) {
  // Initialize internal params dictionary.
  var _params = {
    reducer: ee.Reducer.mean(),
    scale: null,
    crs: null,
    bands: null,
    bandsRename: null,
    imgProps: null,
    imgPropsRename: null,
    datetimeName: 'datetime',
    datetimeFormat: 'YYYY-MM-dd HH:mm:ss'
  };

  // Replace initialized params with provided params.
  if (params) {
    for (var param in params) {
      _params[param] = params[param] || _params[param];
    }
  }

  // Set default parameters based on an image representative.
  var imgRep = ic.first();
  var nonSystemImgProps = ee.Feature(null)
    .copyProperties(imgRep).propertyNames();
  if (!_params.bands) _params.bands = imgRep.bandNames();
  if (!_params.bandsRename) _params.bandsRename = _params.bands;
  if (!_params.imgProps) _params.imgProps = nonSystemImgProps;
  if (!_params.imgPropsRename) _params.imgPropsRename = _params.imgProps;

  // Map the reduceRegions function over the image collection.
  var results = ic.map(function(img) {
    // Select bands (optionally rename), set a datetime & timestamp property.
    img = ee.Image(img.select(_params.bands, _params.bandsRename))
      .set(_params.datetimeName, img.date().format(_params.datetimeFormat))
      .set('timestamp', img.get('system:time_start'));

    // Define final image property dictionary to set in output features.
    var propsFrom = ee.List(_params.imgProps)
      .cat(ee.List([_params.datetimeName, 'timestamp']));
    var propsTo = ee.List(_params.imgPropsRename)
      .cat(ee.List([_params.datetimeName, 'timestamp']));
    var imgProps = img.toDictionary(propsFrom).rename(propsFrom, propsTo);

    // Subset points that intersect the given image.
    var fcSub = fc.filterBounds(img.geometry());

    // Reduce the image by regions.
    return img.reduceRegions({
      collection: fcSub,
      reducer: _params.reducer,
      scale: _params.scale,
      crs: _params.crs
    })
    // Add metadata to each feature.
    .map(function(f) {
      return f.set(imgProps);
    });
  }).flatten().filter(ee.Filter.notNull(_params.bandsRename));

  return results;
}

var ptsTopo = poi.map(bufferPoints(15, false));

// Define parameters for the zonalStats function.
var params = {
  crs: "EPSG:3411",
  scale:30
};

// Extract zonal statistics per point per image.
var ptsTopoStats = zonalStats(topoCol, ptsTopo, params);
print(ptsTopoStats.limit(10));

Export.table.toDrive({
  collection: ptsTopoStats,
  folder: 'gee',
  description: 'randomSampleDEM',
  fileFormat: 'CSV'
});