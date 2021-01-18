%% load data
clc
close all
clear all

pathData = 'Data/';
nameNetwork = 'SimpleGeneralNetwork';
G = ParseGraph(pathData, nameNetwork);

%% construct system model
numLinks = G.numedges;
indLast = numLinks;
ODs = [1, 4, 1.0]; % source-target-demand
numODs = size(ODs, 1);
allPaths = {};
allPathsEdges = {};
indPaths = {};
factorPrune = 1.5;

for i = 1:numODs
    start = ODs(i, 1);
    target = ODs(i, 2);
    demand = ODs(i, 3);
    paths = FindPaths(G, start, target, factorPrune);
    allPaths = [allPaths; paths];
    indLastNew = indLast + numel(paths);
    indPaths = [indPaths; (indLast+1):indLastNew];
    indLast = indLastNew;
end

numPaths = numel(allPaths);
numXAndP = numLinks + numPaths;

A = sparse(numODs+numLinks, numXAndP);
b = sparse(numODs+numLinks, 1);
b(1:numODs) = ODs(:, 3);
A(numODs+1:end, 1:numLinks) = -eye(numLinks);

% | A11 | A12 |   | x |   | d |
% |-----+-----| * |---| = |---|
% | A21 | A22 |   | p |   | 0 |

for i = 1:numODs
    A(i, indPaths{i}) = 1;
end

for k = 1:numel(allPaths)
    pathEdges = PathNode2PathEdge(G, allPaths{k});
    allPathsEdges = [allPathsEdges; pathEdges];
    A(numODs+pathEdges, numLinks+k) = 1;
end