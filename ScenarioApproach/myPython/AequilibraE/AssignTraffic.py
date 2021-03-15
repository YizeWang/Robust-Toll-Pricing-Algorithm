from aequilibrae.paths import TrafficAssignment, TrafficClass
import pandas as pd


def AssignTraffic(graph, demand, alg='bfw', maxIter=1000, gap=0.0001):

    assig = TrafficAssignment()
    assigclass = TrafficClass(graph, demand)
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
