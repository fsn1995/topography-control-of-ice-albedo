/*
This is a script to generate random sampling points with buffer to avoid 
the inluence of spatial autocorrelation.

Shunan Feng (shunan.feng@envs.au.dk)
*/



/*
initialize random sampler
*/
var cellSize = 500, //size of the sample grid
    seed = 1, 
    projcrs = "EPSG:3411"; //in WGS 84 / EPSG Greenland Polar Stereographic

               
var arcticDEM = ee.Image('UMN/PGC/ArcticDEM/V3/2m_mosaic');

var elamask = arcticDEM.lte(2000);
var greenlandmask = ee.Image('OSU/GIMP/2000_ICE_OCEAN_MASK')
                   .select('ice_mask').eq(1); // #'ice_mask', 'ocean_mask'    
var arcticDEMgreenland = arcticDEM.updateMask(greenlandmask).updateMask(elamask);

var visPara = {min: 0,  max: 3000.0, palette: ['0d13d8', '60e1ff', 'ffffff']};
// # visPara = {'min': 0,  'max': 3000.0, 'palette': palette}

Map.addLayer(arcticDEMgreenland, visPara, 'Arctic DEM terrain');
// Map.setCenter(-41.0, 74.0, 3);

/*
Functions for random sampling with buffer by Noel Gorelick,
modifed to mask out by ELA.
ref:https://medium.com/google-earth/random-samples-with-buffering-6c8737384f8c
*/

// Generate random points in the given region, buffered by the scale of the given projection.
// When strict is
//   true: points will be at least 'scale' apart, with an average spacing of 2*scale.
//   false: points will be, on average, 'scale' apart, but with no minimum distance guarantee.
var pointsWithBuffer = function(proj, region, seed, strict, elamask) {
  // Construct a grid of random numbers with the appropriate sized pixels 
  // and randomly offset it, so subsequent runs don't sample from the exact same cells.
  var looseGrid = ee.Image.random(seed).multiply(1000000).int().updateMask(elamask);

  // To ensure no points can be closer than the given distance we mask off 8 out of 9 grid cells.
  // leaving only those cells have an odd x and y coordinates.  
  // Cell coordinates are centered on the 1/2 pixel. The double not is to avoid float comparison issues.
  var mask = ee.Image.pixelCoordinates(proj)
      .expression('!((b("x") + 0.5) % 2 != 0 || (b("y") + 0.5) % 2 != 0)');
  var strictGrid = looseGrid.updateMask(mask);

  // Pick a grid based on the 'strict' option.
  var cells = ee.Image(ee.Algorithms.If(strict, strictGrid, looseGrid)).clip(region).reproject(proj);
  // Uncomment to visuaize cells.
  // Map.addLayer(cells.randomVisualizer());
  
  // Generate another random image and select the maximum random value 
  // in each grid cell as the sample point.
  var random = ee.Image.random(seed).multiply(1000000).int();
  var maximum = cells.addBands(random).reduceConnectedComponents(ee.Reducer.max());
  
  // Find all the points that are local maximums and convert to a FeatureCollection.
  var points = random.eq(maximum).selfMask()
  var samples = points.reduceToVectors({
    reducer: ee.Reducer.countEvery(),
    geometry: region,
    crs: proj.scale(1/16, 1/16),
    geometryType: 'centroid',
    maxPixels: 1e13,
  })

  return samples
}

// Translates a projection by a random amount between 0 and 1 in projection units.
var randomOffset = function(projection, seed) {
  var values = ee.FeatureCollection([ee.Feature(null, null)])
    .randomColumn('x', seed)
    .randomColumn('y', seed)
    .first()
  return projection.translate(values.get("x"), values.get("y"))
}

// Display the pixel grid assocaited with a projection, as box outlines.
var displayGrid = function(proj, mask) {
  // Scale by 2 because we have 2 zero crossings when using round.
  var cells = ee.Image.pixelCoordinates(proj.scale(2,2))
  return cells.subtract(cells.round()).zeroCrossing().reduce('sum').selfMask().updateMask(mask)
}

/*
random sampling points with strict buffer
*/

var region = ee.FeatureCollection("projects/ee-deeppurple/assets/icePoly");

var grid = randomOffset(ee.Projection(projcrs).atScale(cellSize), seed);

// Map.addLayer(pointsWithBuffer(grid, region, seed, true, elamask), {color: '#b22222'}, 'Strict')
Map.addLayer(displayGrid(grid, elamask).clip(region), {palette: ['#92222244']}, 'Strict Grid');
// print(pointsWithBuffer(grid, region, seed, true, elamask).size(), " strict points, spaced ", grid.nominalScale(), " meters apart.")

// // Make the background map dark.
// Map.setOptions('dark',{
//   'dark': [
//     { 'elementType': 'labels', 'stylers': [ { 'visibility': 'off' } ] },
//     { 'elementType': 'geometry', 'stylers': [ { 'color': '#808080' } ] },
//     { 'featureType': 'water',  'stylers': [ { 'color': '#404040' } ] }
//   ]
// })


// Export an ee.FeatureCollection as an Earth Engine asset in case the sampling points size is too big.
Export.table.toAsset({
    collection: pointsWithBuffer(grid, region, seed, true, elamask),
    description:'randomELA2000',
    assetId: 'projects/ee-deeppurple/assets/randomELA2000',
  });


/*
Visualize the exported feature collection the the grid
*/

var poi = ee.FeatureCollection("projects/ee-deeppurple/assets/topography/randomELA2000");  
Map.addLayer(poi, {color: '#b22222'}, 'Strict Points')     
print(poi.size(), " strict points, spaced ", grid.nominalScale(), " meters apart.")
