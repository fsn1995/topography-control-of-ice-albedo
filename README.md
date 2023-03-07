[Reserved for doi badge]
[Reserved for view count badge]
# Analysis of topographic controls on the spatial distribution of dark ice on the Greenland Ice Sheet

This is part of a manuscript that will be under review (hopefully).

## Albedo and ArcticDEM data extraction
- [src/randomSampleBuffer.js](src/randomSampleBuffer.js)
- [src/randomSampleDEMAlbedo.py](src\randomSampleDEMAlbedo.py)

Both the harmonized satellite albedo and the ArcticDEM were extracted using the generated random sampling points. 

Functions for random sampling with buffer were made by Noel Gorelick and were modfied to adapt to our methodology. Ref: https://medium.com/google-earth/random-samples-with-buffering-6c8737384f8c

## Data analysis
- [src/dataPrep.py](src/dataPrep.py)
- [src/topoanalysis.py](src/topoanalysis.py)
- [src/topoStats.py](src/topoStats.py)
- [src/topoDarkIceRF.m](src/topoDarkIceRF.m)

The extracted albedo and dem data were further analyzed in this section.

```
|   README.md
|   LICENSE
\---src
    |   dataPrep.py
    |   exportAlbedoImage.py      
    |   pointDEM.js
    |   randomSampleBuffer.js     
    |   randomSampleDEMAlbedo.py  
    |   randomSampleGEE.js        
    |   randomSampleTemplate.js   
    |   topoanalysis.py
    |   topoDarkIceML.m
    |   topoDarkIceRF.m
    |   topoEEexport.js
    |   topoML.m
    |   topoStats.py
    |
    +---shp
    |       contour.cpg
    |       contour.dbf
    |       contour.prj
    |       contour.sbn
    |       contour.sbx
    |       contour.shp
    |       contour.shp.xml
    |       contour.shx
    |       GrISBasinDissolved.cpg
    |       GrISBasinDissolved.dbf
    |       GrISBasinDissolved.prj
    |       GrISBasinDissolved.sbn
    |       GrISBasinDissolved.sbx
    |       GrISBasinDissolved.shp
    |       GrISBasinDissolved.shp.xml
    |       GrISBasinDissolved.shx
    |       randamSample.cpg
    |       randamSample.dbf
    |       randamSample.fix
    |       randamSample.prj
    |       randamSample.shp
    |       randamSample.shp.xml
    |       randamSample.shx
    |
    \---stat
            Sbasin_stat.csv
            stats.xlsx
```