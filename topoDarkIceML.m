

%% load data
topodf = readtable("H:\AU\topography\basin\SW_annual.csv");
% topodf = readtable("/data/shunan/data/topography/basin/SE_annual.csv");
topodf.iceclass = repmat("bare ice", length(topodf.albedo) , 1);
index = topodf.albedo < 0.45;
topodf.iceclass(index) = repmat("dark ice", sum(index) , 1);
topodf.distance = topodf.dist / 1000;
%% prepare input
index = topodf.distance<9.57041446875;
topodf = topodf(index, :);

slope = normalize(topodf.slope, 'range', [0 1]);
aspect = normalize(topodf.aspect, 'range', [0 1]);
elevation = normalize(topodf.elevation, 'range', [0 1]);
% distance = normalize(topodf.distance, 'range', [0 1]);
% duration = normalize(topodf.duration, 'range', [0 1]);

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
% SW 0.2945 0.3006
t = templateTree("Reproducible", true, "Surrogate", "on", "MinLeafSize", 30);
mdl = fitcensemble(trainData, trainLabel,"Method", "Bag",...
     "Learners", t, "NumLearningCycles", 28);

% %SE 0.2668  0.2716 
% t = templateTree("Reproducible", true, "Surrogate", "on", "MinLeafSize", 24);
% mdl = fitcensemble(trainData, trainLabel,"Method", "Bag",...
%      "Learners", t, "NumLearningCycles", 59);

mdlPred = string(predict(mdl, testData));
mdlLoss = loss(mdl, testData, testLabel);
fprintf("model loss rate is: %.4f \n", mdlLoss);
f1 = figure;
confusionchart(testLabel, mdlPred);
set(f1,'Position',[10 10 350 300])
fontsize(gcf,scale=1.2)
% exportgraphics(f1, 'print/SWconfusion.png', 'Resolution',300);

impOOB = oobPermutedPredictorImportance(mdl);
f2 = figure;
b = bar(impOOB,'FaceColor','flat');
% b.CData = [0 0.4470 0.7410
%            0.8500 0.3250 0.0980
%            0.9290 0.6940 0.1250
%            0.4940 0.1840 0.5560
%            0.3010 0.7450 0.9330];
% title('Unbiased Predictor Importance Estimates')
% xlabel('Predictors')
ylabel('Importance')
h = gca;
h.XTickLabel = mdl.PredictorNames;
grid on
fontsize(gcf,scale=1.2)
% exportgraphics(f2, 'print/SWimportance.png', 'Resolution',300);

f3 = figure;
ax = gca();
b = pie(ax, impOOB);
% ax.Colormap = [0 0.4470 0.7410
%                0.8500 0.3250 0.0980
%                0.9290 0.6940 0.1250
%                0.4940 0.1840 0.5560
%                0.3010 0.7450 0.9330];
set(f3,'Position',[10 10 350 300])
fontsize(gcf,scale=1.2)
% exportgraphics(f3, 'print/SWpie.png', 'Resolution',300);
