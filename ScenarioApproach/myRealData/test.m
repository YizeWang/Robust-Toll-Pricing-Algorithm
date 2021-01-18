%% load data
clc
close all
clear all

pathData = 'Data/';
nameNetwork = 'ComplexGeneralNetwork';
G = ParseGraph(pathData, nameNetwork);

%% generate samples
d = 1;
N = 20;
mu = d;
sigma = 0.5;
uncertainty = 0.5;
pd = makedist('Normal', 'mu', mu, 'sigma', sigma);
tg = truncate(pd, mu-uncertainty, mu+uncertainty);
smpl = random(tg, 1, N);
taxable = [zeros(4, 1); 1; zeros(5, 1); zeros(9, 1)];
beq = [d; zeros(10, 1)];

%% construct system model
factorPrune = 10;
ODs = [1, 6, smpl]; % source-target-demand
[Aeq, beqs, H, f] = ModelSystem(G, ODs, factorPrune);

[optTolls] = ComputeOptTolls(H, f, Aeq, beqs, taxable);
[xSA, costSA] = ComputeNashFlow(optTolls, H, f, Aeq, beq, zeros(size(Aeq, 2)), []);