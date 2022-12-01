

%% load data
topodf = readtable("H:\AU\topography\basin\SW.csv");
index = topodf.month > 6 & topodf.month < 9;
topodf = topodf(index, :);

topodf.iceclass = repmat("bare ice", length(topodf.albedo) , 1);
index = topodf.albedo < 0.45;
topodf.iceclass(index) = repmat("dark ice", sum(index) , 1);
iceclass = topodf.iceclass;
%% prepare input
slope = normalize(topodf.slope, 'range', [-1 1]);
aspect = normalize(topodf.aspect, 'range', [-1 1]);
elevation = normalize(topodf.elevation, 'range', [-1 1]);

% df = table(slope, aspect, elevation);
df = [slope, aspect, elevation];

[trainId,valId,testId] = dividerand(length(topodf.iceclass), 0.6, 0.2, 0.2);


% Use Indices to parition the matrix  
trainData = df(trainId,:);
trainLabel = topodf.iceclass(trainId);
testData = df(testId,:);
testLabel = topodf.iceclass(testId);
valiData = df(valId, :);
valiLabel = topodf.iceclass(valId);

%% training model



options = trainingOptions("adam", ... 
    ValidationData={valiData, valiLabel}, ...
    Plots="training-progress", ...
    Verbose=0);

numFeatures = 3;
numClasses = 2;

filterSize = 3;
numFilters = 32;

layers = [
    sequenceInputLayer(numFeatures)
    lstmLayer(128)
    fullyConnectedLayer(numFeatures)
    regressionLayer];

mynet = trainNetwork(trainData, trainLabel, layers, options);
