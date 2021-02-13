%% network construction
date = datetime('now');
date.Format = 'yyyyMMddHHmm';
nameDiary = ['./Diary/' char(date) '-Diary'];
diary(nameDiary);

nameNetwork1   = 'SimpleGeneralNetwork';
nameNetwork2   = 'SiouxFalls';
nameNetwork3   = 'Brasse';
pathDataFolder = '..\myRealData\';

nameNetwork = nameNetwork2;
G = ParseTNTP(pathDataFolder, nameNetwork);
ODs = readmatrix([pathDataFolder nameNetwork '\' nameNetwork '_ODs.csv']);
ODs(:, 3) = ODs(:, 3) / 1000;
ODs = ODs(1:100, :);
% ODs = ODs(1:30, :);
% PlotNetwork(G);

% extract dimensions
M = G.numedges;   % number of edges
N = G.numnodes;   % number of nodes
K = size(ODs, 1); % number of demands

% extract link attributes
T = G.Edges.FreeFlowTime;
B = G.Edges.B;

% l(x) = ax + c
a = T .* B;
c = T;

% Ax = b
[A, b] = GetEqualityConstraints(G, ODs);

% decision variable dimension
xDim = M + M * K; %     |  x   |
tDim = M;         % v = | tau  |
uDim = xDim;      %     |  mu  |
lDim = M + N * K; %     |lambda|
hDim = 1;         %     |  h   |
bDim = M + N * K;
ADim = [bDim, xDim];
vDim = xDim + tDim + uDim + lDim + hDim;

%% construct gurobi model
% decision variables
x  = sdpvar(xDim, 1); % x
t  = sdpvar(tDim, 1); % tau
u  = sdpvar(uDim, 1); % mu
l  = sdpvar(lDim, 1); % lambda
h  = sdpvar(hDim, 1); % h

% construct objective function
xLink = x(1:M);
Q = diag(a);
q = c;

% define optimization problem
O = h;
% O1 = xLink' * Q * xLink + q' * xLink;
% O2 = 0.5 * xLink' * Q * xLink + q' * xLink;
% O3 = xLink' * Q * xLink + q' * xLink;

% constraints
cons = [t >= 0, x >= 0, u >= 0];
cons = [cons, [(T+t) + T.*B.*xLink; zeros(M*K, 1)] - u + A'*l == 0];
cons = [cons, A*x - b == 0];
cons = [cons, x' * u == 0];
cons = [cons, xLink' * Q * xLink + q' * xLink <= h];

%% solve problem
options = sdpsettings('solver', 'gurobi', 'verbose', 1);

optimize(cons, O, options);
value(xLink' * Q * xLink + q' * xLink)
xLink = value(xLink);

% optimize(cons, O1, options);
% value(xLink' * Q * xLink + q' * xLink)
% xLink1 = value(xLink);

% optimize(cons, O2, options);
% value(xLink' * Q * xLink + q' * xLink)
% xLink2 = value(xLink);

% optimize(cons, O3, options);
% value(xLink' * Q * xLink + q' * xLink)
% xLink3 = value(xLink);

diary off