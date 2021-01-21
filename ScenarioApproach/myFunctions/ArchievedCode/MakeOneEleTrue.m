function [statCandExplSmps] = MakeOneEleTrue(statExplSmp)

numSmp = size(statExplSmp, 2);
statNotExpl = ~statExplSmp;
numNotExpl = nnz(statNotExpl);
indNotExpl = find(statNotExpl);
indNotExplSubs = sub2ind([numNotExpl, numSmp], 1:numNotExpl, indNotExpl);
indToExplSmps = false(numNotExpl, numSmp);
indToExplSmps(indNotExplSubs) = true;

statCandExplSmps = repmat(statExplSmp, numNotExpl, 1) | indToExplSmps;

end

