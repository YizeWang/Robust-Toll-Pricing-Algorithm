%% network construction
clc
clear all
close all

nameNetwork1   = 'SimpleGeneralNetwork';
nameNetwork2   = 'SiouxFalls';
nameNetwork3   = 'Brasse';
pathDataFolder = '..\myRealData\';

nameNetwork = nameNetwork3;
G = ParseTNTP(pathDataFolder, nameNetwork);
PlotNetwork(G);

ODs = [1, 2, 6.0];

%% store data
FFT = G.Edges.FreeFlowTime;
B   = G.Edges.B;
Pow = G.Edges.Power;
Cap = G.Edges.Capacity;

%% system model
A = [1  0 -1 -1  0;
     0  1  0  1 -1;
     1  1  0  0  0;
     0  0  1  0  1];
b = [0  0  6  6]';
x = sdpvar(5, 1);

%% compute nash equilibrium
xInt = FFT .* x .* (1 + B .* x .^ Pow ./ (Pow + 1) ./ Cap .^ Pow);
ONE = sum(xInt);
consNE = [x >= 0, A*x == b];

ops = sdpsettings('verbose', 0);
optimize(consNE, ONE, ops);

xNE = value(x);
costNE = sum(xNE .* FFT .* (1 + B .* xNE .^ Pow ./ Cap .^ Pow));

%% compute optimal solution
xCost = x .* FFT .* (1 + B .* x .^ Pow ./ Cap .^ Pow);
OOpt = sum(xCost);
consOpt = [x >= 0, A*x == b];

ops = sdpsettings('verbose', 0);
optimize(consOpt, OOpt, ops);

xOpt = value(x);
costOpt = sum(xOpt .* FFT .* (1 + B .* xOpt .^ Pow ./ Cap .^ Pow));

%% branch and bound manual test
M = 10000; % big M
t = sdpvar(5, 1);
u = sdpvar(5, 1);
lambda = sdpvar(4, 1);
delta = sdpvar(5, 1);

fGrad = FFT + t + FFT .* B .* ((x ./ Cap) .^ Pow);
cons = [fGrad - u + A'*lambda == 0];
cons = [cons, A*x - b == 0];
cons = [cons, x >= 0, x <= M*delta];
cons = [cons, u >= 0, u <= M*(1-delta)];
cons = [cons, delta >= 0, delta <= 1];
cons = [cons, t >= 0];

xCost = x .* FFT .* (1 + B .* x .^ Pow ./ Cap .^ Pow);
O = sum(xCost);

ops = sdpsettings('verbose', 1);
optimize(cons, O, ops);

