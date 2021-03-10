clc
close all
clear all

nameNetwork = 'Massachusetts';
% nameNetwork = 'SiouxFalls';
nameCSV = ['resMat' nameNetwork '.csv'];

% csv = readmatrix(nameCSV);

csv = [0.7000000000, 0.9000000000, 1.2000000000, 1.5000000000;
       18820.515160, 25036.437964, 35174.850360, 46908.841894;
       18379.512167, 24250.848933, 33808.300371, 44930.474642;
       18729.723740, 24930.256670, 34682.177289, 45806.106076;
       18384.705815, 24267.185768, 33816.554534, 44960.166492];

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