import networkx as nx
import matplotlib.pyplot as plt
import random

# Crie um grafo inicial com nós aleatórios e arestas aleatórias
random.seed(42)
num_nodes = random.randint(5, 9)

G = nx.Graph()
for i in range(num_nodes):
    G.add_node(str(i))

# Adicione arestas aleatórias
for i in range(num_nodes):
    for j in range(i + 1, num_nodes):
        if random.choice([True, False]):
            weight = random.randint(1, 10)
            G.add_edge(str(i), str(j), weight=weight)

# Inicialize uma lista vazia para armazenar as arestas da árvore geradora mínima
mst_edges = []

# Crie um conjunto para rastrear os componentes conectados
components = {node: node for node in G.nodes}

# Ordene as arestas por peso
edges = sorted(G.edges(data=True), key=lambda x: x[2]['weight'])

# Função para encontrar o componente de um nó
def procuraComponente(node):
    if components[node] != node:
        components[node] = procuraComponente(components[node])
    return components[node]

# Função para unir dois componentes
def uniao(component1, component2):
    root1 = procuraComponente(component1)
    root2 = procuraComponente(component2)
    components[root1] = root2

# Algoritmo de Kruskal
for edge in edges:
    u, v, data = edge
    if procuraComponente(u) != procuraComponente(v):
        mst_edges.append((u, v, data))
        uniao(u, v)

# Crie um grafo com as arestas da árvore geradora mínima
mst = nx.Graph(mst_edges)

# Posição dos nós para plotagem
pos = nx.spring_layout(G)

# Desenhe o grafo original
plt.figure()
nx.draw(G, pos, with_labels=True)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels={(k[0], k[1]): v for k, v in labels.items()})
plt.title("Grafo Original")
plt.savefig("grafoOriginal.png")
plt.show()


# Desenhe a árvore geradora mínima sem rótulos de peso para arestas que não fazem parte dela
plt.figure()
mst_labels = {edge: mst.get_edge_data(edge[0], edge[1])['weight'] for edge in mst.edges}
nx.draw(mst, pos, with_labels=True)
nx.draw_networkx_edge_labels(mst, pos, edge_labels=mst_labels)
plt.title("Árvore Geradora Mínima")
plt.savefig("arvore geradora minima.png")
plt.show()

print("Finalizado")
