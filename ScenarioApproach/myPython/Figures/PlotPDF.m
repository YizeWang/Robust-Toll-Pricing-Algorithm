mu = 1000;
sigma = 100;
pd1 = makedist('Normal', 'mu', mu, 'sigma', sigma);
x1 = 800:1:1200;
y1 = pdf(pd1, x1);
plot(x1, y1)
hold on

lambda = 1000;
pd = makedist('Poisson','lambda',lambda);
x2 = 800:1:1200;
y2 = pdf(pd, x2);
plot(x2, y2)
hold on

lb = 800;
ub = 1200;
pd3 = makedist('Uniform', 'lower', lb, 'upper', ub);
x3 = 800:1:1200;
y3 = pdf(pd3, x3);
plot(x3, y3)

writematrix(y1, 'yGaussian.csv')
writematrix(y2, 'yPoisson.csv')
writematrix(y3, 'yUniform.csv')