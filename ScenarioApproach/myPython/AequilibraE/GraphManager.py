import time
import numpy as np
from copy import copy
import numpy as nameProject
from aequilibrae.paths import TrafficAssignment, TrafficClass


class GraphManager:

    def __init__(self, project, demand):

        project.network.build_graphs()
        self.graph = project.network.graphs['c']
        self.graph.set_graph('distance')
        self.graph.set_blocked_centroid_flows(False)

        self.FFT = copy(self.graph.graph['free_flow_time'].to_numpy())
        self.B   = copy(self.graph.graph['b'].to_numpy())
        self.C   = copy(self.graph.graph['capacity'].to_numpy())
        self.P   = copy(self.graph.graph['power'].to_numpy())

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
        self.graph.graph['b'] = np.divide(np.multiply(self.B, self.FFT), self.FFT + toll)


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

            minusToll = copy(toll)
            plusToll = copy(toll)
            minusToll[m] = max(minusToll[m]-deltaToll, 0)
            plusToll[m] = plusToll[m] + deltaToll

            self.ImposeToll(minusToll)
            minusFlow, _ = self.ComputeNashFlow()
            minusH = self.ComputeSocialCost(minusFlow)

            self.ImposeToll(plusToll)
            plusFlow, _ = self.ComputeNashFlow()
            plusH = self.ComputeSocialCost(plusFlow)

            num = plusH - minusH
            den = deltaToll * 2 if minusToll[m] > 0 else deltaToll + toll[m]

            gradient = num / den
            grad[m] = gradient

        return grad

    def ComputeTollNash(self, toll):
        
        self.ImposeToll(toll)
        nashFlow, _ = self.ComputeNashFlow()
        H = self.ComputeSocialCost(nashFlow)

        return H

    def GradientDescent(self, toll=None):

        maxIteration = 200
        currIteration = 0

        self.toll = np.zeros(self.graph.num_links) if toll is None else toll
        H = self.ComputeTollNash(self.toll)

        Hs = [H]
        gammas = []
        times = []
        tolls = np.reshape(self.toll, (1, -1))

        print("Iteration: %d, H: %.1f" % (currIteration, H))

        while currIteration < maxIteration:

            startTime = time.time()
            currIteration = currIteration + 1

            grad = self.ComputeGradient(self.toll)

            gamma = 0.001 / currIteration
            step = grad * gamma
            maxMagStep = np.max(np.abs(step))
            step = step / maxMagStep

            self.toll = self.toll - step
            self.toll[self.toll<0] = 0

            tolls = np.vstack((tolls, np.reshape(self.toll, (1, -1))))

            prevH = copy(H)
            H = self.ComputeTollNash(self.toll)
            
            Hs.append(H)
            tElapsed = float(time.time()-startTime)
            print("Iteration: %d, H: %.1f, Time: %.1f, Gamma: %f, dH: %.1f" % (currIteration, H, tElapsed, gamma, H-prevH))
            times.append(tElapsed)
            gammas.append(gamma)

            if abs(prevH - H) < 200: break

        return Hs, tolls, gammas, times
