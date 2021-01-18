function [optTolls, h] = ComputeOptTolls(H, f, Aeq, beqs, taxable)

tStart = tic;

m = size(beqs, 1); % number of constraints
N = size(beqs, 2); % number of samples
n = size(Aeq, 2);  % number of paths and links

A = [Aeq; -Aeq; eye(n)];         % Ax <= b, Ax >= b, x >= 0
b = [beqs; -beqs; zeros(n, N)];  % Ax <= b, Ax >= b, x >= 0

h = sdpvar(1, 1);
x = sdpvar(n, N);
t = sdpvar(n, 1);
t(~taxable) = 0;

lambda = sdpvar(2*m+n, N);
slack = A*x - b;

KKT = [];
for k = 1:N
    KKT = [KKT, ...
           H*x(:,k)+f+t-A'*lambda(:,k) == 0, ...
           A*x(:,k) - b(:,k) >= 0, ...
           x(:,k)'*H*x(:,k) + f'*x(:,k) <= h, ...
           complements(lambda(:,k) >= 0, slack(:,k) >= 0)];
end
KKT = [KKT, lambda <= 100];

cons = [KKT, t >= 0];

ops = sdpsettings('solver', 'gurobi', 'verbose', 0);
optimize(cons, h, ops);

optTolls = value(t);
h = value(h);

time = toc(tStart);
fprintf('Elapsed Time: %.4fs\n', time);

end