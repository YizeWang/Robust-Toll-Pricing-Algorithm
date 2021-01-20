%% load data
clc
close all
clear all

doPlot = false;
pathData = 'myRealData/';
nameNetwork = 'SiouxFalls';
G = ParseGraph(pathData, nameNetwork, doPlot);

%% construct system model
factorPrune = 2;
ODs = [2, 13, 1, 1.1]; % source-target-demand
[Aeq, beqs, H, f] = ModelSystem(G, ODs, factorPrune);
taxable = false(76, 1);
taxable(30) = true;
CompOptTollGreedy(H, f, Aeq, beqs, taxable);