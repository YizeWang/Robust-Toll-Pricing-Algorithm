clc
clear all
close all

nameNetwork1   = 'SimpleGeneralNetwork';
nameNetwork2   = 'SiouxFalls';
pathDataFolder = '..\myRealData\TransportationNetworks\';

nameNetwork = nameNetwork2;
G = ParseTNTP(pathDataFolder, nameNetwork);
PlotNetwork(G);

ODs = [1, 4, 1.0];

x = zeros(G.numedges, 1);
cellSP = CompCellSP(G, x);
flowAllHave = CompAllHaveFlow(G, cellSP, ODs);