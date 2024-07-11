function [flowAllHave] = CompAllHaveFlow(G, cellSP, ODs)

% extract dimensions
numEdge = G.numedges;
numDmnd = size(ODs, 1);

% initialize flowAllHave vector
flowAllHave = zeros(numEdge, 1);

% impose all demand on shortest path
for indOD = 1:numDmnd
    s = ODs(indOD, 1);
    t = ODs(indOD, 2);
    d = ODs(indOD, 3);
    
    path = cellSP{s, t};
    flowAllHave(path) = flowAllHave(path) + d;
end

end