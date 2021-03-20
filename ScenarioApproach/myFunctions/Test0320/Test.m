clc
clear all
close all

H = readmatrix('Hs.csv');
gamma = readmatrix('gammas.csv');
time = readmatrix('times.csv');
toll = readmatrix('tolls.csv');

costNash = 7465921.462217;
costOpt = 7199354.776482;

figure(1)
x1 = 0:68;
hold on
plot(x1, H, 'LineWidth', 1)
plot(x1, repmat(costNash, 1, 69), 'LineWidth', 0.5, 'LineStyle', '--')
plot(x1, repmat(costOpt, 1, 69), 'LineWidth', 0.5, 'LineStyle', '--')
axis([0 70 7.15e6 7.6e6]);
legend('Objective', 'Nash Cost', 'Optimal Cost')
ylabel('Cost')
xlabel('Iteration')
title('Cost - Iteration')

figure(2)
x2 = 1:68;
plot(x2, gamma, 'LineWidth', 1);
ylabel('Step Size')
xlabel('Iteration')
title('Step Size - Iteration')
legend('\gamma = 0.001 / Iteration')

figure(3)
x3 = 1:69;
plot(x3, toll, 'LineWidth', 0.5);
xlabel('Iteration')
ylabel('Toll')
title('Toll - Iteration')