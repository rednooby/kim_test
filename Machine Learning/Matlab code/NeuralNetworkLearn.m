
function Network = NeuralNetworkLearn(Layers,learnRate,errFunChgLmt,weightChgLmt,maxRound,trainInput,trainDesiredOut,testInput,testDesiredOutput)

[inputRow,inputCol] = size(trainInput);
[outputRow,outputCol] = size(trainDesiredOut);

% each input vector has a corresponding desired output
if inputRow ~= outputRow 
    error('backprop:invalidTrainingAndDesired', ...
          'The number of input vectors and desired ouput do not match');
end

% equivalent dimensions
if inputCol ~= Layers(1) || outputCol ~= Layers(end)
    e = sprintf('Dimensions of input (%d) does not match input layer (%d)',inputCol,Layers(1));
    error('backprop:invalidLayerSize', e);
elseif outputCol ~= Layers(end)
    e = sprintf('Dimensions of output (%d) does not match output layer (%d)',outputCol,Layers(end));
    error('backprop:invalidLayerSize', e);    
end


% initialization
layerLen = length(Layers);
Network.layerLen = layerLen;

Network.trainErrFun = [];
Network.trainErrFunRate = [];
Network.testErrFun = [];
Network.testErrFunRate = [];

% randomize the weight matrices
Network.w = cell(layerLen-1,1);
for i=1:layerLen-2        
    Network.w{i} = 1 - 2.*rand(Layers(i+1),Layers(i)+1);
end
%Network.w{end} = 1 - 2.*rand(Layers(end),Layers(end-1)+1);
Network.w{layerLen-1} = 1 - 2.*rand(Layers(layerLen),Layers(layerLen-1)+1);


% initialize stopping conditions
errFunChg = realmax;  % assuming the intial weight matrices are bad
weightChg = realmax;
round = 0;
min_trainErrFun = realmax;
while errFunChg > errFunChgLmt && weightChg > weightChgLmt && round < maxRound
    
    m = inputRow; %  #examples
    
    % forwardProp
    
    out = cell(layerLen,1);
    out{1} = [repmat(-1,1,m); trainInput'];
    for i=1:layerLen-1
        z{i+1} = Network.w{i} * out{i}; % z = w*o
        out{i+1} = [repmat(-1,1,m); sigmoid(z{i+1})]; % out = 1/(1+e^(-z))
    end
    output = out{layerLen}(2:end,:);
    
    err = mean((output - trainDesiredOut').^2, 1); % E(w)
    last_errFun = mean(err);
    
    
    
    % backPropagation
    
    delta = cell(layerLen,1);
    % delta_output = out*(1-out)*(output-desiredOutput)
    delta{layerLen} = deriv_sigmoid(output) .*  deriv_squared_error(output, trainDesiredOut');
    % calculate delta_input
    for i = layerLen:-1:3
        x = out{i-1}(2:end,:);
        d = delta{i};
        delta{i-1} = deriv_sigmoid(x) .* (Network.w{i-1}(:,2:end)' * d);
    end
    for i = layerLen:-1:2
        x = out{i-1};
        d = delta{i};
        OutDelta{i} = d*x';
    end
    
    
    % update
    
    weightChg = 0;
    for i=layerLen:-1:2
        change = learnRate/m * OutDelta{i};
        Network.w{i-1} = Network.w{i-1} - change;
        weightChg = max(weightChg, max(abs(change(:))));
    end
    round = round + 1;
    
    
    % forwardProp, check error(train)
    
    out{1} = [repmat(-1,1,m); trainInput'];
    for i=1:layerLen-1
        z{i+1} = Network.w{i} * out{i};
        out{i+1} = [repmat(-1,1,m); sigmoid(z{i+1})];
    end
    output = out{layerLen}(2:end,:);
    
    trainErr = mean((output - trainDesiredOut').^2, 1);
    trainErrFun = mean(trainErr);
    trainErrFunRate = 1-mean(all(trainDesiredOut' == (output == repmat(max(output),size(output,1),1)),1));
    
    Network.trainErrFun = [Network.trainErrFun trainErrFun];
    Network.trainErrFunRate = [Network.trainErrFunRate trainErrFunRate];
    
    errFunChg = abs(trainErrFun - last_errFun);
    
    
    % forwardProp, error(test)
    
    out{1} = [repmat(-1,1,size(testInput,1)); testInput'];
    for i=1:layerLen-1
        z{i+1} = Network.w{i} * out{i};
        out{i+1} = [repmat(-1,1,size(testInput,1)); sigmoid(z{i+1})];
    end
    output = out{layerLen}(2:end,:);
    
    testErr = mean((output - testDesiredOutput').^2, 1);
    testErrFun = mean(testErr);
    testErrFunRate = 1-mean(all(testDesiredOutput' == (output == repmat(max(output),size(output,1),1)),1));
    
    Network.testErrFun = [Network.testErrFun testErrFun];
    Network.testErrFunRate = [Network.testErrFunRate testErrFunRate];
    
    
    % lowest training error
    
    if(trainErrFun < min_trainErrFun)
        min_trainErrFun = trainErrFun;
        min_trainErrFunRate = trainErrFunRate;
        min_testErrFun = testErrFun;
        min_testErrFunRate = testErrFunRate;
        
        Network.bestNetwork = Network;
        Network.bestNetwork.bestTrainErrFun = min_trainErrFun;
        Network.bestNetwork.bestTrainErrFunRate = min_trainErrFunRate;
        Network.bestNetwork.bestTestErrFun = min_testErrFun;
        Network.bestNetwork.bestTestErrFunRate = min_testErrFunRate;
    end
end