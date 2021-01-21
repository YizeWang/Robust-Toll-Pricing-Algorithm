function [cardinality, indSup] = FindSubsamples(tollCands, H, f, Aeq, beqList, lb, ub)

    numSamples = size(beqList, 2);
    tollOpt = ComputeSATolls(tollCands, H, f, Aeq, beqList, lb, ub);
    L = 1:numSamples;
    
    for i = 1:numSamples
        indToRemove = find(L == i);
        LPrime = [L(1:indToRemove-1), L(indToRemove+1:end)];
        beq = beqList(:, LPrime);
        tollOptCurr = ComputeSATolls(tollCands, H, f, Aeq, beq, lb, ub);
        
        if isequal(tollOpt, tollOptCurr)
            L = LPrime;
        end
    end
    
    cardinality = numel(L);
    indSup = L;
    
end