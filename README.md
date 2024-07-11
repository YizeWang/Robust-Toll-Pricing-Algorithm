# Robust-Toll-Pricing-Algorithm

This repository stores the implementation of my Master's Thesis *Data-Driven Robust Congestion Pricing*. The thesis and conference paper can be found in `doc`.

## Abstract

Whilst overloaded transportation systems bear a significant impact on everyone’s welfare, governments strive to improve their performances. Amongst the many solutions proposed, congestion pricing is becoming increasingly popular as it has the potential to reduce congestion by indirectly influencing the drivers’ routing choices. Commonly advocated for, the marginal cost mechanism ensures that self-interested decision-making results in optimal system performances. However, such a mechanism suffers from three important drawbacks in that i) it requires levying tolls on every road, ii) it does not allow for upper bounds on the magnitude of the tolls, and iii) it is flow-dependent. In response to these challenges, researchers have introduced the restricted network tolling problem, seeking constant tolls of bounded magnitude that induce equilibria with a small social cost. However, tolls designed through this approach are tailored to a specific traffic demand, resulting in a design that has the potential to exacerbate the very issue it set out to solve, if the demand changes. Our work addresses this issue and aims at infusing robustness guarantees to the restricted network tolling problem. We do so by seeking tolls that have good performance over past demand realizations, and leverage recent results in scenario optimization to equip our design with formal generalization guarantees.

## Reference

Y. Wang and D. Paccagnan, "Data-Driven Robust Congestion Pricing," *2022 IEEE 61st Conference on Decision and Control (CDC)*, Cancun, Mexico, 2022, pp. 4437-4443