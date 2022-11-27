

%% load data
topodf = readtable("H:\AU\randomPoints\basin\SW.csv");
index = topodf.month > 6 & topodf.month < 9;
topodf = topodf(index, :);

topodf.iceclass = repmat("bare ice", length(topodf.albedo) , 1);
index = topodf.albedo < 0.45;
topodf.iceclass(index) = repmat("dark ice", sum(index) , 1);

%% prepare input
slope = normalize(topodf.slope, 'range', [-1 1]);
aspect = normalize(topodf.aspect, 'range', [-1 1]);
elevation = normalize(topodf.elevation, 'range', [-1 1]);
% slope = gpuArray(topodf.slope);
% aspect = gpuArray(topodf.aspect);
% elevation = gpuArray(topodf.elevation);
df = table(gpuArray(slope), gpuArray(aspect), gpuArray(elevation));
% [coeff,score,latent,tsquared,explained,mu] = pca([elevation aspect slope]);
% df = table(score(:,1), score(:,2));

cvpt = cvpartition(topodf.iceclass, "HoldOut", 0.3);

% Extract indices for training and test 
trainId = training(cvpt);
testId = test(cvpt);

% Use Indices to parition the matrix  
trainData = df(trainId,:);
trainLabel = topodf.iceclass(trainId);
testData = df(testId,:);
testLabel = topodf.iceclass(testId);


%% training model
options = struct("Optimizer","asha");
[Mdl,OptimizationResults] = fitcauto(trainData, trainLabel, "Learners","auto",...
    "HyperparameterOptimizationOptions",options);

mdlPred = string(predict(Mdl, testData));
mdlLoss = loss(Mdl, testData, testLabel);
fprintf("model loss rate is: %.4f \n", mdlLoss);
figure;
confusionchart(testLabel, mdlPred);

% %% knn
% mdl = fitcknn(trainData, trainLabel, "NumNeighbors", 5);
% 
% mdlPred = string(predict(mdl, testData));
% mdlLoss = loss(mdl, testData, testLabel);
% fprintf("model loss rate is: %.4f \n", mdlLoss);
% figure;
% confusionchart(testLabel, mdlPred);
% title("cknn");
% 
% %% decision tree
% mdl = fitctree(trainData, trainLabel, 'OptimizeHyperparameters','auto');
% 
% mdlPred = string(predict(mdl, testData));
% mdlLoss = loss(mdl, testData, testLabel);
% fprintf("model loss rate is: %.4f \n", mdlLoss);
% figure;
% confusionchart(testLabel, mdlPred);
% title("tree");
% 
% %% Naïve Bayes
% mdl = fitcnb(trainData, trainLabel);
% 
% mdlPred = string(predict(mdl, testData));
% mdlLoss = loss(mdl, testData, testLabel);
% fprintf("model loss rate is: %.4f \n", mdlLoss);
% figure;
% confusionchart(testLabel, mdlPred);
% title("Naïve Bayes");
% 
% %% neural network
% mdl = fitcnet(trainData, trainLabel,"LayerSizes",[35 20]);
% 
% mdlPred = string(predict(mdl, testData));
% mdlLoss = loss(mdl, testData, testLabel);
% fprintf("model loss rate is: %.4f \n", mdlLoss);
% figure;
% confusionchart(testLabel, mdlPred);
% title("neural network");
% 
% %% svm
% mdl = fitcsvm(trainData, trainLabel);
% 
% mdlPred = string(predict(mdl, testData));
% mdlLoss = loss(mdl, testData, testLabel);
% fprintf("model loss rate is: %.4f \n", mdlLoss);
% figure;
% confusionchart(testLabel, mdlPred);
% title("svm");
% 
% %% random forest
% t = templateTree('NumVariablesToSample','all',...
%     'PredictorSelection','interaction-curvature','Surrogate','on');
% 
% mdl = fitcensemble(trainData, trainLabel, 'Method','Bag',...
%     'NumLearningCycles',200, 'Learners',t);
% 
% mdlPred = string(predict(mdl, testData));
% mdlLoss = loss(mdl, testData, testLabel);
% fprintf("model loss rate is: %.4f \n", mdlLoss);
% figure;
% confusionchart(testLabel, mdlPred);
% title("rf");
