%% system setup
clc
clear all
close all

doComputeConfidence = true;

% decision variable [x_i; p_j], i = 1, ..., 10, j = 1, ..., 9
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
lb = zeros(19, 1);
ub = [];

nameNetwork = 'General Network';
startPoints = [1 1 2 2 3 3 4 4 4 5];
endPoints = [2 3 3 4 4 5 3 6 5 6];
latencies = {'l_1 = x+1', 'l_2 = 2x+1', 'l_3 = 3x+0.5', 'l_4 = x+3', 'l_5 = 0.5x+1', 'l_6 = 0.5x+4', 'l_7 = 4x', 'l_8 = 2x+0.5', 'l_9 = x', 'l_{10} = 1'}';
EdgeTable = table([startPoints' endPoints'], latencies, 'VariableNames', {'EndNodes', 'Labels'});

options = optimoptions('quadprog', 'Display', 'none');

%% print network
PlotGraph(nameNetwork, EdgeTable, []);

%% solve and plot nash flow
xNash = quadprog(H, f, [], [], Aeq, beq, lb, ub, [], options);
costNash = xNash' * H * xNash + f' * xNash;
PrintVector('Nash Flow', xNash(1:10));
PrintValue('Nash Cost', costNash);
PlotGraph(strcat(nameNetwork, ' Nash Flow'), EdgeTable, xNash((1:10)));

%% solve and plot optimal flow
[xOpt, costOpt] = quadprog(2*H, f, [], [], Aeq, beq, lb, ub, [], options);
PrintVector('Optimal Flow', xOpt(1:10));
PrintValue('Optimal Cost', costOpt);
PlotGraph(strcat(nameNetwork, ' Optimal Flow'), EdgeTable, xOpt(1:10));

%% generate samples
N = 1000;
mu = d;
sigma = 0.5;
uncertainty = 0.5;
pd = makedist('Normal', 'mu', mu, 'sigma', sigma);
tg = truncate(pd, mu-uncertainty, mu+uncertainty);
dSampled = random(tg, 1, N);

%% compute optimal tolls
pPlaceHolder = 0.0;
t1Cands = 0.0;
t2Cands = 0.0;
t3Cands = 0.0;
t4Cands = 0.0;
t5Cands = 0:0.1:1;
t6Cands = 0.0;
t7Cands = 0.0;
t8Cands = 0.0;
t9Cands = 0.0;
t10Cands = 0.0;
tollCands = GenerateTollCandidates({t1Cands, t2Cands, t3Cands, t4Cands, ...
                                    t5Cands, t6Cands, t7Cands, t8Cands, ...
                                    t9Cands, t10Cands, pPlaceHolder, ...
                                    pPlaceHolder, pPlaceHolder, pPlaceHolder, ...
                                    pPlaceHolder, pPlaceHolder, pPlaceHolder, ...
                                    pPlaceHolder, pPlaceHolder});
beqList = [zeros(10, N); dSampled];

tollOpt = ComputeSATolls(tollCands, H, f, Aeq, beqList, lb, ub);
[xSA, costSA] = ComputeNashFlow(tollOpt, H, f, Aeq, beq, lb, ub);

PrintVector('SA Toll', tollOpt);
PrintVector('SA Flow', xSA(1:10));
PrintValue('SA Cost', costSA);
PlotGraph(strcat(nameNetwork, ' SA Flow'), EdgeTable, xSA(1:10));

%% compute confidence
if doComputeConfidence
    failureRisk = 1e-6;
    [cardinality, indSup] = FindSubsamples(tollCands, H, f, Aeq, beqList, lb, ub);
    epsilon = ComputeEpsilon(cardinality, N, failureRisk);
    PrintConfidence(epsilon, failureRisk);
end

%% compare costs
numPts = 200;
d = linspace(mu-uncertainty, mu+uncertainty, numPts);

cost = zeros(numPts, 6);

toll0 = zeros(19, 1);
toll1 = zeros(19, 1);
toll2 = zeros(19, 1);
toll3 = zeros(19, 1);
toll4 = zeros(19, 1);
toll0(5) = 0.0;
toll1(5) = 0.5;
toll2(5) = 0.8;
toll3(5) = 0.9;
toll4(5) = 1.0;

for k = 1:numPts
    beqNew = [ zeros(10, 1); d(k)];
    [~, cost(k, 1)] = ComputeNashFlow(toll0, H, f, Aeq, beqNew, lb, ub);
    [~, cost(k, 2)] = ComputeNashFlow(toll1, H, f, Aeq, beqNew, lb, ub);
    [~, cost(k, 3)] = ComputeNashFlow(toll2, H, f, Aeq, beqNew, lb, ub);
    [~, cost(k, 4)] = ComputeNashFlow(toll3, H, f, Aeq, beqNew, lb, ub);
    [~, cost(k, 5)] = ComputeNashFlow(toll4, H, f, Aeq, beqNew, lb, ub);
    [~, cost(k, 6)] = quadprog(2*H, f, [], [], Aeq, beqNew, lb, ub, [], options);
end

figure('Name', 'Compare Costs with Different Tolls')
plot(d, cost)
xlabel('Demand')
ylabel('Social Cost')
legend('Nash', '\tau_5 = 0.5', '\tau_5 = 0.8', '\tau_5 = 0.9 (Chosen)', '\tau_5 = 1.0', 'Opt')