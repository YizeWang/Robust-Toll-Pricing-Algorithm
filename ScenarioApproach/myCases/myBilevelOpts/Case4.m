clc
clear all
close all

N = 100;
d = 1.0;
H = diag([0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 4.0]);
f = [0.0; 0.0; 0.0; 1.0; 1.0; 1.0; 1.5; 2.0];
%     p1 p2 p3 x1 x2 x3 x4 x5
Aeq = [1  1  1  0  0  0  0  0;
       1  0  0 -1  0  0  0  0;
       1  0  0  0 -1  0  0  0;
       1  1  0  0  0 -1  0  0;
       0  1  0  0  0  0 -1  0;
       0  0  1  0  0  0  0 -1];
beq = [d; zeros(5, 1)];

mu = d;
sigma = 0.5;
uncertainty = 0.5;
pd = makedist('Normal', 'mu', mu, 'sigma', sigma);
tg = truncate(pd, mu-uncertainty, mu+uncertainty);
beqs = [random(tg, 1, N); zeros(5, N)];
taxable = [0 0 0 1 1 1 1 1];

[optTolls] = ComputeOptTolls(H, f, Aeq, beqs, taxable);
[xSA, costSA] = ComputeNashFlow(optTolls, H, f, Aeq, beq, zeros(size(Aeq, 2)), []);

% [statSubSmp] = FindSubSmps(H, f, Aeq, beqs, taxable);