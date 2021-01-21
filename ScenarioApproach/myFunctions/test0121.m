clc
clear all
close all

pathDataFolder = '..\myRealData\TransportationNetworks\';
name1 = 'SimpleGeneralNetwork';
name2 = 'SiouxFalls';

nameNetwork = name2;
G = ParseTNTP(pathDataFolder, nameNetwork);
% PlotNetwork(G);

ODs = [2, 13, 20000;
       5, 18, 10000];
[A, b] = GetEqualityConstraints(G, ODs);

[xNash, costNash, costLink] = ComputeNashFlow(G, A, b, ODs);