var greenlandmask = ee.Image('OSU/GIMP/2000_ICE_OCEAN_MASK')
                   .select('ice_mask').eq(1); // #'ice_mask', 'ocean_mask'
var arcticDEM = ee.Image('UMN/PGC/ArcticDEM/V3/2m_mosaic');

var arcticDEMgreenland = arcticDEM.updateMask(greenlandmask);

var visPara = {min: 0,  max: 3000.0, palette: ['0d13d8', '60e1ff', 'ffffff']};
// # visPara = {'min': 0,  'max': 3000.0, 'palette': palette}

Map.addLayer(arcticDEMgreenland, visPara, 'Arctic DEM terrain');
Map.setCenter(-41.0, 74.0, 3);

var region = /* color: #ffc82d */ee.Geometry.Polygon(
    [[[-36.29516924635421, 83.70737243835941],
      [-51.85180987135421, 82.75597137647488],
      [-61.43188799635421, 81.99879137488564],
      [-74.08813799635422, 78.10103528196419],
      [-70.13305987135422, 75.65372336709613],
      [-61.08032549635421, 75.71891096312955],
      [-52.20337237135421, 60.9795530382023],
      [-43.41430987135421, 58.59235996703347],
      [-38.49243487135421, 64.70478286561182],
      [-19.771731746354217, 69.72271161037442],
      [-15.728762996354217, 76.0828635948066],
      [-15.904544246354217, 79.45091003031243],
      [-10.015872371354217, 81.62328742628017],
      [-26.627200496354217, 83.43179828852398],
      [-31.636966121354217, 83.7553561747887]]]); // whole greenland

var maskPoly = greenlandmask.reduceToVectors({geometry: region, scale: 1000}).filterMetadata("label","equals",1);
Map.addLayer(maskPoly,{color: 'yellow'}, 'ice mask');
//  https://gis.stackexchange.com/a/245276
// // An ee.Geometry to constrain the geographic bounds of random points.
// var region = ee.Geometry.Rectangle(
//     {coords: [-50.844727,  65.146115,  -39.243164,  70.859087], geodesic: false});

// Generate 50 random points with the region.
var randomPoints = ee.FeatureCollection.randomPoints(
    {region: maskPoly, points: 100, seed: 0, maxError: 1});
print('Random points from within the defined region', randomPoints);

// Map.addLayer(region, {color: 'yellow'}, 'Region');
Map.addLayer(randomPoints, {color: 'black'}, 'Random points');

// Export an ee.FeatureCollection as an Earth Engine asset.
Export.table.toAsset({
    collection: maskPoly,
    description:'icePoly',
    assetId: 'projects/ee-deeppurple/assets/icePoly',
  });

Export.table.toAsset({
    collection: randomPoints,
    description:'randamSample',
    assetId: 'projects/ee-deeppurple/assets/topography/randomPoints',
  });