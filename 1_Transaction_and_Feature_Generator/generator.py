'''
This file includes data generator.
'''

import networkx as nx
import numpy as np


def ER_generator(n=10000, p=0.001, seed=2019):
    ER = nx.DiGraph()
    ER.add_nodes_from(list(range(n)))
    edges = []
    np.random.seed(seed)

    for i in range(n):
        for j in range(n):
            if j != i:
                if np.random.rand() < p:
                    edges.append((i, j, np.random.rand()))
                if np.random.rand() < p:
                    edges.append((j, i, np.random.rand()))
        # nodes = list(range(i)) + list(range(i+1, n))
        # np.random.shuffle(nodes)
        # for e in nodes:
        #     eps = np.random.rand()
        #     if eps < p:
        #         w = np.random.rand()
        #         edges.append((i, e, w))
    ER.add_weighted_edges_from(edges)
    return ER


# original: graph, w=0.999, n_min=5, n_max=21, left=5, middle=3, right=1, omega=1
def draw_anomalies(graph, w=0.999, n_min=5, n_max=21, left=5, middle=3, right=1, omega=1):
    anomaly_graph = graph.copy()

    num_anomaly = np.random.randint(low=n_min, high=n_max)
    print("Adding " + str(num_anomaly) + " anomalies...")
    n = graph.number_of_nodes()
    nodes = np.array(range(n))
    np.random.shuffle(nodes)
    begin_index = 0

    for i in range(num_anomaly):
        print("The " + str(i+1) + "th anomaly...")
        print(begin_index)
        anomaly_type = np.random.randint(5)
        # 4: trees
        if anomaly_type == 4:
            print("Adding trees...")
            end_index = begin_index + left + middle + right
            print(end_index)
            nodes_to_add = nodes[begin_index:end_index]
            if len(nodes_to_add) > 0:
                anomaly_graph = add_trees(anomaly_graph, nodes_to_add, w, left, middle, right, omega)
            # begin_index = end_index
        else:
            size = np.random.randint(low=n_min, high=n_max)
            end_index = begin_index + size
            nodes_to_add = nodes[begin_index:end_index]
            print(end_index)
            if len(nodes_to_add) > 0:
                # 0: rings
                if anomaly_type == 0:
                    print("Adding rings...")
                    anomaly_graph = add_rings(anomaly_graph, nodes_to_add, w)
                # 1: paths
                elif anomaly_type == 1:
                    print("Adding paths...")
                    anomaly_graph = add_paths(anomaly_graph, nodes_to_add, w)
                # 2: cliques
                elif anomaly_type == 2:
                    print("Adding cliques...")
                    anomaly_graph = add_cliques(anomaly_graph, nodes_to_add, w)
                # 3: stars
                else:
                    print("Adding stars...")
                    anomaly_graph = add_stars(anomaly_graph, nodes_to_add, w)
            
        begin_index = end_index

    return anomaly_graph


def add_rings(graph, nodes_to_add, w):
    all_nodes_to_add = np.append(nodes_to_add, nodes_to_add[0])
    for j in range(len(all_nodes_to_add) - 1):
        weight = np.random.rand() * (1 - w) + w
        graph.add_weighted_edges_from([(all_nodes_to_add[j], all_nodes_to_add[j+1], weight)])
        graph.nodes[nodes_to_add[j]]["type"] = 'ring'
    
    return graph


def add_paths(graph, nodes_to_add, w):
    print(nodes_to_add)
    for j in range(len(nodes_to_add) - 1):
        weight = np.random.rand() * (1 - w) + w
        graph.add_weighted_edges_from([(nodes_to_add[j], nodes_to_add[j+1], weight)])
        graph.nodes[nodes_to_add[j]]["type"] = 'path'
    graph.nodes[nodes_to_add[-1]]["type"] = 'path'
    return graph


def add_stars(graph, nodes_to_add, w):
    center = nodes_to_add[0]
    graph.nodes[center]['type'] = 'star'
    stars = nodes_to_add[1:]
    for j in range(len(stars)):
        weight = np.random.rand() * (1 - w) + w
        eps = np.random.rand()
        if eps < 0.5:
            graph.add_weighted_edges_from([(center, stars[j], weight)])
        else:
            graph.add_weighted_edges_from([(stars[j], center, weight)])
        graph.nodes[stars[j]]['type'] = 'star'
    
    return graph


def add_cliques(graph, nodes_to_add, w):
    for j in range(len(nodes_to_add)):
        graph.nodes[nodes_to_add[j]]['type'] = 'clique'
        for k in range(len(nodes_to_add)):
            if j != k:
                weight = np.random.rand() * (1 - w) + w
                eps = np.random.rand()
                if eps < 0.5:
                    graph.add_weighted_edges_from([(nodes_to_add[j], nodes_to_add[k], weight)])
                else:
                    graph.add_weighted_edges_from([(nodes_to_add[k], nodes_to_add[j], weight)])
    
    return graph


def add_trees(graph, nodes_to_add, w, left, middle, right, omega):
    left_nodes = nodes_to_add[0:left]
    middle_nodes = nodes_to_add[left:left+middle]
    right_nodes = nodes_to_add[left+middle:left+middle+right]
    for l in left_nodes:
        graph.nodes[l]['type'] = 'tree'
        for m in middle_nodes:
            weight = np.random.rand() * (1 - w) + w
            eps = np.random.rand()
            if eps < omega:
                graph.add_weighted_edges_from([(l, m, weight)])
            else:
                graph.add_weighted_edges_from([(m, l, weight)])
    for m in middle_nodes:
        graph.nodes[m]['type'] = 'tree'
        for r in right_nodes:
            weight = np.random.rand() * (1 - w) + w
            eps = np.random.rand()
            if eps < omega:
                graph.add_weighted_edges_from([(m, r, weight)])
            else:
                graph.add_weighted_edges_from([(r, m, weight)])
    for r in right_nodes:
        graph.nodes[r]['type'] = 'tree'
    return graph


# # test
# er = ER_generator()

# er_random = draw_anomalies(er)

# nodes_to_add = [1, 10, 100, 1000, 30, 55, 77, 99, 208, 444, 1999, 4000]
# er_rings = add_rings(er, nodes_to_add, w=0.99)
# print(er_rings.get_edge_data(1, 10))
# print(er_rings.node[1999]['type'])
# er_paths = add_paths(er, nodes_to_add, w=0.99)
# print(er_paths.get_edge_data(4000, 1))
# print(er_paths.node[10]['type'])
# er_stars = add_stars(er, nodes_to_add, w=0.99)
# print(er_stars.get_edge_data(1, 30))
# print(er_stars.node[55]['type'])
# er_cliques = add_cliques(er, nodes_to_add, w=0.999)
# print(er_cliques.get_edge_data(1000, 77))
# print(er_cliques.node[444]['type'])
# er_trees = add_trees(er, nodes_to_add[0:9], w=0.999, left=5, middle=3, right=1, omega=1.0)
# print(er_trees.get_edge_data(10, 99))
# print(er_trees.node[1]['type'])
