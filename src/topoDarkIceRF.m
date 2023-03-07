

%% load data
topodf = readtable("H:\AU\topography\basin\SW_annual.csv");
% topodf = readtable("/data/shunan/data/topography/basin/SE_annual.csv");
topodf.iceclass = repmat("bare ice", length(topodf.albedo) , 1);
index = topodf.albedo < 0.45;
topodf.iceclass(index) = repmat("dark ice", sum(index) , 1);
topodf.distance = topodf.dist / 1000;
%% prepare input

slope = normalize(topodf.slope, 'range', [0 1]);
aspect = normalize(topodf.aspect, 'range', [0 1]);
elevation = normalize(topodf.elevation, 'range', [0 1]);
distance = normalize(topodf.distance, 'range', [0 1]);
duration = normalize(topodf.duration, 'range', [0 1]);



%% split data 

% df = table(gpuArray(slope), gpuArray(aspect), gpuArray(elevation));
df = table(slope, aspect, elevation, distance, duration);

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
% SW 
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


impOOB = oobPermutedPredictorImportance(mdl);


f=figure;
set(f,'Position',[200 200 1200 300])

tilefig = tiledlayout(1, 4);
ax1 = nexttile;

b = bar(impOOB,'FaceColor','flat');
b.CData = [0 0.4470 0.7410
           0.8500 0.3250 0.0980
           0.9290 0.6940 0.1250
           0.4940 0.1840 0.5560
           0.3010 0.7450 0.9330];
title('a) SW')
% xlabel('Predictors')
ylabel('Importance')
h = gca;
h.XTickLabel = mdl.PredictorNames;
grid on

ax2=nexttile;
b = pie(ax2, impOOB);
ax2.Colormap = [0 0.4470 0.7410
               0.8500 0.3250 0.0980
               0.9290 0.6940 0.1250
               0.4940 0.1840 0.5560
               0.3010 0.7450 0.9330];
title(ax1, 'a) SW')

%% load data
topodf = readtable("H:\AU\topography\basin\SE_annual.csv");
% topodf = readtable("/data/shunan/data/topography/basin/SE_annual.csv");
topodf.iceclass = repmat("bare ice", length(topodf.albedo) , 1);
index = topodf.albedo < 0.45;
topodf.iceclass(index) = repmat("dark ice", sum(index) , 1);
topodf.distance = topodf.dist / 1000;
%% prepare input


slope = normalize(topodf.slope, 'range', [0 1]);
aspect = normalize(topodf.aspect, 'range', [0 1]);
elevation = normalize(topodf.elevation, 'range', [0 1]);
distance = normalize(topodf.distance, 'range', [0 1]);
duration = normalize(topodf.duration, 'range', [0 1]);



%% split data 

% df = table(gpuArray(slope), gpuArray(aspect), gpuArray(elevation));
df = table(slope, aspect, elevation, distance, duration);

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
% SW 
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


impOOB = oobPermutedPredictorImportance(mdl);



ax3 = nexttile;

b = bar(impOOB,'FaceColor','flat');
b.CData = [0 0.4470 0.7410
           0.8500 0.3250 0.0980
           0.9290 0.6940 0.1250
           0.4940 0.1840 0.5560
           0.3010 0.7450 0.9330];
title('c) SE')
ylabel('Importance')
h = gca;
h.XTickLabel = mdl.PredictorNames;
grid on


ax4=nexttile;
b = pie(ax4, impOOB);
ax4.Colormap = [0 0.4470 0.7410
               0.8500 0.3250 0.0980
               0.9290 0.6940 0.1250
               0.4940 0.1840 0.5560
               0.3010 0.7450 0.9330];
title('d) SE')
tilefig.TileSpacing = 'compact';
tilefig.Padding = 'compact';
fontsize(f, scale=1.2)
exportgraphics(tilefig, 'print/rfpredictor.pdf', 'Resolution',300);


