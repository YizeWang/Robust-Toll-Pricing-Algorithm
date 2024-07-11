function paths = FindPathsRec(Adj, nodes, currentPath, start, target, maxLen)

paths = {};
nodes(start) = 0;
currentPath = [currentPath, start];
childAdj = Adj(start, :) & nodes;
childList = find(childAdj);
childCount = numel(childList);

if childCount == 0 || start == target || numel(currentPath) > maxLen
  if start == target
     paths = [paths; currentPath];
  end
  return;
end

for idx = 1:childCount
  currentNode = childList(idx);
  newNodes = nodes;
  newNodes(currentNode) = 0;
  newPaths = FindPathsRec(Adj, newNodes, currentPath, currentNode, target, maxLen);
  paths = [paths; newPaths];
end
   
end