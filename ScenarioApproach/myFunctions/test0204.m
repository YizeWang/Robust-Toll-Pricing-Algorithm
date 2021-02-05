%% network construction
clc
clear all
close all

nameNetwork1   = 'SimpleGeneralNetwork';
nameNetwork2   = 'SiouxFalls';
nameNetwork3   = 'Brasse';
pathDataFolder = '..\myRealData\';

nameNetwork = nameNetwork2;
G = ParseTNTP(pathDataFolder, nameNetwork);
PlotNetwork(G);

Q = readmatrix([pathDataFolder nameNetwork2 '\SiouxFalls_trips.csv']);

ODs = [];
for i = 1:24
    for j = 1:24
        if i == j || Q(i, j) == 0
            continue;
        end
        ODs = [ODs; i, j, Q(i, j)];
    end
end

tic
[x1, it1, xs1] = CompNashFlowFW(G, ODs);
t1 = toc;

tic
[x2, it2, xs2] = CompNashFlowFW2(G, ODs);
t2 = toc;

tic
[x3, it3, xs3] = CompNashFlowFW3(G, ODs);
t3 = toc;

% extract vector values
FFT = G.Edges.FreeFlowTime;
B   = G.Edges.B;
Pow = G.Edges.Power;
Cap = G.Edges.Capacity;

cost1 = sum(FFT .* x1 + B ./ (Pow + 1) .* x1 .^ (Pow + 1) ./ (Cap .^ Pow));
cost2 = sum(FFT .* x2 + B ./ (Pow + 1) .* x2 .^ (Pow + 1) ./ (Cap .^ Pow));
cost3 = sum(FFT .* x3 + B ./ (Pow + 1) .* x3 .^ (Pow + 1) ./ (Cap .^ Pow));

costs1 = [];
costs2 = [];
costs3 = [];

for i = 1:size(xs1, 2)
    x1 = xs1(1:G.numedges, i);
    costs1 = [costs1 sum(FFT .* x1 + B ./ (Pow + 1) .* x1 .^ (Pow + 1) ./ (Cap .^ Pow))];
end

for i = 1:size(xs2, 2)
    x2 = xs2(1:G.numedges, i);
    costs2 = [costs2 sum(FFT .* x2 + B ./ (Pow + 1) .* x2 .^ (Pow + 1) ./ (Cap .^ Pow))];
end

for i = 1:size(xs3, 2)
    x3 = xs3(1:G.numedges, i);
    costs3 = [costs3 sum(FFT .* x3 + B ./ (Pow + 1) .* x3 .^ (Pow + 1) ./ (Cap .^ Pow))];
end

xlabels1 = 1:size(xs1, 2);
xlabels2 = 1:size(xs2, 2);
xlabels3 = 1:size(xs3, 2);

plot(xlabels1, costs1, xlabels2, costs2, xlabels3, costs3)