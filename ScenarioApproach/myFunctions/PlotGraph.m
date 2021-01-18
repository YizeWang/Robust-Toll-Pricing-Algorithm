function [] = PlotGraph(name, EdgeTable, flows)

    numLinks = size(EdgeTable, 1);
    lineWidthCoeff = 5.0;
    
    if isempty(flows)
        weights = ones(numLinks, 1) / numLinks;
        labels = EdgeTable.Labels;
    else
        weights = flows * lineWidthCoeff / sum(flows);
        x = [ones(numLinks, 1) * 'x = ', num2str(flows, 4)];
        labels = mat2cell(x, ones(1, numLinks), size(x, 2));
    end
    
    EdgeTable.EdgeLabel = labels;
    EdgeTable.LineWidth = weights;
    G = digraph(EdgeTable);
    figure('Name', name);
    plot(G, 'EdgeLabel', G.Edges.EdgeLabel, 'LineWidth', G.Edges.LineWidth);

end