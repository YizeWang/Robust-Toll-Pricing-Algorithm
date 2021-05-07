clc
close all
clear all

nameNetwork   = 'Pigou';
pathDataFolder = '..\myRealData\';

G = ParseTNTP(pathDataFolder, nameNetwork);
ODs = readmatrix([pathDataFolder nameNetwork '\' nameNetwork '_ODs.csv']);

X = G.Nodes.X;
Y = G.Nodes.Y;
labelEdges = {'f_2 = 0.0, l_2(f_2) = 1', 'f_1 = 1.0, l_1(f_1) = f_1'};
labelNodes = {'o', 'd'};
flowEdges = [0.000001, 1.0] * 2;

figure(1)
plot(G, 'XData', X, 'YData', Y, 'EdgeLabel', labelEdges, 'NodeLabel', labelNodes, 'LineWidth', flowEdges, 'EdgeFontSize', 10.5);
title("Pigou's Network (UE)", 'fontsize', 12)
set(gca, 'xtick', [])
set(gca, 'ytick', [])
print -depsc -painters -tiff -r300 pigou_network_ue.eps

X = G.Nodes.X;
Y = G.Nodes.Y;
labelEdges = {'f_2 = 0.5, l_2(f_2) = 1', 'f_1 = 0.5, l_1(f_1) = f_1'};
labelNodes = {'o', 'd'};
flowEdges = [0.5, 0.5] * 2;

figure(2)
plot(G, 'XData', X, 'YData', Y, 'EdgeLabel', labelEdges, 'NodeLabel', labelNodes, 'LineWidth', flowEdges, 'EdgeFontSize', 10.5);
title("Pigou's Network (SO)", 'fontsize', 12)
set(gca, 'xtick', [])
set(gca, 'ytick', [])
print -depsc -painters -tiff -r300 pigou_network_so.eps