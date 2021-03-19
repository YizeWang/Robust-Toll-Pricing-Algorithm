import numpy as np
from aequilibrae.paths import TrafficAssignment, TrafficClass
from copy import copy


class GraphManager:

    def __init__(self, project, demand):

        project.network.build_graphs()
        self.graph = project.network.graphs['c']
        self.graph.set_graph('distance')
        self.graph.set_blocked_centroid_flows(False)

        self.FFT = self.graph.graph['free_flow_time'].to_numpy()
        self.B   = self.graph.graph['b'].to_numpy()
        self.C   = self.graph.graph['capacity'].to_numpy()
        self.P   = self.graph.graph['power'].to_numpy()

        self.demand = demand
        self.toll = np.zeros(self.graph.num_links)


    def ComputeSocialCost(self, xLink):

        termLinear = np.multiply(self.FFT, xLink)             # cost term linear in xLink
        TB = np.multiply(self.FFT, self.B)                    # free flow time * b
        base = np.divide(xLink, self.C)                       # xLink / capacity
        poly = np.power(base, self.P)                         # base * P
        termPoly = np.multiply(np.multiply(TB, poly), xLink)  # cost term polynomial in xLink

        return np.sum(termLinear + termPoly)


    def ImposeToll(self, toll):

        self.graph.graph['free_flow_time'] = self.FFT + toll
        self.graph.graph['b'] = np.divide(np.multiply(self.B, self.FFT), self.FFT)


    def ComputeNashFlow(self, alg='bfw', maxIter=1000, gap=0.0001):

        assig = TrafficAssignment()
        assigclass = TrafficClass(self.graph, self.demand)
        assig.set_classes([assigclass])
        assig.set_vdf("BPR")
        assig.set_vdf_parameters({"alpha": "b", "beta": "power"})
        assig.set_capacity_field("capacity")
        assig.set_time_field("free_flow_time")
        assig.set_algorithm(alg)

        assig.max_iter = maxIter
        assig.rgap_target = gap
        
        assig.execute()
        nashFlow = assigclass.results.link_loads.flatten()
        rgap = assig.assignment.convergence_report['rgap']

        return nashFlow, rgap
        
    def ComputeGradient(self, toll, deltaToll=0.1):
        
        numEdge = self.graph.num_links
        grad = np.zeros(numEdge, dtype=np.double)

        for m in range(numEdge):

            minusTolls = copy(toll)
            plusTolls = copy(toll)
            minusTolls[m] = minusTolls[m] - deltaToll if minusTolls[m] - deltaToll > 0 else 0
            plusTolls[m] = plusTolls[m] + deltaToll

            self.ImposeToll(minusTolls)
            minusFlow, _ = self.ComputeNashFlow()
            minusH = self.ComputeSocialCost(minusFlow)

            self.ImposeToll(plusTolls)
            plusFlow, _ = self.ComputeNashFlow()
            plusH = self.ComputeSocialCost(plusFlow)

            num = plusH - minusH
            den = deltaToll * 2 if minusTolls[m] - deltaToll > 0 else deltaToll + minusTolls[m]

            gradient = num / den
            grad[m] = gradient

        return grad

    def GradientDescent(self):

        maxIteration = 1
        currIteration = 1
        nashFlow, _ = self.ComputeNashFlow()
        H = self.ComputeSocialCost(nashFlow)
        Hs = [H]
        tolls = np.zeros((1, self.graph.num_links))
        gammas = []
        print(H)

        while currIteration < maxIteration:

            
            currIteration = currIteration + 1
            grad = self.ComputeGradient(self.toll)
            gamma = 0.001 / currIteration
            self.toll = self.toll - grad * gamma
            self.toll[self.toll<0] = 0
            tolls = np.vstack((tolls, self.toll))
            prevH = copy(H)
            self.ImposeToll(self.toll)
            nashFlow, _ = self.ComputeNashFlow()
            H = self.ComputeSocialCost(nashFlow)
            Hs.append(H)
            print(H)
            gammas.append(gamma)
            if abs(prevH - H) < 10:
                break

        return Hs, tolls, gammas