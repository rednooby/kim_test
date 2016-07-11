
% 1. transformed data

load 'dataset1.dat'
load 'testnormal.dat'
train_data_tran = dataset1;
test_data_tran = testnormal;

trainDataTran = train_data_tran(:,1:(end-1));
trainClassTran_temp = train_data_tran(:,end);
m = size(trainDataTran, 1);
trainClassTran = ( repmat ( 0:1 , m , 1 ) == repmat ( trainClassTran_temp , 1 , 2 ) ) ;
testDataTran = test_data_tran(:,1:(end-1));
testClassTran_temp = test_data_tran(:,end);
m = size(testDataTran, 1);
testClassTran = ( repmat ( 0:1 , m , 1 ) == repmat ( testClassTran_temp , 1 , 2 ) ) ;


Layers = [2000 100 2];
errFunChgLmt = 1e-6;
weightChgLmt = 1e-4;
maxRound = 200;
learnRate = 21;

NetworkTran = NeuralNetworkLearn(Layers,learnRate,errFunChgLmt,weightChgLmt,maxRound,trainDataTran,trainClassTran,testDataTran,testClassTran);

bestErrTran = [NetworkTran.bestNetwork.bestTrainErrFun NetworkTran.bestNetwork.bestTestErrFun NetworkTran.bestNetwork.bestTrainErrFunRate NetworkTran.bestNetwork.bestTestErrFunRate];
fprintf('Transformed Data - best values\n');
fprintf('training error function   test error function   training misclassification error rate    test misclassification error rate\n');
disp(bestErrTran);


figure;
train = plot(NetworkTran.trainErrFun, 'r');
hold on;
test = plot(NetworkTran.testErrFun, 'b');
hold off;
legend([train test],{'training error function', 'test error function'});
xlabel('rounds');
title('Transformed data');

figure;
train = plot(NetworkTran.trainErrFunRate, 'r');
hold on;
test = plot(NetworkTran.testErrFunRate, 'b');
hold off;
legend([train test],{'training misclassification error rate', 'test misclassification error rate'});
xlabel('rounds');
title('Transformed data');



% 2. trial data

load 'trial1.dat'
trial_data_tran = trial1;
trialDataTran = trial_data_tran(:,1:(end-1));
trialClassTran_temp = trial_data_tran(:,end);
m = size(trialDataTran, 1);
trialClassTran = ( repmat ( 0:1 , m , 1 ) == repmat ( trialClassTran_temp , 1 , 2 ) ) ;

classifiedClassTran = ApplyNeuralNetwork(NetworkTran.bestNetwork, trialDataTran);
fprintf('Transformed trial data\n');
fprintf('desired output\n');
disp(trialClassTran);
fprintf('classified output\n');
disp(classifiedClassTran);

