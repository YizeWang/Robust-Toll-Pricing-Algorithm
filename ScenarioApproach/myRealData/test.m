%% load data
clc
close all
clear all

pathData = 'Data/';
nameNetwork = 'ComplexGeneralNetwork';
G = ParseGraph(pathData, nameNetwork);

%% construct system model
factorPrune = 10;
ODs = [1, 6, 1.0]; % source-target-demand
[A, b] = ModelSystem(G, ODs, factorPrune);