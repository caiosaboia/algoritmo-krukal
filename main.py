import networkx as nx
import matplotlib.pyplot as plt
import random

random.seed(42) #Semente para as escolhas aleatorias
numero_nodes = random.randint(5, 9) #Aqui escolhemos de forma aletoria o numero de nodes

G = nx.Graph() #Criacao de um grafo
for i in range(numero_nodes):
    G.add_node(str(i))

#Adicionamos arestas ao nosso grafo
for i in range(numero_nodes):
    for j in range(i + 1, numero_nodes):
        if random.choice([True, False]):
            weight = random.randint(1, 10)
            G.add_edge(str(i), str(j), weight=weight)

#Criamos uma lista vazia para a geradora minima
genMin_edges = []

#Aqui criamos um dicionario que procura todos os nos do grafo G
componentes = {node: node for node in G.nodes}

#Aqui organizamos as areastas por peso
edges = sorted(G.edges(data=True), key=lambda x: x[2]['weight'])


def procuraComponente(node):
    if componentes[node] != node:
        componentes[node] = procuraComponente(componentes[node])
    return componentes[node]

#Essa def faz com possamos fazer a uniao de dois componentes
def uniao(componente1, componente2):
    root1 = procuraComponente(componente1)
    root2 = procuraComponente(componente2)
    componentes[root1] = root2

# Algoritmo de Kruskal de fato
for edge in edges:
    u, v, data = edge
    if procuraComponente(u) != procuraComponente(v):
        genMin_edges.append((u, v, data))
        uniao(u, v)

# Crie um grafo com as arestas da árvore geradora mínima
genMin = nx.Graph(genMin_edges)

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
mst_labels = {edge: genMin.get_edge_data(edge[0], edge[1])['weight'] for edge in genMin.edges}
nx.draw(genMin, pos, with_labels=True)
nx.draw_networkx_edge_labels(genMin, pos, edge_labels=mst_labels)
plt.title("Árvore Geradora Mínima")
plt.savefig("arvore geradora minima.png")
plt.show()

print("Finalizado")
