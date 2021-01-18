clc
clear all
close all

d = 1.0;
H = diag([0.5, 1.5, 2.0, 0.5]);
f = [4.0; 1.0; 1.0; 2.0];
Aeq = [1.0, 1.0, 1.0, 1.0];
beq = d;

x = sdpvar(4,1);
t = sdpvar(4,1);

OO = x'*H*x + f'*x;
CO = [t >= 0];

OI = 0.5*x'*H*x + (f+t)'*x;
CI = [Aeq*x == beq, x >= 0];

solvebilevel(CO,OO,CI,OI,x);

x = value(x);
t = value(t);
opt = value(OO);