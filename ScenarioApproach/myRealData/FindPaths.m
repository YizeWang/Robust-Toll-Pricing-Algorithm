function paths = FindPaths(G, start, target, factorPrune)

emptyPath = [];
matAdj = adjacency(G);
unusedNodes = ones(1, size(matAdj, 1));
shortestPath = numel(shortestpath(G, start, target));
maxLength = floor(shortestPath * factorPrune);
paths = FindPathsRec(matAdj, unusedNodes, emptyPath, start, target, maxLength);
   
end