%% system setup
clc
clear all
close all

doComputeConfidence = true;

d = 1.0;
H = diag([1.0, 0.0]);
f = [0.0; 1.0];
Aeq = [1.0, 1.0];
beq = d;
lb = zeros(2, 1);
ub = [];

nameNetwork = 'Simple Double-Linked Network';
startPoints = [1 1];
endPoints = [2 2];
latencies = {'l_1 = x', 'l_2 = 1'}';
EdgeTable = table([startPoints' endPoints'], latencies, 'VariableNames', {'EndNodes', 'Labels'});

options = optimoptions('quadprog', 'Display', 'none');

%% print network
PlotGraph(nameNetwork, EdgeTable, []);

%% solve and plot nash flow
xNash = quadprog(H, f, [], [], Aeq, beq, lb, ub, [], options);
costNash = xNash' * H * xNash + f' * xNash;
PrintVector('Nash Flow', xNash);
PrintValue('Nash Cost', costNash);
PlotGraph(strcat(nameNetwork, ' Nash Flow'), EdgeTable, xNash);

%% solve and plot optimal flow
[xOpt, costOpt] = quadprog(2*H, f, [], [], Aeq, beq, lb, ub, [], options);
PrintVector('Optimal Flow', xOpt);
PrintValue('Optimal Cost', costOpt);
PlotGraph(strcat(nameNetwork, ' Optimal Flow'), EdgeTable, xOpt)

%% generate samples
N = 100;
mu = d;
sigma = 0.5;
uncertainty = 0.5;
pd = makedist('Normal', 'mu', mu, 'sigma', sigma);
tg = truncate(pd, mu-uncertainty, mu+uncertainty);
dSampled = random(tg, 1, N);

%% compute optimal tolls
t1Cands = 0:0.1:1;
t2Cands = 0.0;
tollCands = GenerateTollCandidates({t1Cands, t2Cands});
beqList = dSampled;

tollOpt = ComputeSATolls(tollCands, H, f, Aeq, beqList, lb, ub);
[xSA, costSA] = ComputeNashFlow(tollOpt, H, f, Aeq, beq, lb, ub);

PrintVector('SA Toll', tollOpt);
PrintVector('SA Flow', xSA);
PrintValue('SA Cost', costSA);
PlotGraph(strcat(nameNetwork, ' SA Flow'), EdgeTable, xSA);

%% compute confidence
if doComputeConfidence
    failureRisk = 1e-6;
    [cardinality, indSup] = FindSubsamples(tollCands, H, f, Aeq, beqList, lb, ub);
    epsilon = ComputeEpsilon(cardinality, N, failureRisk);
    PrintConfidence(epsilon, failureRisk);
end

%% compare costs
numPts = 100;
d = linspace(mu-uncertainty, mu+uncertainty, numPts);

cost = zeros(numPts, 6);

toll0 = [0.0; 0.0];
toll1 = [0.1; 0.0];
toll2 = [0.2; 0.0];
toll3 = [0.4; 0.0];
toll4 = [0.5; 0.0];

for k = 1:numPts
    beqNew = d(k);
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
legend('Nash', '\tau_1 = 0.1', '\tau_1 = 0.2', '\tau_1 = 0.4', '\tau_1 = 0.5 (Chosen)', 'Opt')