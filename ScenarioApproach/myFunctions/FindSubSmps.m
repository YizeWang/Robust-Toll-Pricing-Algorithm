function [statSubSmp] = FindSubSmps(H, f, Aeq, beqs, taxable)

isCompleted = false;
numSmp = size(beqs, 2);
statSubSmp = zeros(1, numSmp);
statNotExpl = ones(1, numSmp);
statSubSmp(1) = true;
statNotExpl(1) = false;

[~, optH] = ComputeOptTolls(H, f, Aeq, beqs, taxable);

while ~isCompleted
    [statSubSmp, statNotExpl, isCompleted] = UpdateSubSmps(statSubSmp, statNotExpl, H, f, Aeq, beqs, taxable, optH);
end

end