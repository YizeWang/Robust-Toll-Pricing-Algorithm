function [A, b, H, f] = ModelSystem(G, ODs, factorPrune)

numLinks = G.numedges;
numODs = size(ODs, 1);
indLast = numLinks;
numSmpl = size(ODs, 2) - 2;

allPaths = {};
indPaths = {};

for i = 1:numODs
    start = ODs(i, 1);
    target = ODs(i, 2);
    paths = FindPaths(G, start, target, factorPrune);
    allPaths = [allPaths; paths];
    indLastNew = indLast + numel(paths);
    indPaths = [indPaths; (indLast+1):indLastNew];
    indLast = indLastNew;
end

numPaths = numel(allPaths);
numXAndP = numLinks + numPaths;

A = sparse(numODs+numLinks, numXAndP);
b = sparse(numODs+numLinks, numSmpl);
b(1:numODs, :) = ODs(:, 3:end);
A(numODs+1:end, 1:numLinks) = -eye(numLinks); % A21

% |  0  | A12 |   | x |   | d |
% |-----+-----| * |---| = |---|
% | A21 | A22 |   | p |   | 0 |

for i = 1:numODs
    A(i, indPaths{i}) = 1; % A12
end

for k = 1:numel(allPaths)
    pathEdges = PathNode2PathEdge(G, allPaths{k});
    A(numODs+pathEdges, numLinks+k) = 1; % A22
end

edgeTable = sortrows(G.Edges, {'LinkIndex'}, {'ascend'});
H = sparse(numXAndP, numXAndP);
f = sparse(numXAndP, 1);
H(1:numLinks, 1:numLinks) = diag(edgeTable.a);
f(1:numLinks, 1) = edgeTable.b;

end
