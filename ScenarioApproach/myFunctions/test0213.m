clc
close all
clear all

%% network construction
date = datetime('now');
date.Format = 'yyyyMMddHHmm';
nameDiary = ['./Diary/' char(date) '-Diary.txt'];
diary(nameDiary);

nameNetwork1   = 'SimpleGeneralNetwork';
nameNetwork2   = 'SiouxFalls';
nameNetwork3   = 'Brasse';
pathDataFolder = '..\myRealData\';

nameNetwork = nameNetwork2;
G = ParseTNTP(pathDataFolder, nameNetwork);
ODs = readmatrix([pathDataFolder nameNetwork '\' nameNetwork '_ODs.csv']);

%% generate data
% ODsSampled = GenerateSamples(ODs, numSmpl);
ODs = ODs(1:50, :);
ODs(:, 3) = ODs(:, 3) / 1000;
Params = ExtractParameters(G, ODs);
[A, b] = GetEqualityConstraints(G, ODs);
[xOpt1, tOpt1, hOpt1] = ComputeOptimalTolls1(G, ODs, Params);
% [xOpt2, tOpt2, hOpt2] = ComputeOptimalTolls2(G, ODs, Params);
% [xOpt3, tOpt3, hOpt3] = ComputeOptimalTolls3(G, ODs, Params);
% [xOpt4, tOpt4, hOpt4] = ComputeOptimalTolls4(G, ODs, Params);

diary off