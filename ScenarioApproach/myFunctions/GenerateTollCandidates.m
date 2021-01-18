function [tollCands] = GenerateTollCandidates(var)

    tollCands = [];
    numLinks = numel(var);
    sizes = zeros(numLinks, 1);
    for i = 1:numLinks
        sizes(i, 1) = numel(var{i});
    end

    ms = cell(numLinks, 1);
    for i = 1:numLinks
        ms{i} = 1:sizes(i);
    end

    X = cell(numLinks, 1);
    [X{:}] = ndgrid(ms{:});
    for i = 1:numLinks 
        tollCandsOfCurrLink = reshape(var{i}, numel(var{i}), 1);
        tollCands = [tollCands tollCandsOfCurrLink(X{i}, :)];
    end

    tollCands = tollCands';
    
end