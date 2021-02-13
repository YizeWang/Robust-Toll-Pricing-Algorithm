function [stepLength] = FindOptStep(G, x, y)

% extract dimensions
numEdge = G.numedges;

% extract vector values
FFT = G.Edges.FreeFlowTime;
B   = G.Edges.B;
Pow = G.Edges.Power;
Cap = G.Edges.Capacity;

% define symbolic step length variable
syms a
xNew = x + a * (y - x);

% construct symbolic objective function
num = B .* FFT;                                     % dim: numEdge x 1
den = Cap .^ Pow .* (Pow + 1);                      % dim: numEdge x 1
Z = FFT .* xNew + num ./den .* (xNew .^ (Pow + 1)); % dim: numEdge x 1
Z = sum(Z);                                         % dim:       1 x 1
Z = matlabFunction(Z);

% compute optimal step length
stepLength = fminbnd(Z, 0, 1);

end


