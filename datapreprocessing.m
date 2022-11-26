%% This script identifies the point data based on the drainage basin of GrIS.

%% read data
dfdem = readtable("H:\AU\randomPoints\dem.csv");
dfalbedo = readtable("H:\AU\randomPoints\albedo.csv");
basinpoly = readgeotable("basin\GrISBasinDissolved.shp");

dfdem.basin = repmat("basin", length(dfdem.id), 1);
%% dem points inside basins

coordinates = unique([dfdem.longitude, dfdem.longitude], "rows");

for i = 1:length(basinpoly.SUBREGION1)
    index = isinterior(basinpoly.Shape(i), mappointshape(coordinates(:,1), ...
        coordinates(:,2)));
    dfdem.basin(index) = basinpoly.SUBREGION1(i);
end
