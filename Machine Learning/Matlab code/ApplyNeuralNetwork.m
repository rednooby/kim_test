function output = ApplyNeuralNetwork(Network, data)

    out = cell(Network.layerLen,1);
    out{1} = [repmat(-1,1,size(data,1)); data'];
    for i=2:Network.layerLen
        out{i} = Network.w{i-1} * out{i-1};
        out{i} = threshold_matrix(out{i});
        out{i} = [repmat(-1,1,size(data,1)); out{i}];
    end
    output = out{Network.layerLen}(2:end,:);
    output = output';
end