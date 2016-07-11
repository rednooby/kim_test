function y = threshold_matrix (x)

[row,col] = size(x);

for i=1:row
    for j=1:col
        if x(i,j) < 0
            x(i,j) = 0;
        else
            x(i,j) = 1;
        end
    end
end

y = x;

end
