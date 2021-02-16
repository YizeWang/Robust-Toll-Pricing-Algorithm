function [Params] = ExtractParameters(G, ODs)

% extract dimensions
Params.M = G.numedges;       % number of edges
Params.N = G.numnodes;       % number of nodes
Params.K = size(ODs, 1);     % number of demands
Params.S = size(ODs, 2) - 2; % number of samples

% extract link attributes
Params.T = G.Edges.FreeFlowTime;
Params.B = G.Edges.B;

% l(x) = ax + c
Params.a = Params.T .* Params.B;
Params.c = Params.T;

end