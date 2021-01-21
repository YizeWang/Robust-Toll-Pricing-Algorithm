function [xNash, costNash] = ComputeNashFlow(toll, H, f, Aeq, beq, lb, ub)

    options = optimoptions('quadprog', 'Display', 'none');
    fTolled = f + toll;
    xNash = quadprog(H, fTolled, [], [], Aeq, beq, lb, ub, [], options);
    costNash = xNash' * H * xNash + f' * xNash;
    
end