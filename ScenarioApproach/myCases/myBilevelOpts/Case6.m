clc
clear all
close all

N = 30;

d = 1.0;
H = diag([1.0, 2.0, 3.0, 1.0, 0.5, 0.5, 4.0, 2.0, 1.0, 0.0, zeros(1, 9)]);
f = [1.0; 1.0; 0.5; 3.0; 1.0; 4.0; 0.0; 0.5; 0.0; 1.0; zeros(9, 1)];
Aeq1 = eye(10);
Aeq2 = zeros(10, 9);
Aeq2(1, [1 2 3 4 5 9]) = -1.0;
Aeq2(2, [6 7 8]) = -1.0;
Aeq2(3, [1 2 3]) = -1.0;
Aeq2(4, [4 5 9]) = -1.0;
Aeq2(5, [1 2 7 8]) = -1.0;
Aeq2(6, [3 6 9]) = -1.0;
Aeq2(7, [9]) = -1.0; %#ok<*NBRAK> 
Aeq2(8, [1 5 7]) = -1.0;
Aeq2(9, [2 4 8]) = -1.0;
Aeq2(10, [2 3 4 6 8 9]) = -1.0;
Aeq3 = zeros(1, 10);
Aeq4 = ones(1, 9);
Aeq = [Aeq1, Aeq2; Aeq3, Aeq4];
beq = [zeros(10, 1); d];

mu = d;
sigma = 0.5;
uncertainty = 0.5;
pd = makedist('Normal', 'mu', mu, 'sigma', sigma);
tg = truncate(pd, mu-uncertainty, mu+uncertainty);
beqs = [zeros(10, N); random(tg, 1, N)];
taxable = [zeros(4, 1); 1; zeros(5, 1); zeros(9, 1)];

[optTolls, time] = ComputeOptTolls(H, f, Aeq, beqs, taxable);
[xSA, costSA] = ComputeNashFlow(optTolls, H, f, Aeq, beq, zeros(size(Aeq, 2)), []);