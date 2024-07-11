function [xOpt, tOpt, hOpt] = ComputeOptimalTolls1(G, ODs, Params)

% extract dimensions
M = Params.M; % number of edges
N = Params.N; % number of nodes
K = Params.K; % number of demands
S = Params.S; % number of samples

% variable dimensions
tDim = M;
hDim = 1;
xDim = M + M * K;
uDim = xDim;
lDim = M + N * K;

% decision variables
t    = sdpvar(tDim, 1); % tau
h    = sdpvar(hDim, 1); % h
xBig = sdpvar(xDim, S); % x
uBig = sdpvar(uDim, S); % mu
lBig = sdpvar(lDim, S); % lambda

% coefficients
T = Params.T;
B = Params.B;

a = Params.a;
c = Params.c;

Q = diag(a); % quadratic cost term
q = c;       % linear cost term

% define optimization problem
obj = h;
cons = [xBig >= 0, uBig >= 0, t >= 0];

% add constraints
for s = 1:S
    x = xBig(:, s);
    u = uBig(:, s);
    l = lBig(:, s);
    OD = [ODs(:, 1), ODs(:, 2), ODs(:, s+2)];
    xLink = x(1:M);
    
    [A, b] = GetEqualityConstraints(G, OD);
    
    cons = [cons, xLink'*Q*xLink+q'*xLink <= h];
    cons = [cons, [T+t+a.*xLink; zeros(M*K, 1)] - u + A'*l == 0];
    cons = [cons, A*x - b == 0];
    cons = [cons, x' * u == 0];
end

% solve optimization problem
options = sdpsettings('solver', 'gurobi', 'verbose', 1);
optimize(cons, obj, options);

% assign return values
tOpt = value(t);
hOpt = value(h);
xOpt = value(xBig);

end