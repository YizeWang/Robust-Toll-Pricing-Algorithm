import time
import numpy as np
from copy import copy
from os.path import join
import matplotlib.pyplot as plt
from aequilibrae.project import Project
from aequilibrae.matrix import AequilibraeMatrix
from aequilibrae.paths import TrafficAssignment, TrafficClass


class ScenarioApproachManager:

    def __init__(self, pathDmndDir, pathProjDir, numSample):

        project = Project()
        project.load(pathProjDir)
        project.network.build_graphs()
        project.close()

        demand = AequilibraeMatrix()
        demand.load(join(pathDmndDir, 'demand.omx'))
        demand.computational_view(['matrix'])

        self.graph = project.network.graphs['c']
        self.graph.set_graph('distance')
        self.graph.set_blocked_centroid_flows(False)

        self.FFT = copy(self.graph.graph['free_flow_time'].to_numpy())
        self.B   = copy(self.graph.graph['b'].to_numpy())
        self.C   = copy(self.graph.graph['capacity'].to_numpy())
        self.P   = copy(self.graph.graph['power'].to_numpy())

        self.demand = demand
        self.numSample = numSample
    

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


    def ComputeNashFlow(self, indSample, toll, alg='bfw', maxIter=1000, gap=0.0001):

        self.ImposeToll(toll)

        self.demand.computational_view(['Demand'+str(indSample)])

        assig = TrafficAssignment()
        assigclass = TrafficClass(self.graph, self.demand)
        assig.set_classes([assigclass])
        assig.set_cores(4)
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
        

    def ComputeBigH(self, toll):

        hList = np.zeros(self.numSample)

        for indSample in range(self.numSample):
            nashFlow, _ = self.ComputeNashFlow(indSample, toll)
            hList[indSample] = self.ComputeSocialCost(nashFlow)

        return np.max(hList), hList, np.argmax(hList)


    def ComputeGradient(self, toll, deltaToll=0.1):
        
        numEdge = self.graph.num_links
        grad = np.zeros(numEdge, dtype=np.double)

        for m in range(numEdge):

            minusToll = copy(toll)
            plusToll = copy(toll)
            minusToll[m] = max(minusToll[m]-deltaToll, 0)
            plusToll[m] = plusToll[m] + deltaToll

            minusH, _, _ = self.ComputeBigH(minusToll)
            plusH, _, _ = self.ComputeBigH(plusToll)

            num = plusH - minusH
            den = deltaToll * 2 if minusToll[m] > 0 else deltaToll + toll[m]

            gradient = num / den
            grad[m] = gradient

        return grad

        
    def GradientDescent(self, toll=None):

        maxIteration = 200
        currIteration = 0

        toll = np.zeros(self.graph.num_links) if toll is None else toll
        H, hList, _ = self.ComputeBigH(toll)

        Hs = [H]
        hLists = np.reshape(hList, (1, -1))
        gammas = []
        times = []
        tolls = np.reshape(toll, (1, -1))

        print("Iteration: %d, H: %.1f" % (currIteration, H))

        fig, (ax) = plt.subplots(1, 1)
        ax.set_xlim([0, maxIteration])
        ax.scatter(np.zeros(self.numSample), hList)
        plt.pause(0.05)

        while currIteration < maxIteration:

            startTime = time.time()
            currIteration = currIteration + 1

            grad = self.ComputeGradient(toll)

            gamma = 0.001 / currIteration
            step = grad * gamma
            maxMagStep = np.max(np.abs(step))
            normStep = step / maxMagStep

            toll = toll - normStep
            toll[toll<0] = 0

            tolls = np.vstack((tolls, np.reshape(toll, (1, -1))))

            prevH = copy(H)

            H, hList, _ = self.ComputeBigH(toll)
            
            Hs.append(H)
            hLists = np.vstack((hLists, hList))
            tElapsed = float(time.time()-startTime)
            print("Iteration: %d, H: %.1f, Time: %.1f, Gamma: %f, dH: %.1f" % (currIteration, H, tElapsed, gamma, H-prevH))
            times.append(tElapsed)
            gammas.append(gamma)

            ax.plot(range(len(Hs)), hLists)
            plt.pause(0.05)

            if abs(prevH - H) < 300: break

        return Hs, tolls, gammas, times, hLists


    def GreedyComputeBigH(self, indSampleList, toll):

        h = -1

        for indSample in indSampleList:

            self.demand.computational_view(['Demand'+str(indSample)])
            nashFlow, _ = self.ComputeNashFlow(indSample, toll)
            h = max(h, self.ComputeSocialCost(nashFlow))

        return h


    def GreedyComputeGradient(self, indSampleList, toll, deltaToll=0.1):

        numEdge = self.graph.num_links
        grad = np.zeros(numEdge, dtype=np.double)

        for m in range(numEdge):

            minusToll = copy(toll)
            plusToll = copy(toll)
            minusToll[m] = max(minusToll[m]-deltaToll, 0)
            plusToll[m] = plusToll[m] + deltaToll

            minusH = self.GreedyComputeBigH(indSampleList, minusToll)
            plusH = self.GreedyComputeBigH(indSampleList, plusToll)

            num = plusH - minusH
            den = deltaToll * 2 if minusToll[m] > 0 else deltaToll + toll[m]

            gradient = num / den
            grad[m] = gradient

        return grad


    def GreedyGradientDescent(self, toll):

        maxIteration = 2
        currIteration = 0

        toll = np.zeros(self.graph.num_links) if toll is None else toll
        H, hList, _ = self.ComputeBigH(toll)
        prevH = copy(H)

        Hs = [H]
        hLists = np.reshape(hList, (1, -1))
        gammas = []
        times = []
        tolls = np.reshape(toll, (1, -1))

        while currIteration < maxIteration:
            startTime = time.time()
            currIteration = currIteration + 1

            indSampleList = []
            H, hList, indMaxH = self.ComputeBigH(toll)
            indSampleList.append(indMaxH)

            while True:
                grad = self.GreedyComputeGradient(indSampleList, toll)
                gamma = 0.001 / currIteration
                step = grad * gamma
                maxMagStep = np.max(np.abs(step))
                normStep = step / maxMagStep

                tollTry = toll - normStep
                tollTry[tollTry<0] = 0

                H, hList, indMaxH = self.ComputeBigH(tollTry)
                if indMaxH not in indSampleList:
                    indSampleList.append(indMaxH)
                else:
                    toll = tollTry
                    indSampleList.clear()
                    break

            Hs.append(H)
            hLists = np.vstack((hLists, hList))
            tElapsed = float(time.time()-startTime)
            gammas.append(gamma)
            times.append(tElapsed)
            tolls = np.vstack((tolls, np.reshape(toll, (1, -1))))
            print("Iteration: %d, H: %.1f, Time: %.1f, Gamma: %f, dH: %.1f" % (currIteration, H, tElapsed, gamma, H-prevH))

            if abs(prevH - H) < 300: break
            prevH = copy(H)

        return Hs, tolls, gammas, times, hLists
