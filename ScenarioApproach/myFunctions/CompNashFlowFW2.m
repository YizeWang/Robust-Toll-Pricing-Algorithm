function [x, it, xs] = CompNashFlowFW2(G, ODs)

% extract dimensions
numEdge = G.numedges;
numDmnd = size(ODs, 1);
ops = optimoptions('linprog', 'Display', 'none');

% extract vector values
FFT = G.Edges.FreeFlowTime;
B   = G.Edges.B;
Pow = G.Edges.Power;
Cap = G.Edges.Capacity;

% compute system model
[A, b] = GetEqualityConstraints(G, ODs);

% compute free flow
fGrad = [zeros(numEdge, 1); repmat(FFT, numDmnd, 1)];
x = linprog(fGrad', [], [], A, b, zeros(numEdge*numDmnd+numEdge,1), [], ops);

% iteration settings
it = 0;
maxIteration = 1000;
tol = 1;
xDiffNormAvg = inf;
xs = [];

% iterate until convergence
while xDiffNormAvg > tol && it < maxIteration
    xs = [xs, x];
    xOld = x;
    t = FFT .* (1 + B .* (x(1:numEdge) ./ Cap) .^ Pow);
    fGrad = [zeros(numEdge, 1); repmat(t, numDmnd, 1)];
    s = linprog(fGrad', [], [], A, b, zeros(numEdge*numDmnd+numEdge,1), [], ops);
    step = 2 / (it + 2);
    x = x + step * (s - x);
    xDiffNormAvg = norm(x(1:numEdge) - xOld(1:numEdge)) / G.numedges;
    it = it + 1;
end

x = x(1:numEdge);

end