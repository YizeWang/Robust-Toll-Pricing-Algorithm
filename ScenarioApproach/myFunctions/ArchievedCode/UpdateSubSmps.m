function [statSubSmp, statNotExpl, isCompleted] = UpdateSubSmps(statSubSmp, statNotExpl, H, f, Aeq, beqs, taxable, optH)

tol = 0.01;
numSmp = length(statSubSmp);
numNotExpl = nnz(statNotExpl);

[~, currH] = ComputeOptTolls(H, f, Aeq, beqs(:, find(statSubSmp)), taxable);

if abs(currH-optH) < tol || numNotExpl == 0
    statNotExpl = zeros(1, numSmp);
    isCompleted = true;
    return;
end

statCandSubSmps = MakeOneEleTrue(statSubSmp);

h = zeros(numNotExpl, 1);
for k = 1:numNotExpl
    statCandSubSmp = statCandSubSmps(k, :);
    [~, h(k)] = ComputeOptTolls(H, f, Aeq, beqs(:, statCandSubSmp), taxable);
end
[~, indMaxH] = max(h);

statSubSmp = statCandSubSmps(indMaxH, :);
statNotExpl(indNotExpl(indMaxH)) = false;
isCompleted = false;

end