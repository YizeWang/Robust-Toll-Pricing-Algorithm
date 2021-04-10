import os
import subprocess
import numpy as np
import pandas as pd


class TrafficAssigner:

    def __init__(self):
        self.pathExecutable = None
        self.pathTempFolder = None
        self.maxIteration = None
        self.edgeData = None
        self.demandData = None
        self.tempEdgeData = None
        self.objective = None
        self.pathFlowData = None
        self.pathDemandData = None
        self.pathEdgeData = None

    def SetDataFolderPath(self, pathDataFolder: str) -> None:
        self.pathEdgeData = os.path.join(pathDataFolder, "edges.csv")
        self.pathDemandData = os.path.join(pathDataFolder, "od.csv")
        self.edgeData = pd.read_csv(self.pathEdgeData, delimiter=',')
        self.demandData = pd.read_csv(self.pathDemandData, delimiter=',')

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

    def AssignTraffic(self, toll: np.array) -> None:
        self.ImposeToll(toll)
        
        args = f'-n {str(self.maxIteration)} -i {self.tempEdgeData} -od {self.pathDemandData} -o {self.pathTempFolder} -obj {self.objective}'.split(' ')
        subprocess.run([self.pathExecutable] + args)
        flow = pd.read_csv(self.pathFlowData, skiprows=1, delimiter=',')

        return flow.flow.to_numpy()
