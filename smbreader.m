%%
path_smb = "H:\AU\topography\HIRHAM5\DMI-HIRHAM5_GL2_ERAI_1980_2014_SMB_YM.nc";
% path_smb = "H:\AU\topography\HIRHAM5\DMI-HIRHAM5-MODIS-ERAI_1980_2017_SMB_MM.nc";

% ncdisp(path_smb);
% ncdisp(path_grid);

%% nc to tif
outpath='H:\AU\topography\HIRHAM5\tif\';% specify the output folder

df = ncread(path_smb,'smb');
lat = ncread(path_smb,'lat');
lon = ncread(path_smb,'lon');
% R = georasterref('RasterSize',[size(df,2), size(df,1)],'LongitudeLimits',...
%     [min(lon, [],'all'),max(lon, [],'all')],'LatitudeLimits',...
%     [min(lat, [],'all'),max(lat, [],'all')], 'CoordRefSysCode', 3411);
% R = georefcells([min(lat, [],'all'),max(lat, [],'all')], ...
%     [min(lon, [],'all'),max(lon, [],'all')], [size(df,2), size(df,1)],...
%     'ColumnsStartFrom','north', 'RowsStartFrom','west');
dateRef = datetime(1989,01,01,03,00,00);
time = ncread(path_smb,'time') + datenum(dateRef);
time = datetime(time,'ConvertFrom','datenum');
% geoshow(rot90(df(:,:,1,j), 1),R);
for j = 1 : length(time)
    [y,m,d] = ymd(time(j));
    outname= y;
    A = df(:,:, 1,j);
    A(A>0) = nan;
    figure;
    geoshow(lat,lon,A, 'DisplayType', 'surface');
    colorbar
    title(num2str(y))
%     writename = [outpath,num2str(outname),'.tif'];
%     print(writename,'-djpeg');
%     close(f);
%     writename = [outpath,num2str(outname*100 + m),'.jpg']; geotiffwrite(writename,flipud(rot90(df(:,:,1,j),1)),R);
%     geotiffwrite(writename,rot90(df(:,:,1,j), 1),R, "CoordRefSysCode", 3411);
end
