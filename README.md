# Robust-Toll-Pricing-Algorithm

This repository stores the implementation of my Master's Thesis *Data-Driven Robust Congestion Pricing*. The thesis and conference paper can be found in `doc`.

## Abstract

Self-interested routing is often inefficient in traffic networks. Economists and computer scientists have proven that imposing proper tolls on congested roads, i.e., congestion pricing, can effectively improve network efficiency by reducing the total travel time experienced by all users. However, most researches focus on deterministic demands, while uncertainties are rarely studied. As a result, the tolls designed for the deterministic demands may behave undesirably when the actual demands deviate from the expectation. Existing solutions for uncertain demands mostly require a particular structure of either the network or the uncertainty, which motivates us to investigate a robust congestion pricing scheme for general networks that guarantees the toll performance under unknown uncertainties.

This thesis combines congestion pricing and scenario approach, a general framework for data-driven robust optimization, and formulates the robust toll design task as a bi-level optimization. Taking observed scenarios into account, we are able to design robust tolls that perform well when actual demands respect the same distribution with no knowledge of the distribution required. Besides exact algorithms, we also propose approximate ones to solve the NP-hard bi-level optimization within a reasonable time. We illustrate that the robustness can be quantified, and the toll-setter can compromise between robustness and performance. Finally, we demonstrate with numerical examples that the designed tolls can deal with uncertainties in unseen scenarios.

## Reference

Y. Wang and D. Paccagnan, "Data-Driven Robust Congestion Pricing," *2022 IEEE 61st Conference on Decision and Control (CDC)*, Cancun, Mexico, 2022, pp. 4437-4443