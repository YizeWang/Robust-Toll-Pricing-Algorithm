function [] = PlotNetwork(G)

% extract label data
X       = G.Nodes.X;
Y       = G.Nodes.Y;
indEdge = G.Edges.IndexLink;
indNode = G.Nodes.IndexNode;

% plot graph
plot(G, 'XData', X, 'YData', Y, 'EdgeLabel', indEdge, 'NodeLabel', indNode);
title('Network Topology')
xlabel('X')
ylabel('Y')

end