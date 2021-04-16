import os
import time
import subprocess
import numpy as np
import pandas as pd
from copy import copy
from hashlib import sha1


class TrafficAssigner:

    def __init__(self):
        self.pathExecutable = None
        self.pathTempFolder = None
        self.maxIteration = None
        self.pathDemandData = None
        self.pathEdgeData = None
        self.demandData = None
        self.edgeData = None
        self.tempEdgeData = None
        self.objective = None
        self.pathFlowData = None
        self.numSample = None
        self.listOD = []
        self.optCosts = []
        self.numEdges = None
        self.buffer = {}

    def SetDataFolderPath(self, pathDataFolder: str) -> None:
        self.pathEdgeData = os.path.join(pathDataFolder, "edges.csv")
        self.pathDemandData = os.path.join(pathDataFolder, "od.csv")
        self.edgeData = pd.read_csv(self.pathEdgeData, delimiter=',')
        self.demandData = pd.read_csv(self.pathDemandData, delimiter=',')
        self.numEdges = len(self.edgeData)

    def SetTempFolderPath(self, pathTempFolder: str) -> None:
        self.pathTempFolder = pathTempFolder
        self.tempEdgeData = os.path.join(pathTempFolder, "edges.csv")
        self.pathFlowData = os.path.join(pathTempFolder, "flow.csv")

        os.makedirs(pathTempFolder, exist_ok=True) 

    def SetExecutablePath(self, pathExecutable: str) -> None:
        self.pathExecutable = pathExecutable

    def SetMaxIteration(self, maxIteration: int) -> None:
        self.maxIteration = maxIteration

    def SetObjective(self, objective: str) -> None:
        self.objective = objective

    def ImposeToll(self, toll: np.array) -> None:
        edges = self.edgeData.copy()
        lengthModified = edges.length + np.multiply(toll*60.0, edges.speed) / 3.6
        edges.b = np.divide(np.multiply(edges.length, edges.b), lengthModified)
        edges.length = lengthModified
        edges.to_csv(self.tempEdgeData, index=False)

    def AssignTraffic(self, toll: np.array, indSample: int=None, objective: str=None) -> None:
        self.ImposeToll(toll)
        if objective is None: objective = self.objective
        pathDemandData = self.pathDemandData if indSample is None else self.listOD[indSample]

        if (sha1(toll).hexdigest(), indSample) in self.buffer:
            return self.buffer[(sha1(toll).hexdigest(), indSample)]

        args = f'-n {str(self.maxIteration)} -i {self.tempEdgeData} -od {pathDemandData} -o {self.pathTempFolder} -obj {objective}'.split(' ')
        subprocess.run([self.pathExecutable] + args)
        flow = pd.read_csv(self.pathFlowData, skiprows=1, delimiter=',')
        
        if objective == 'user_eq':
            self.buffer[(sha1(toll).hexdigest(), indSample)] = flow.flow.to_numpy()

        return flow.flow.to_numpy()

    def SocialCost(self, flow: np.array) -> float:
        FFT = np.divide(self.edgeData.length, self.edgeData.speed) * 0.06
        termLinear = np.multiply(FFT, flow)
        TB = np.multiply(FFT, self.edgeData.b)
        base = np.divide(flow, self.edgeData.capacity)
        poly = np.power(base, self.edgeData.power)
        termPoly = np.multiply(np.multiply(TB, poly), flow)

        return np.sum(termLinear + termPoly)

    def GenSample(self, numSample: int, randRange: float) -> None:
        self.numSample = numSample
        numDmnd = len(self.demandData)

        for s in range(numSample):
            randCoeff = (np.random.rand(numDmnd) - 0.5) * 2 * randRange + 1
            randDemand = np.multiply(randCoeff, self.demandData.volume)

            randData = self.demandData.copy()
            randData.volume = randDemand

            pathRandData = os.path.join(self.pathTempFolder, 'od'+str(s)+'.csv')
            randData.to_csv(pathRandData, index=False)
            self.listOD.append(pathRandData)

        for indSample in range(numSample):
            optFlow = self.AssignTraffic(np.zeros(self.numEdges), indSample, objective='sys_opt')
            optCost = self.SocialCost(optFlow)
            self.optCosts.append(optCost)

    def ComputeBigH(self, toll: np.array, indSampleList: list=None):
        hList = np.zeros(self.numSample)
        indSampleList = range(self.numSample) if indSampleList is None else indSampleList

        for indSample in indSampleList:
            flow = self.AssignTraffic(toll, indSample)
            hList[indSample] = self.SocialCost(flow)

        return np.max(hList), hList, np.argmax(hList)

    def ComputePoAs(self, toll: np.array, indSampleList: list=None):
        PoAs = np.zeros(self.numSample)
        indSampleList = range(self.numSample) if indSampleList is None else indSampleList

        for indSample in indSampleList:
            flow = self.AssignTraffic(toll, indSample)
            PoAs[indSample] = self.SocialCost(flow) / self.optCosts[indSample]

        return np.max(PoAs), PoAs, np.argmax(PoAs)

    def ComputeGradient(self, toll: np.array, indSampleList: list, deltaToll=0.05):
        grad = np.zeros(self.numEdges, dtype=np.double)

        for m in range(self.numEdges):
            minusToll = copy(toll)
            plusToll = copy(toll)
            minusToll[m] = max(minusToll[m]-deltaToll, 0)
            plusToll[m] = plusToll[m] + deltaToll

            minusH, _, _ = self.ComputeBigH(minusToll, indSampleList)
            plusH, _, _ = self.ComputeBigH(plusToll, indSampleList)

            num = plusH - minusH
            den = deltaToll * 2 if minusToll[m] > 0 else deltaToll + toll[m]

            gradient = num / den
            grad[m] = gradient

        return grad

    def ComputeGradientPoA(self, toll: np.array, indSampleList: list, deltaToll=0.05):
        grad = np.zeros(self.numEdges, dtype=np.double)

        for m in range(self.numEdges):
            minusToll = copy(toll)
            plusToll = copy(toll)
            minusToll[m] = max(minusToll[m]-deltaToll, 0)
            plusToll[m] = plusToll[m] + deltaToll

            minusPoA, _, _ = self.ComputePoAs(minusToll, indSampleList)
            plusPoA, _, _ = self.ComputePoAs(plusToll, indSampleList)

            num = plusPoA - minusPoA
            den = deltaToll * 2 if minusToll[m] > 0 else deltaToll + toll[m]

            gradient = num / den
            grad[m] = gradient

        return grad

    def GreedyGradientDescent(self, initToll: np.array=None):
        maxIteration = 200
        currIteration = 0
        numToConverge = 0

        toll = np.zeros(self.numEdges) if initToll is None else initToll
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

            gamma = 0.001 / (currIteration * 2) if currIteration < 20 else 0.01 / currIteration / currIteration

            while True:
                grad = self.ComputeGradient(toll, indSampleList)
                step = grad * gamma
                maxMagGrad = np.max(np.abs(grad))
                maxMagStep = np.max(np.abs(step))
                normStep = step if np.max(np.abs(step)) < 1 else step / maxMagStep
                magNormStep = np.max(np.abs(normStep))

                tollTry = toll - normStep
                tollTry[tollTry<0] = 0

                tollTry = np.round(tollTry, decimals=2)

                H, hList, indMaxH = self.ComputeBigH(tollTry)
                if indMaxH not in indSampleList:
                    indSampleList.append(indMaxH)
                else:
                    toll = tollTry
                    break

            Hs.append(H)
            hLists = np.vstack((hLists, hList))
            tElapsed = float(time.time()-startTime)
            gammas.append(gamma)
            times.append(tElapsed)
            tolls = np.vstack((tolls, np.reshape(toll, (1, -1))))
            print('Iteration: {0:3d}, H: {1:10.1f}, Time: {2:5.1f}, Gamma: {3:8f}, MagNormStep: {4:6.3f}, dH: {5:8.1f}, MaxMagGrad: {6:8.1f} SupportSet: {7}'.format(currIteration, H, tElapsed, gamma, magNormStep, H-prevH, maxMagGrad,indSampleList))
            indSampleList.clear()
            
            if abs(prevH - H) < 500:
                if numToConverge > 5: break
                else: numToConverge += 1
            else: numToConverge = 0

            prevH = copy(H)

        return Hs, tolls, gammas, times, hLists

    def GreedyGradientDescentPoA(self, initToll: np.array=None):
        maxIteration = 200
        currIteration = 0
        numToConverge = 0

        toll = np.zeros(self.numEdges) if initToll is None else initToll
        PoA, PoAList, _ = self.ComputePoAs(toll)
        prevPoA = copy(PoA)

        PoAs = [PoA]
        PoALists = np.reshape(PoAList, (1, -1))
        gammas = []
        times = []
        tolls = np.reshape(toll, (1, -1))

        while currIteration < maxIteration:
            startTime = time.time()
            currIteration = currIteration + 1

            indSampleList = []
            PoA, PoAList, indMaxPoA = self.ComputePoAs(toll)
            indSampleList.append(indMaxPoA)

            gamma = 1000 / (currIteration * 2) if currIteration < 20 else 10000 / currIteration / currIteration

            while True:
                grad = self.ComputeGradientPoA(toll, indSampleList)
                step = grad * gamma
                maxMagGrad = np.max(np.abs(grad))
                maxMagStep = np.max(np.abs(step))
                normStep = step if np.max(np.abs(step)) < 1 else step / maxMagStep
                magNormStep = np.max(np.abs(normStep))

                tollTry = toll - normStep
                tollTry[tollTry<0] = 0

                tollTry = np.round(tollTry, decimals=2)

                PoA, PoAList, indMaxPoA = self.ComputePoAs(tollTry)
                if indMaxPoA not in indSampleList:
                    indSampleList.append(indMaxPoA)
                else:
                    toll = tollTry
                    break

            self.buffer.clear()
            PoAs.append(PoA)
            PoALists = np.vstack((PoALists, PoAList))
            tElapsed = float(time.time()-startTime)
            gammas.append(gamma)
            times.append(tElapsed)
            tolls = np.vstack((tolls, np.reshape(toll, (1, -1))))
            print('Iteration: {0:3d}, PoA: {1:10.9f}, Time: {2:5.1f}, Gamma: {3:8f}, MagNormStep: {4:6.3f}, dPoA: {5:10.9f}, MaxMagGrad: {6:8.7f} SupportSet: {7}'.format(currIteration, PoA, tElapsed, gamma, magNormStep, PoA-prevPoA, maxMagGrad,indSampleList))
            indSampleList.clear()
            
            if abs(prevPoA - PoA) < 0.001:
                if numToConverge > 10: break
                else: numToConverge += 1
            else: numToConverge = 0

            prevPoA = copy(PoA)

        return PoAs, tolls, gammas, times, PoALists
