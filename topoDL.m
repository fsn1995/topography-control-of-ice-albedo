

%% load data
topodf = readtable("H:\AU\randomPoints\basin\SW.csv");
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

df = table(slope, aspect, elevation);

[trainId,valId,testId] = dividerand(length(topodf.iceclass), 0.6, 0.2, 0.2);


% Use Indices to parition the matrix  
trainData = df(trainId,:);
trainLabel = topodf.iceclass(trainId);
testData = df(testId,:);
testLabel = topodf.iceclass(testId);
valiData = df(valId, :);
valiLabel = topodf.iceclass(valId);

%% training model

miniBatchSize = 27;

options = trainingOptions("adam", ...
    MiniBatchSize=miniBatchSize, ...
    MaxEpochs=15, ...
    SequencePaddingDirection="left", ...
    ValidationData={valiData, valiLabel}, ...
    Plots="training-progress", ...
    Verbose=0);

filterSize = 3;
numFilters = 32;

layers = [ ...
    sequenceInputLayer(3)
    convolution1dLayer(filterSize,numFilters,Padding="causal")
    reluLayer
    layerNormalizationLayer
    convolution1dLayer(filterSize,2*numFilters,Padding="causal")
    reluLayer
    layerNormalizationLayer
    globalAveragePooling1dLayer
    fullyConnectedLayer(2)
    softmaxLayer
    classificationLayer];

mynet = trainNetwork(trainData, trainLabel, layers, options);
