var greenlandmask = ee.Image('OSU/GIMP/2000_ICE_OCEAN_MASK')
                      .select('ice_mask').eq(1); //'ice_mask', 'ocean_mask'
// var greenlandmask = ee.Image('OSU/GIMP/2000_ICE_OCEAN_MASK')
//                       .select('ocean_mask').eq(1); //'ice_mask', 'ocean_mask'

// var aoi = /* color: #ffc82d */ee.Geometry.Polygon(
//   [[[-36.29516924635421, 83.70737243835941],
//     [-51.85180987135421, 82.75597137647488],
//     [-61.43188799635421, 81.99879137488564],
//     [-74.08813799635422, 78.10103528196419],
//     [-70.13305987135422, 75.65372336709613],
//     [-61.08032549635421, 75.71891096312955],
//     [-52.20337237135421, 60.9795530382023],
//     [-43.41430987135421, 58.59235996703347],
//     [-38.49243487135421, 64.70478286561182],
//     [-19.771731746354217, 69.72271161037442],
//     [-15.728762996354217, 76.0828635948066],
//     [-15.904544246354217, 79.45091003031243],
//     [-10.015872371354217, 81.62328742628017],
//     [-26.627200496354217, 83.43179828852398],
//     [-31.636966121354217, 83.7553561747887]]]); // whole greenland

// var aoi = /* color: #d63000 */ee.Geometry.Polygon(
//         [[[-75.35327725640606, 78.15797707936824],
//           [-58.137306661848434, 69.59945512283268],
//           [-51.82415036596651, 59.897134149764156],
//           [-42.233465551083604, 59.260337764670496],
//           [-61.95501079278244, 79.65995314962508]]]);   // western greenland
var aoi = ee.Geometry.Polygon(
         [[[-51.26670684036638, 71.10667904834996],
           [-50.613642172036386, 69.35172505065574],
           [-51.925886527866396, 67.4097894479071],
           [-51.20992413915373, 66.27518798747208],
           [-51.86713118464301, 66.04083709002118],
           [-51.68516540592766, 65.85920268639616],
           [-50.14610137161638, 63.77010325395928],
           [-44.45518340286638, 63.62039597689339],
           [-44.45518340286638, 71.06394313461017]]]); // dark zone connected ice
           

// Display AOI on the map.
Map.centerObject(aoi, 4);
Map.addLayer(aoi, {color: 'f8766d'}, 'AOI');
Map.setOptions('HYBRID');

var date_start = ee.Date.fromYMD(2009, 8, 16);
var date_end = ee.Date.fromYMD(2017, 3, 12);

/*
arctic dem strips
*/

var elevation = ee.ImageCollection('UMN/PGC/ArcticDEM/V3/2m')
                  .filterBounds(aoi)
                  .select('elevation');
var elevationVis = {
  min: -50.0,
  max: 1000.0,
  palette: ['0d13d8', '60e1ff', 'ffffff'],
};
// Map.addLayer(elevation, elevationVis, 'Elevation');


// Difference in days between start and finish
var diff = date_end.difference(date_start, 'day');

// Make a list of all dates
var dayNum = 1; // steps of day number
var range = ee.List.sequence(0, diff.subtract(1), dayNum).map(function(day){return date_start.advance(day,'day')});

// Function for iteration over the range of dates
var day_mosaicsArcticDEM = function(date, newlist) {
  // Cast
  date = ee.Date(date);
  newlist = ee.List(newlist);

  // Filter collection between date and the next day
  var filtered = elevation.filterDate(date, date.advance(dayNum,'day'));
  // Make the mosaic
  var image = ee.Image(
      filtered.mosaic().copyProperties(filtered.first()))
      .set({date: date.format('yyyy-MM-dd')})
      .set('system:time_start', filtered.first().get('system:time_start'));

  // Add the mosaic to a list only if the collection has images
  return ee.List(ee.Algorithms.If(filtered.size(), newlist.add(image), newlist));
};
var arcticDEMdayCol = ee.ImageCollection(ee.List(range.iterate(day_mosaicsArcticDEM, ee.List([]))));
Map.addLayer(arcticDEMdayCol, elevationVis, 'Elevation');