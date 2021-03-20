clc
close all
clear all

% nameNetwork = 'Massachusetts';
nameNetwork = 'SiouxFalls';
% nameNetwork = 'Brasse';

nameCSV = ['resMat' nameNetwork '.csv'];

csv = readmatrix(nameCSV);

scaleFactor = csv(1, :);
Nash = csv(2, :);
Opt = csv(3, :);
Toll1 = csv(4, :);
Toll2 = csv(5,: );

POA  = Nash  ./ Opt;
POA1 = Toll1 ./ Opt;
POA2 = Toll2 ./ Opt;
Ones = ones(numel(scaleFactor), 1);

plot(scaleFactor, POA, scaleFactor, POA1, scaleFactor, POA2, scaleFactor, Ones, 'LineWidth', 1)
xlabel('Scale Factor')
ylabel('PoA')
nameTitle = ['PoA of Different Tolls (' nameNetwork ')'];
title(nameTitle)
legend('No Toll', 'Toll (Ref: Nash)', 'Toll (Ref: Opt)', 'Baseline')