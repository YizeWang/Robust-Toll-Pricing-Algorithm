function [G] = ParseGraph(pathData, nameNetwork, doPlot)

pathNetwork = [pathData, nameNetwork, 'Network.tntp'];
pathNodePos = [pathData, nameNetwork, 'Node.tntp'];

dataNetwork = tdfread(pathNetwork, '\t');
dataNode = tdfread(pathNodePos, '\t');

startPoints = dataNetwork.init_node;
endPoints = dataNetwork.term_node;
ODs = [startPoints, endPoints];
numLinks = numel(startPoints);
indLinks = (1:numLinks)';
a = dataNetwork.a;
b = dataNetwork.b;

X = dataNode.X;
Y = dataNode.Y;
nameNode = string(dataNode.Node);

nameVarsEdge = {'EndNodes', 'LinkIndex', 'a', 'b'};
nameVarsNode = {'Name', 'X', 'Y'};
NodeTable = table(nameNode, X, Y, 'VariableNames', nameVarsNode);
EdgeTable = table(ODs, indLinks, a, b, 'VariableNames', nameVarsEdge);
G = digraph(EdgeTable, NodeTable);

if doPlot
    figure('Name', nameNetwork);
    plot(G, 'XData', G.Nodes.X, 'YData', G.Nodes.Y, 'EdgeLabel', G.Edges.LinkIndex, 'NodeLabel', G.Nodes.Name);
    xlabel('X')
    ylabel('Y')
end

end