function [optTolls, optH, indSubSmpl] = CompOptTollGreedy(H, f, Aeq, beqs, taxable)

tol = 0.01;
numSmp = size(beqs, 2);
firstSmp = randi([1, numSmp], 1, 1);
statExplSmp = false(1, numSmp);
statExplSmp(firstSmp) = true;
maxH = 0;

if numSmp == 1
	indSubSmpl = 1;
	[optTolls, optH] = ComputeOptTolls(H, f, Aeq, beqs(:, indSubSmpl), taxable);
    return;
end

while true
    statCandExplSmps = MakeOneEleTrue(statExplSmp);
    numToExplSmp = size(statCandExplSmps, 1);
    
    h = zeros(numToExplSmp, 1);
    for k = 1:numToExplSmp
        statCandSubSmp = statCandExplSmps(k, :);
        [~, h(k)] = ComputeOptTolls(H, f, Aeq, beqs(:, statCandSubSmp), taxable);
    end
    [maxCurrH, indMaxH] = max(h);
    
    if abs(maxCurrH-maxH) < tol
        break;
    end
    
    maxH = maxCurrH;
    statExplSmp = statCandExplSmps(indMaxH, :);
end

indSubSmpl = find(statExplSmp);
[optTolls, optH] = ComputeOptTolls(H, f, Aeq, beqs(:, indSubSmpl), taxable);

end

