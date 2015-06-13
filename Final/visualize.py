import numpy as np
import pylab as pl

nodes = []
edges = []
per_graph_nodes = []
per_graph_edges = []

max_edge_mean_so_far = np.array([-1.0, -1.0], dtype=float)
for i in range (0000,10000):
    filename = '%0*d' % (4, i)
    fileext = 'graphs/%s' % filename
    with open(fileext) as f:
        for row in f:
            if row[0] == 'N':
                node_row = row.strip().split(' ')[1:]
                nodes.append(node_row)
            if row[0] == 'E':
                edge_row = row.strip().split(' ')[1:]
                edges.append(edge_row)
    f_nodes = np.mean(np.array(nodes, dtype=float), axis=0)
    f_edges = np.mean(np.array(edges, dtype=float), axis=0)
    f = f_edges[2]
    m = max_edge_mean_so_far[1]
    if f > m:
        max_edge_mean_so_far[0] = i
        max_edge_mean_so_far[1] = f
    per_graph_nodes.append(f_nodes)
    per_graph_edges.append(f_edges)
per_graph_nodes = np.vstack(per_graph_nodes)[:,3]
per_graph_edges = np.vstack(per_graph_edges)[:,2]

highest_edge_mean_index = max_edge_mean_so_far[0]

highest_edge_mean_file = '%0*d' % (4, highest_edge_mean_index)
fileext = 'graphs/%s' % highest_edge_mean_file
hem_nodes = []
hem_edges = []
with open(fileext) as f:
    for row in f:
        if row[0] == 'N':
            node_row = row.strip().split(' ')[1:]
            hem_nodes.append(node_row)
        if row[0] == 'E':
            edge_row = row.strip().split(' ')[1:]
            hem_edges.append(edge_row)

nodes = np.array(nodes, dtype=float)
edges = np.array(edges, dtype=float)

import networkx as nx

def draw_graph(hem_nodes, hem_edges):

    # create networkx graph
    G = nx.Graph()

    # add nodes
    color='green'
    for n1, n2, n3, n4 in hem_nodes:
        if n1 == '000':
            n1 = '0'
        else:
            n1 = n1.lstrip('0')
        G.add_node(n1, pos=(int(n2), int(n3)))

    # add edges
    for e1, e2, e3 in hem_edges:
        if e1 != '000':
            e1 = e1.lstrip('0')
        if e2 != '000':
            e2 = e2.lstrip('0')
        if e1 == '000':
            e1 = '0'
        if e2 == '000':
            e2 = '0'
        G.add_edge(e1, e2)

    # node size
    d = []
    for n in hem_nodes:
        d.append(int(float(n[3]) * 3 + 1)*2*300)

    # node color
    c = []
    for n in hem_nodes:
        if 0.0 <= float(n[3]) < 0.26:
            c.append('red')
        if 0.26 <= float(n[3]) < 0.50:
            c.append('green')
        if 0.50 <= float(n[3]) < 0.75:
            c.append('blue')
        if 0.76 <= float(n[3]) <= 1.00:
            c.append('black')

    # draw graph
    pos = nx.get_node_attributes(G,'pos')
    nx.draw(G, pos, node_size=d, node_color=c)

    # show graph
    pl.show()

# draw example
draw_graph(hem_nodes, hem_edges)

pl.hist(nodes, bins=100)
pl.show()

pl.hist(edges, bins=100)
pl.show()

pl.hist(per_graph_nodes, bins=100)
pl.show()

pl.hist(per_graph_edges, bins=100)
pl.show()
