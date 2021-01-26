function [] = PlotNetwork(G)

% extract label data
X       = G.Nodes.X;
Y       = G.Nodes.Y;
indEdge = 1:G.numedges;
indNode = 1:G.numnodes;

% plot graph
plot(G, 'XData', X, 'YData', Y, 'EdgeLabel', indEdge, 'NodeLabel', indNode);
title('Network Topology')
xlabel('X')
ylabel('Y')

end