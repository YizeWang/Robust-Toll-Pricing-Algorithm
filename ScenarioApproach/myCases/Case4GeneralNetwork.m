%% system setup
clc
clear all
close all

doComputeConfidence = false;

% decision variable [p_i; x_j], i = 1, 2, 3, j = 1, 2, 3, 4, 5
d = 1.0;
H = diag([0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 4.0]);
f = [0.0; 0.0; 0.0; 1.0; 1.0; 1.0; 1.5; 2.0];
Aeq = [1  1  1  0  0  0  0  0;
       1  0  0 -1  0  0  0  0;
       1  0  0  0 -1  0  0  0;
       1  1  0  0  0 -1  0  0;
       0  1  0  0  0  0 -1  0;
       0  0  1  0  0  0  0 -1];
beq = [d; zeros(5, 1)];
lb = zeros(8, 1);
ub = [];

nameNetwork = 'Simple General Network';
startPoints = [1 2 3 1 1];
endPoints = [2 3 4 3 4];
latencies = {'l_1 = 1', 'l_2 = x+1', 'l_3 = x+1', 'l_4 = x+1.5', 'l_5 = 4x+2'}';
EdgeTable = table([startPoints' endPoints'], latencies, 'VariableNames', {'EndNodes', 'Labels'});

options = optimoptions('quadprog', 'Display', 'none');

%% print network
PlotGraph(nameNetwork, EdgeTable, []);

%% solve and plot nash flow
xNash = quadprog(H, f, [], [], Aeq, beq, lb, ub, [], options);
costNash = xNash' * H * xNash + f' * xNash;
PrintVector('Nash Flow', xNash(4:end));
PrintValue('Nash Cost', costNash);
PlotGraph(strcat(nameNetwork, ' Nash Flow'), EdgeTable, xNash(4:end));

%% solve and plot optimal flow
[xOpt, costOpt] = quadprog(2*H, f, [], [], Aeq, beq, lb, ub, [], options);
PrintVector('Optimal Flow', xOpt(4:end));
PrintValue('Optimal Cost', costOpt);
PlotGraph(strcat(nameNetwork, ' Optimal Flow'), EdgeTable, xOpt(4:end))

%% generate samples
N = 100;
mu = d;
sigma = 0.5;
uncertainty = 0.5;
pd = makedist('Normal', 'mu', mu, 'sigma', sigma);
tg = truncate(pd, mu-uncertainty, mu+uncertainty);
dSampled = random(tg, 1, N);

%% compute optimal tolls
p1PlaceHolder = 0.0;
p2PlaceHolder = 0.0;
p3PlaceHolder = 0.0;
t1Cands = 0.0;
t2Cands = 0.0;
t3Cands = 0.0;
t4Cands = 0:0.1:1;
t5Cands = 0.0;
tollCands = GenerateTollCandidates({p1PlaceHolder, p2PlaceHolder, p3PlaceHolder, t1Cands, t2Cands, t3Cands, t4Cands, t5Cands});
beqList = [dSampled; zeros(5, N)];

tollOpt = ComputeSATolls(tollCands, H, f, Aeq, beqList, lb, ub);
[xSA, costSA] = ComputeNashFlow(tollOpt, H, f, Aeq, beq, lb, ub);

PrintVector('SA Toll', tollOpt);
PrintVector('SA Flow', xSA(4:end));
PrintValue('SA Cost', costSA);
PlotGraph(strcat(nameNetwork, ' SA Flow'), EdgeTable, xSA(4:end));

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

toll0 = [zeros(3, 1); zeros(3, 1); 0.00; zeros(1, 1)];
toll1 = [zeros(3, 1); zeros(3, 1); 0.10; zeros(1, 1)];
toll2 = [zeros(3, 1); zeros(3, 1); 0.15; zeros(1, 1)];
toll3 = [zeros(3, 1); zeros(3, 1); 0.20; zeros(1, 1)];
toll4 = [zeros(3, 1); zeros(3, 1); 0.40; zeros(1, 1)];

for k = 1:numPts
    beqNew = [d(k); zeros(5, 1)];
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
legend('Nash', '\tau_4 = 0.1', '\tau_4 = 0.15', '\tau_4 = 0.2 (Chosen)', '\tau_4 = 0.4', 'Opt')