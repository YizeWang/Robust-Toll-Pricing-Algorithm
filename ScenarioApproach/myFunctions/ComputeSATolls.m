function [tollOpt] = ComputeSATolls(tollCands, H, f, Aeq, beqList, lb, ub)

    if isempty(tollCands)
        error('No toll candidates found');
    end

    costMin = inf;
    tollOpt = zeros(size(tollCands, 1), 1);

    for i = 1:size(tollCands, 2)
        costSup = -inf;
        toll = tollCands(:, i);
        
        for j = 1:size(beqList, 2)
            beq = beqList(:, j);
            [~, costNew] = ComputeNashFlow(toll, H, f, Aeq, beq, lb, ub);
            costSup = max(costSup, costNew);
        end
        
        if costSup < costMin
            costMin = costSup;
            tollOpt = toll;
        end
    end

end