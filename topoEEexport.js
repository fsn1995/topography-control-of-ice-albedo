var randomPoints = ee.FeatureCollection("projects/ee-deeppurple/assets/topography/randomELA2000"),
    icemask = ee.FeatureCollection("projects/ee-deeppurple/assets/icePoly");


Export.table.toDrive({
    collection: icemask,
    description:'icePoly',
    fileFormat: 'SHP'
  });

Export.table.toDrive({
    collection: randomPoints,
    description:'randamSample',
    fileFormat: 'SHP'
  });