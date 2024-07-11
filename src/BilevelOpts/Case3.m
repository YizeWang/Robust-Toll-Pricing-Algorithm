clc
clear all
close all

N = 100;
d = 1.0;
H = diag([0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0]);
f = [0.0; 0.0; 0.0; 0.0; 1.0; 1.0; 0.0; 0.0];
%       p1   p2   p3   x1   x2   x3   x4   x5
Aeq = [1.0  1.0  1.0  0.0  0.0  0.0  0.0  0.0;
       1.0  1.0  0.0 -1.0  0.0  0.0  0.0  0.0;
       0.0  0.0  1.0  0.0 -1.0  0.0  0.0  0.0;
       1.0  0.0  0.0  0.0  0.0 -1.0  0.0  0.0;
       0.0  1.0  1.0  0.0  0.0  0.0 -1.0  0.0;
       0.0  1.0  0.0  0.0  0.0  0.0  0.0 -1.0];
beq = [d; zeros(5, 1)];

mu = d;
sigma = 0.5;
uncertainty = 0.5;
pd = makedist('Normal', 'mu', mu, 'sigma', sigma);
tg = truncate(pd, mu-uncertainty, mu+uncertainty);
dSampled = random(tg, 1, N);
beqs = [dSampled; zeros(5, N)];
taxable = [0 0 0 1 1 1 1 1];

[optTolls] = ComputeOptTolls(H, f, Aeq, beqs, taxable);
[xSA, costSA] = ComputeNashFlow(optTolls, H, f, Aeq, beq, zeros(size(Aeq, 2)), []);