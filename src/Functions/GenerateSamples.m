function [ODsSampled] = GenerateSamples(ODs, numSmpl)

numDmnd = size(ODs, 1);

mu = 1.0;
sigma = 0.5;
uncertainty = 0.5;
pd = makedist('Normal', 'mu', mu, 'sigma', sigma);
tg = truncate(pd, mu-uncertainty, mu+uncertainty);

coeffSampled = random(tg, numDmnd, numSmpl);
demandSampled = coeffSampled .* ODs(:, 3);

ODsSampled = [ODs(:, 1), ODs(:, 2), demandSampled];

end