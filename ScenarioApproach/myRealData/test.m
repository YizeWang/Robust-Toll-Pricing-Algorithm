%% load data
clc
close all
clear all

pathData = 'Data/';
nameNetwork = 'SiouxFalls';
G = ParseGraph(pathData, nameNetwork);

%% construct system model
factorPrune = 2;
ODs = [2, 13, 1]; % source-target-demand
[Aeq, beqs, H, f] = ModelSystem(G, ODs, factorPrune);
beq = [1; zeros(size(Aeq, 1)-1, 1)];