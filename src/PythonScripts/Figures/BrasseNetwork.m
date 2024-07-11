clc
close all
clear all


nameNetwork   = 'Brasse';
pathDataFolder = '..\myRealData\';

G = ParseTNTP(pathDataFolder, nameNetwork);
ODs = readmatrix([pathDataFolder nameNetwork '\' nameNetwork '_ODs.csv']);

X = G.Nodes.X;
Y = G.Nodes.Y;
labelEdges = {'l_1(f_1)=10f_1', 'l_2(f_2)=f_2+50', 'l_3(f_3)=f_3+50', 'l_4(f_4)=f_4+10', 'l_5(f_5)=10f_5'};
labelNodes ={ 'o', 'd', 'a', 'b'};

figure()
plot(G, 'XData', X, 'YData', Y, 'EdgeLabel', labelEdges, 'NodeLabel', labelNodes, 'EdgeFontSize', 10.5);
set(gca, 'xtick', [])
set(gca, 'ytick', [])
