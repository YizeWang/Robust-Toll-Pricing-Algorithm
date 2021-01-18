clc
clear all
close all

% case setup
numArcs = 6;
demands = 1;
aLatencyFunctions = [  1,   2,   3,   1,   1,   5];
bLatencyFunctions = [  1, 0.5, 0.1,   2,   3,   1];
thetaRestrictions = [0, inf, inf, 1, inf,   4];

Z = [bLatencyFunctions+thetaRestrictions inf];
costs = [];
flows = [];
tolls = [];
for indZ = 1:size(Z, 2)
    z = Z(indZ);
    for indB = 1:size(bLatencyFunctions, 2)
        Az = find(bLatencyFunctions <= z);
        numUsed = size(Az, 2);
        k = aLatencyFunctions(Az)';
        K = diag(k);
        b = bLatencyFunctions(Az)';
        H = 2 * K;
        Aeq = ones(1, numUsed);
        beq = demands;
        lb = zeros(numUsed, 1);
        ub = max((z*ones(numUsed, 1)-b)./k, 0);
        Kbar = repmat(K, numUsed, 1);
        bbar = repmat(b, numUsed, 1);
        Ktilde = reshape(repmat(K, 1, numUsed)', [], numUsed*numUsed)';
        btilde = reshape(repmat(b, 1, numUsed)', [], numUsed*numUsed)';
        theta = thetaRestrictions(Az)';
        thetatilde = reshape(repmat(theta, 1, numUsed)', [], numUsed*numUsed)';
        Aineq = Kbar-Ktilde;
        bineq = btilde+thetatilde-bbar;
        [f, C] = quadprog(H, b', Aineq, bineq, Aeq, beq, lb, ub);
        if(isempty(C))
            costs = [costs, inf];
            flows = [flows, zeros(numArcs, 1)];
            continue;
        end
        costs = [costs, C];
        flow = zeros(numUsed, 1);
        flow(Az) = f;
        flows = [flows, flow];
    end
end






% % construct candidate set
% indexN = find(thetaRestrictions == 0);
% indexT = find(thetaRestrictions ~= 0);
% if(isempty(indexN) || isempty(indexT))
%     error("There should be at least one taxable/non-taxable arc.")
% end
% N = sortrows([bLatencyFunctions(indexN)', indexN']);
% T = sortrows([bLatencyFunctions(indexT)', indexT']);
% N = N(:, 2)';
% T = T(:, 2)';
% S = cell(size(N, 2)*size(T, 2), 1);
% for i = 1:size(N, 2)
%     for j = 1:size(T, 2)
%         S((i-1)*size(T, 2)+j, 1) = {[N(1:i), T(1:j)]};
%     end
% end

% %% plot network graph
% startPoints = ones(1, numArcs) * 1;
% endPoints = ones(1, numArcs) * 2;
% eWeights = ones(1, numArcs) * 1;
% G = graph(startPoints, endPoints, eWeights);
% nLabels = {'{source}', '{destination}'};
% LWidths = 5 * G.Edges.Weight / max(G.Edges.Weight);
% plot(G, 'EdgeLabel', G.Edges.Weight, 'NodeLabel', nLabels, 'LineWidth', LWidths);