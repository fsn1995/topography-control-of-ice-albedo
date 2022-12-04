

%% load data
% topodf = readtable("H:\AU\topography\basin\SW_annual.csv");
topodf = readtable("/data/shunan/data/topography/basin/SE_annual.csv");

% topodf.distance = topodf.dist / 1000;
topodf.iceclass = repmat("bare ice", length(topodf.albedo) , 1);
index = topodf.albedo < 0.45;
topodf.iceclass(index) = repmat("dark ice", sum(index) , 1);
topodf.distance = topodf.dist / 1000;
%% prepare input
% index = topodf.distance>=6.02642477064999;
% topodf = topodf(index, :);

slope = normalize(topodf.slope, 'range', [0 1]);
aspect = normalize(topodf.aspect, 'range', [0 1]);
elevation = normalize(topodf.elevation, 'range', [0 1]);

% %% pca analysis
% [coeff,score,latent,tsquared,explained,mu] = pca([elevation aspect slope]);
% figure; 
% biplot(coeff(:,1:2),'scores',score(:,1:2),'varlabels',{'elevation','aspect','slope'});
% figure;
% pareto(explained, {'pc1','pc2','pc3'}, 1)

%% split data 

% df = table(gpuArray(slope), gpuArray(aspect), gpuArray(elevation));
df = table(slope, aspect, elevation);
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
options = struct("Optimizer","asha", "UseParallel",true);
[Mdl,OptimizationResults] = fitcauto(trainData, trainLabel, "Learners","auto",...
    "HyperparameterOptimizationOptions",options);

mdlPred = string(predict(Mdl, testData));
mdlLoss = loss(Mdl, testData, testLabel);
fprintf("model loss rate is: %.4f \n", mdlLoss);
figure;
confusionchart(testLabel, mdlPred);

%% knn
% fprintf("knn \n")
% mdl = fitcknn(trainData, trainLabel,"OptimizeHyperparameters","auto");
% 
% mdlPred = string(predict(mdl, testData));
% mdlLoss = loss(mdl, testData, testLabel);
% fprintf("model loss rate is: %.4f \n", mdlLoss);
% figure;
% confusionchart(testLabel, mdlPred);
% title("cknn");
% 
% %% decision tree
% fprintf("tree \n")
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
% fprintf("Naïve Bayes \n")
% mdl = fitcnb(trainData, trainLabel, "OptimizeHyperparameters","auto");
% 
% mdlPred = string(predict(mdl, testData));
% mdlLoss = loss(mdl, testData, testLabel);
% fprintf("model loss rate is: %.4f \n", mdlLoss);
% figure;
% confusionchart(testLabel, mdlPred);
% title("Naïve Bayes");
% 
% %% neural network
% fprintf("neural network \n")
% mdl = fitcnet(trainData, trainLabel,"OptimizeHyperparameters","auto"); %"LayerSizes",[35 20]
% 
% mdlPred = string(predict(mdl, testData));
% mdlLoss = loss(mdl, testData, testLabel);
% fprintf("model loss rate is: %.4f \n", mdlLoss);
% figure;
% confusionchart(testLabel, mdlPred);
% title("neural network");
% 
% %% svm
% fprintf("svm \n")
% mdl = fitcsvm(trainData, trainLabel,"OptimizeHyperparameters","auto");
% 
% mdlPred = string(predict(mdl, testData));
% mdlLoss = loss(mdl, testData, testLabel);
% fprintf("model loss rate is: %.4f \n", mdlLoss);
% figure;
% confusionchart(testLabel, mdlPred);
% title("svm");
% 
% %% random forest
% fprintf("RF \n")
% t = templateTree('NumVariablesToSample','all',...
%     'PredictorSelection','interaction-curvature','Surrogate','on');
% 
% % mdl = fitcensemble(trainData, trainLabel, 'Method','Bag',...
% %     'NumLearningCycles',200, 'Learners',t);
% mdl = fitcensemble(trainData, trainLabel,"OptimizeHyperparameters", "auto");
% 
% mdlPred = string(predict(mdl, testData));
% mdlLoss = loss(mdl, testData, testLabel);
% fprintf("model loss rate is: %.4f \n", mdlLoss);
% figure;
% confusionchart(testLabel, mdlPred);
% title("rf");
% 
