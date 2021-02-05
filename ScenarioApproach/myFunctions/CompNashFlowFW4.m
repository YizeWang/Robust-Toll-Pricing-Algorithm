function [x, it, xs] = CompNashFlowFW(G, ODs)

% set termination condition
it = 0;
maxIteration = 1000;
tol = 1;
xDiffNormAvg = inf;
xs = [];

% initialize Frank-Wolfe Algorithm
cellSP = CompCellSP(G, zeros(G.numedges, 1));
x = CompAllHaveFlow(G, cellSP, ODs);

% iterate until convergence
while xDiffNormAvg > tol && it < maxIteration
    xs = [xs, x];
    xOld = x;
    cellSP = CompCellSP(G, x);
    y = CompAllHaveFlow(G, cellSP, ODs);
    stepLength = FindOptStep(G, x, y);
    x = x + stepLength * (y - x);
    
    xDiffNormAvg = norm(x - xOld) / G.numedges;
    it = it + 1;
end

end