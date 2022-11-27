%% read and plot shapefile
% basinpoly = readgeotable("basin\GrISBasinDissolved.shp");
% figure;
% h = geoplot(basinpoly);

%% SW
topodf = readtable("H:\AU\randomPoints\basin\SW.csv");
index = topodf.month > 6 & topodf.month < 9;
topodf = topodf(index, :);

topodf.iceclass = repmat("bare ice", length(topodf.albedo) , 1);
index = topodf.albedo < 0.45;
topodf.iceclass(index) = repmat("dark ice", sum(index) , 1);
% topodf.timestamp = datetime(topodf.time_x, 'ConvertFrom','epochtime',...
%     'TicksPerSecond',1e3,'Format','dd-MMM-yyyy HH:mm:ss.SSS');
slope = normalize(topodf.slope, 'range', [-1 1]);
aspect = normalize(topodf.aspect, 'range', [-1 1]);
elevation = normalize(topodf.elevation, 'range', [-1 1]);

% pca
[coeff,score,latent,tsquared,explained,mu] = pca([elevation aspect slope]);
figure;
pareto(explained,{'pc1','pc2','pc3'}, 1);
xlabel('Principal Component');
ylabel('Variance Explained (%)');

figure;
biplot(coeff(:,1:2),'scores',score(:,1:2),'varlabels',{'elevation','slope','aspect'});

figure;
gscatter(score(:, 1), score(:, 2), topodf.iceclass);

%% CE
topodf = readtable("H:\AU\randomPoints\basin\SE.csv");
index = topodf.month > 6 & topodf.month < 9;
topodf = topodf(index, :);

topodf.iceclass = repmat("bare ice", length(topodf.albedo) , 1);
index = topodf.albedo < 0.45;
topodf.iceclass(index) = repmat("dark ice", sum(index) , 1);
% topodf.timestamp = datetime(topodf.time_x, 'ConvertFrom','epochtime',...
%     'TicksPerSecond',1e3,'Format','dd-MMM-yyyy HH:mm:ss.SSS');
slope = normalize(topodf.slope, 'range', [-1 1]);
aspect = normalize(topodf.aspect, 'range', [-1 1]);
elevation = normalize(topodf.elevation, 'range', [-1 1]);

% pca
[coeff,score,latent,tsquared,explained,mu] = pca([elevation aspect slope]);
figure;
pareto(explained,{'pc1','pc2','pc3'}, 1);
xlabel('Principal Component');
ylabel('Variance Explained (%)');

figure;
biplot(coeff(:,1:2),'scores',score(:,1:2),'varlabels',{'elevation','slope','aspect'});

figure;
gscatter(score(:, 1), score(:, 2), topodf.iceclass);