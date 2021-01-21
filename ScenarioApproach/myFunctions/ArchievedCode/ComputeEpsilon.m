function epsilon = ComputeEpsilon(k, N, failureRisk)

    isValid = (isequal(size(k), size(N)) && ...
               isequal(size(N), size(failureRisk)) && ...
               isequal(size(failureRisk), [1, 1]));

    if ~isValid || k > N || failureRisk < 0
        error("invalid arguments");
    end

    if k == N
        epsilon = 1;
        return;
    end

    % nchoosek method cannot deal with overflow
    pow = (gammaln(N+1) - gammaln(k+1) - gammaln(N-k+1)) / (k-N);
    t = exp(pow);

    epsilon = 1 - (failureRisk/N)^(1/(N-k)) * t;

end