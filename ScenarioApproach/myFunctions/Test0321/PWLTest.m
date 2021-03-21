clc
clear all
close all

precision = [0.01 0.001 0.0001 0.00001 0.005 0.0005 0.00005];
costNash = [4232606.350190781 4231467.052984258 4231348.212970314 4231336.627743795 4232116.305691689 4231397.073390721 4231341.992354427];
error = [2.6612893228255878e-11 2.0980198619483205e-11 2.3261087593992077e-11 2.338378601054728e-11 2.4240917565190228e-11 2.2733736339354608e-11 2.0321502367407864e-11];
socalCost = [7478480.773066, 7476898.677473, 7478832.353137, 7480371.072192, 7496975.868122, 7482705.020695, 7480975.322723];


aNash = 4231384.934405/ min(costNash);
asocaiCost = 7472359.874570/ min(socalCost);

costNash = costNash / min(costNash);
socalCost = socalCost / min(socalCost);

table = [precision; costNash; error; socalCost];
table = sortrows(table')';

figure(1)
hold on
set(gca, 'XScale', 'log')
yyaxis left
plot(table(1, :), table(2, :))
ylabel('Normalized Nash Objective')
plot(precision, repmat(aNash, 1, 7), 'LineWidth', 0.5, 'LineStyle', '--')
yyaxis right
plot(table(1, :), table(4, :))
xlabel('Max Relative Piece Error')
ylabel('Normalized Social Cost')
plot(precision, repmat(asocaiCost, 1, 7), 'LineWidth', 0.5, 'LineStyle', '--')
legend('Gurobi', 'AequilibraE', 'Gurobi', 'AequilibraE')
title('Numerical Accuracy Comparison')