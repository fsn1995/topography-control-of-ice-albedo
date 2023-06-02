// Generate random points in the given region, buffered by the scale of the given projection.
// When strict is
//   true: points will be at least 'scale' apart, with an average spacing of 2*scale.
//   false: points will be, on average, 'scale' apart, but with no minimum distance guarantee.
var pointsWithBuffer = function(proj, region, seed, strict) {
  // Construct a grid of random numbers with the appropriate sized pixels 
  // and randomly offset it, so subsequent runs don't sample from the exact same cells.
  var looseGrid = ee.Image.random(seed).multiply(1000000).int()

  // To ensure no points can be closer than the given distance we mask off 8 out of 9 grid cells.
  // leaving only those cells have an odd x and y coordinates.  
  // Cell coordinates are centered on the 1/2 pixel. The double not is to avoid float comparison issues.
  var mask = ee.Image.pixelCoordinates(proj)
      .expression('!((b("x") + 0.5) % 2 != 0 || (b("y") + 0.5) % 2 != 0)')
  var strictGrid = looseGrid.updateMask(mask)

  // Pick a grid based on the 'strict' option.
  var cells = ee.Image(ee.Algorithms.If(strict, strictGrid, looseGrid)).clip(region).reproject(proj)
  // Uncomment to visuaize cells.
  // Map.addLayer(cells.randomVisualizer())
  
  // Generate another random image and select the maximum random value 
  // in each grid cell as the sample point.
  var random = ee.Image.random(seed).multiply(1000000).int()
  var maximum = cells.addBands(random).reduceConnectedComponents(ee.Reducer.max())
  
  // Find all the points that are local maximums and convert to a FeatureCollection.
  var points = random.eq(maximum).selfMask()
  var samples = points.reduceToVectors({
    reducer: ee.Reducer.countEvery(),
    geometry: region,
    crs: proj.scale(1/16, 1/16),
    geometryType: 'centroid',
    maxPixels: 1e9,
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
var displayGrid = function(proj) {
  // Scale by 2 because we have 2 zero crossings when using round.
  var cells = ee.Image.pixelCoordinates(proj.scale(2,2))
  return cells.subtract(cells.round()).zeroCrossing().reduce('sum').selfMask()
}

// Get the contiguous United States as a region.
var conus = ee.FeatureCollection('USDOS/LSIB_SIMPLE/2017')
    .filter('country_na == "United States"')
    .geometry().dissolve().simplify(10000)

var grid1 = randomOffset(ee.Projection('EPSG:5070').atScale(50000), 72672)
var grid2 = randomOffset(ee.Projection('EPSG:5070').atScale(5000), 51263)

Map.addLayer(pointsWithBuffer(grid2, conus, 51263, true), {color: '#b22222'}, 'Strict')
// Note that all cells are displayed this way, but only the odd ones are used.
Map.addLayer(displayGrid(grid2).clip(conus), {palette: ['#92222244']}, 'Strict Grid')
print(pointsWithBuffer(grid2, conus, 51263, true).size(), " strict points, spaced ", grid2.nominalScale(), " meters apart.")

Map.addLayer(pointsWithBuffer(grid1, conus, 72672, false), {color: '#ffa500'}, 'Loose')
Map.addLayer(displayGrid(grid1).clip(conus), {palette: ['#bba50044']}, 'Loose Grid')

// Make the background map dark.
Map.setOptions('dark',{
  'dark': [
    { 'elementType': 'labels', 'stylers': [ { 'visibility': 'off' } ] },
    { 'elementType': 'geometry', 'stylers': [ { 'color': '#808080' } ] },
    { 'featureType': 'water',  'stylers': [ { 'color': '#404040' } ] }
  ]
})
