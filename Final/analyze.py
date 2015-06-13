import numpy as np

nodes = []
edges = []

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

nodes = np.array(nodes, dtype=float)
edges = np.array(edges, dtype=float)

nodes_max = np.max(nodes[:,3], axis=0)
edges_max = np.max(edges[:,2], axis=0)

print nodes_max
print edges_max

nodes_min = np.min(nodes[:,3], axis=0)
edges_min = np.min(edges[:,2], axis=0)

print nodes_min
print edges_min

nodes_mean = np.mean(nodes[:,3], axis=0)
edges_mean = np.mean(edges[:,2], axis=0)

print nodes_mean
print edges_mean

nodes_std = np.std(nodes[:,3], axis=0)
edges_std = np.std(edges[:,2], axis=0)

print nodes_std
print edges_std
