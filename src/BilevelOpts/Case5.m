clc
clear all
close all

N = 100;
d = 1.0;
H = diag([0.5, 1.5, 2.0, 0.5]);
f = [4.0; 1.0; 1.0; 2.0];
Aeq = [1.0, 1.0, 1.0, 1.0];
beq = [d];

mu = d;
sigma = 0.5;
uncertainty = 0.5;
pd = makedist('Normal', 'mu', mu, 'sigma', sigma);
tg = truncate(pd, mu-uncertainty, mu+uncertainty);
beqs = random(tg, 1, N);
taxable = [0 1 1 0];

[optTolls] = ComputeOptTolls(H, f, Aeq, beqs, taxable);
[xSA, costSA] = ComputeNashFlow(optTolls, H, f, Aeq, beq, zeros(size(Aeq, 2)), []);

[statSubSmp] = FindSubSmps(H, f, Aeq, beqs, taxable);