function y = deriv_sigmoid (x)

y = sigmoid (x) .* (1 - sigmoid (x));

end