[![DOI](https://zenodo.org/badge/502836537.svg)](https://zenodo.org/badge/latestdoi/502836537)
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Ffsn1995%2Ftopography-control-of-ice-albedo&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)
# Analysis of geo-topographic and phenological controls on the spatial distribution of dark ice on the Greenland Ice Sheet

This is part of a research paper. The code is available for reproducibility.
A web map is made to visualize the topographical dataset. The web map is available at https://storymaps.arcgis.com/stories/f52a6a97b8eb4c76af56d848dd5330bb.
A brief description of the code is provided below.

Feng, S., Cook, J. M., Naegeli, K., Anesio, A. M., Benning, L. G., & Tranter, M. (2024). The Impact of Bare Ice Duration and Geo‐Topographical Factors on the Darkening of the Greenland Ice Sheet. Geophysical Research Letters, 51(1), e2023GL104894. [https://doi.org/10.1029/2023GL104894]{https://doi.org/10.1029/2023GL104894}

## Albedo and ArcticDEM data extraction
- [src/randomSampleBuffer.js](src/randomSampleBuffer.js)
- [src/randomSampleDEMAlbedo.py](src\randomSampleDEMAlbedo.py)

Both the harmonized satellite albedo and the ArcticDEM were extracted ([src/randomSampleBuffer.js](src/randomSampleBuffer.js)) using the generated random sampling points ([src/randomSampleDEMAlbedo.py](src\randomSampleDEMAlbedo.py)
). 

Functions for random sampling with buffer were made by Noel Gorelick and were modfied to adapt to our methodology. It runs in the earth engine code editor. Ref: https://medium.com/google-earth/random-samples-with-buffering-6c8737384f8c
The extraction of albedo and ArcticDEM are using EE's python api via geemap. 
## Data analysis
- [src/dataPrep.py](src/dataPrep.py)
- [src/topoanalysis.py](src/topoanalysis.py)
- [src/topoStats.py](src/topoStats.py)
- [src/topoDarkIceRF.m](src/topoDarkIceRF.m)

The extracted albedo and dem data were further analyzed in this section. More detail can be found in the manuscript. 
The shapefiles of the generated random sampling points, contour lines, and the basins are all available in the [src/shp](src/shp) folder.

## Citation
```
@article{Feng2024a,
   author = {Shunan Feng and Joseph Mitchell Cook and Kathrin Naegeli and Alexandre Magno Anesio and Liane G. Benning and Martyn Tranter},
   doi = {10.1029/2023GL104894},
   issn = {0094-8276},
   issue = {1},
   journal = {Geophysical Research Letters},
   month = {1},
   pages = {e2023GL104894},
   title = {The Impact of Bare Ice Duration and Geo‐Topographical Factors on the Darkening of the Greenland Ice Sheet},
   volume = {51},
   year = {2024},
}
```

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