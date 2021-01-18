function [areSame] = AreTollsSame(tolls1, tolls2)

if ~isequal(size(tolls1), size(tolls2))
    areSame = false;
    return;
end

tol = 0.01;

diff = abs(tolls1-tolls2);
areSame = (sum(diff) < tol);

end