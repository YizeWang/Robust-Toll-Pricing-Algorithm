function [cellSP] = CompCellSP(G, flowLink)

% extract dimensions
numNode = G.numnodes;

% extract vector values
FFT = G.Edges.FreeFlowTime;
B   = G.Edges.B;
Pow = G.Edges.Power;
Cap = G.Edges.Capacity;

% compute intermediate values
Base           = flowLink ./ Cap;
ExpTerm        = B .* (Base .^ Pow);
costLink       = FFT .* (1 + ExpTerm);
G.Edges.Weight = costLink;

% construct cellSP
% cellSP: row -> start, colunm -> end, entry -> node-based shortest path
t = 1:numNode;
cellSP = cell(numNode, numNode);
for s = 1:numNode
    cellSP(s, :) = shortestpathtree(G, s, t, 'OutputForm', 'cell')';
end

% covert node-based shortest paths into edge-based ones
for i = 1:numNode
    for j = 1:numNode        
        pathNodes    = cellSP{i, j};
        starts       = pathNodes(1:end-1);
        targets      = pathNodes(2:end);
        pathEdges    = findedge(G, starts, targets);
        cellSP{i, j} = pathEdges;
    end
end

end