import math
import sys
import numpy as np
import networkx as nx
from platform import node
from collections import defaultdict
from ipython_genutils.py3compat import xrange


class Heap():

    def __init__(self):
        self.array = []
        self.size = 0
        self.pos = []

    def newMinHeapNode(self, v, dist):
        minHeapNode = [v, dist]
        return minHeapNode

    def swapMinHeapNode(self, a, b):
        t = self.array[a]
        self.array[a] = self.array[b]
        self.array[b] = t

    def minHeapify(self, idx):
        smallest = idx
        left = 2 * idx + 1
        right = 2 * idx + 2

        if left < self.size and self.array[left][1] < \
                self.array[smallest][1]:
            smallest = left

        if right < self.size and self.array[right][1] < \
                self.array[smallest][1]:
            smallest = right

        if smallest != idx:
            self.pos[self.array[smallest][0]] = idx
            self.pos[self.array[idx][0]] = smallest

            # Swap nodes
            self.swapMinHeapNode(smallest, idx)

            self.minHeapify(smallest)

    def extractMin(self):

        if self.isEmpty() == True:
            return

        root = self.array[0]

        lastNode = self.array[self.size - 1]
        self.array[0] = lastNode

        self.pos[lastNode[0]] = 0
        self.pos[root[0]] = self.size - 1

        self.size -= 1
        self.minHeapify(0)

        return root

    def isEmpty(self):
        return True if self.size == 0 else False

    def decreaseKey(self, v, dist):

        i = self.pos[v]

        self.array[i][1] = dist

        while i > 0 and self.array[i][1] < \
                self.array[(i - 1) // 2][1]:
            self.pos[self.array[i][0]] = (i - 1) / 2
            self.pos[self.array[(i - 1) // 2][0]] = i
            self.swapMinHeapNode(i, (i - 1) // 2)

            i = (i - 1) // 2

    def isInMinHeap(self, v):

        if self.pos[v] < self.size:
            return True
        return False


def printArr(parent, n, grafo):
    pesototal = 0
    vetoraux = []
    arq = open("../out/saida.txt", "w")
    arq.write("Lista de arestas da MST: \n")
    for i in range(1, n):
        vetoraux = matpes.vizinhos(i)
        if(vetoraux.index(parent[i])):
            pesototal += grafo[i].next.weight
        else:
            pesototal += grafo[i].weight
        print("% d - % d" % (parent[i], i))

        arq.write("{} - {} \n".format(parent[i], i))

    arq.write("\nPeso total: {0:.2f} \n".format(pesototal))
    print("Peso total: %.2f" % pesototal)
    arq.close()


class VerticeAdj():
    def __init__(self, vertice, weight):
        self.vertice = vertice
        self.weight = weight
        self.next = None
        self.explored = False


class Graph():
    def __init__(self, vertices):
        self.graph = defaultdict(list)
        self.V = vertices
        self.Time = 0
        self.G = nx.Graph()

    def add_edge(self, u, v, weight):
        vert = VerticeAdj(v, weight)
        vert.next = self.graph[u]
        self.graph[u] = vert

        vert = VerticeAdj(u, weight)
        vert.next = self.graph[v]
        self.graph[v] = vert

        self.G.add_node(u)
        self.G.add_node(v)
        self.G.add_edge(u, v, weight=weight)

    def ordem(self):
        return self.V - 1

    def tamanho(self):
        tamanho = 0
        for i in range(self.V):
            aux = self.graph[i]
            while aux:
                tamanho += 1
                aux = aux.next
        return tamanho // 2

    def densidade(self):
        return self.tamanho() / (self.V - 1)

    def vizinhos(self, vertice_escolhido):
        vizinhos = []
        encontrado = False
        for i in range(self.V):
            if i == vertice_escolhido:
                encontrado = True
                aux = self.graph[i]
                while aux:
                    vizinhos.append(aux.vertice)
                    aux = aux.next
        return vizinhos

    def grau(self, vertice_escolhido):
        grau = 0
        for i in range(self.V):
            aux = self.graph[i]
            while aux:
                if aux.vertice == vertice_escolhido:
                    grau += 1
                aux = aux.next
        return grau

    def ap_util(self, u, visited, ap, parent, low, disc):

        children = 0

        visited[u] = True

        disc[u] = self.Time
        low[u] = self.Time
        self.Time += 1

        aux = self.graph[u]

        while aux:

            if visited[aux.vertice] == False:
                parent[aux.vertice] = u
                children += 1
                self.APUtil(aux.vertice, visited, ap, parent, low, disc)

                low[u] = min(low[u], low[aux.vertice])

                if parent[u] == -1 and children > 1:
                    ap[u] = True

                if parent[u] != -1 and low[aux.vertice] >= disc[u]:
                    ap[u] = True

            elif aux.vertice != parent[u]:
                low[u] = min(low[u], disc[aux.vertice])
            aux = aux.next

    def AP(self):

        visited = [False] * (self.V)
        disc = [float("Inf")] * (self.V)
        low = [float("Inf")] * (self.V)
        parent = [-1] * (self.V)
        ap = [False] * (self.V)

        for i in range(self.V):
            if visited[i] == False:
                self.ap_util(i, visited, ap, parent, low, disc)

        for index, value in enumerate(ap):
            if value == True:
                print(index, end=" ")

    def unmark_all(self, marked):
        for i in xrange(0, self.V):
            temp = self.graph[i]
            marked.append(False)
            while temp:
                temp.explored = False
                temp = temp.next

    def BFS(self, s, matriz_retorno):

        marcados = []
        self.unmark_all(marcados)
        visited = [False] * (max(self.graph) + 1)

        queue = []

        queue.append(s)
        visited[s] = True

        while queue:
            s = queue.pop(0)
            print(s, end=" ")

            aux = self.graph[s]
            while aux:
                if visited[aux.vertice] == False:
                    aux.explored = True
                    queue.append(aux.vertice)
                    visited[aux.vertice] = True
                    aux_temp = self.graph[aux.vertice]
                    while aux_temp:
                        if aux_temp.vertice == s:
                            aux_temp.explored = True
                        aux_temp = aux_temp.next
                else:
                    if aux.explored == False:
                        aux.explored = True
                        aux_temp = self.graph[aux.vertice]
                        while aux_temp:
                            if aux_temp.vertice == s:
                                matriz_retorno[s - 1][aux.vertice - 1] = 1
                            aux_temp = aux_temp.next
                aux = aux.next

    def print_graph(self):
        for i in range(1, self.V):
            print("Lista de vertices adjacentes {}\n cabecalho".format(i), end="")
            temp = self.graph[i]
            while temp:
                print(" -- {} W: {} || ".format(temp.vertice, temp.weight), end="")
                temp = temp.next
            print(" \n")

    def componentes_conexas(self):
        visitados = []
        compconex = []
        for i in range(self.V):
            visitados.append(False)
        for i in range(1, self.V):
            if not visitados[i]:
                aux = []
                compconex.append(self.DFScompconexas(aux, i, visitados))
        return compconex

    def DFScompconexas(self, aux, i, visitados):
        visitados[i] = True
        aux.append(i)

        aux_graph = self.graph[i]

        while aux_graph:
            if not visitados[aux_graph.vertice]:
                aux = self.DFScompconexas(aux, aux_graph.vertice, visitados)
            aux_graph = aux_graph.next
        return aux

    def isCyclicUtil(self, v, visited, parent):
        visited[v] = True
        aux = self.graph[v]
        while aux:
            if not visited[aux.vertice]:
                if self.isCyclicUtil(aux.vertice, visited, v):
                    return True
            elif parent != aux.vertice:
                return True
            aux = aux.next
        return False

    def isCyclic(self):
        visited = [False]*(self.V)
        for i in range(self.V):
            if visited[i] == False:
                if(self.isCyclicUtil
                        (i, visited, -1)) == True:
                    return True
        return False

    def PrimMST(self):
        V = self.V

        key = []

        parent = []

        minHeap = Heap()

        for v in range(V):
            parent.append(1)
            key.append(1e7)
            minHeap.array.append(minHeap.newMinHeapNode(v, key[v]))
            minHeap.pos.append(v)

        minHeap.pos[0] = 0
        key[0] = 0
        minHeap.decreaseKey(0, key[0])

        minHeap.size = V

        while minHeap.isEmpty() == False:

            newHeapNode = minHeap.extractMin()
            u = newHeapNode[0]

            aux = self.graph[u]
            while aux:
                v = aux.vertice
                weight = aux.weight
                if minHeap.isInMinHeap(v) and weight < key[v]:
                    parent[v] = u
                    key[v] = weight
                    minHeap.decreaseKey(v, key[v])
                aux = aux.next
        printArr(parent, V, self.graph)

    # A function used by isConnected
    def DFSUtil(self, v, visited):
        # Mark the current node as visited
        visited[v] = True

        # Recur for all the vertices adjacent to this vertex
        aux=self.graph[v]
        while aux:
            if visited[aux.vertice] == False:
                self.DFSUtil(aux.vertice, visited)
            aux=aux.next

    '''Method to check if all non-zero degree vertices are
    connected. It mainly does DFS traversal starting from
    node with non-zero degree'''

    def isConnected(self):

        # Mark all the vertices as not visited
        visited = [False] * (self.V)

        #  Find a vertex with non-zero degree
        for i in range(self.V):
            if matpes.grau(i) > 1:
                break

        # If there are no edges in the graph, return true
        if i == self.V - 1:
            return True

        # Start DFS traversal from a vertex with non-zero degree
        self.DFSUtil(i, visited)

        # Check if all non-zero degree vertices are visited
        for i in range(self.V):
            if visited[i] == False and len(self.graph[i]) > 0:
                return False

        return True

    '''The function returns one of the following values
       0 --> If graph is not Eulerian
       1 --> If graph has an Euler path (Semi-Eulerian)
       2 --> If graph has an Euler Circuit (Eulerian)  '''

    def isEulerian(self):
        # Check if all non-zero degree vertices are connected
        if self.isConnected() == False:
            return 0
        else:
            # Count vertices with odd degree
            odd = 0
            for i in range(self.V):
                if (matpes.grau(i)) % 2 != 0:
                    odd += 1

            '''If odd count is 2, then semi-eulerian.
            If odd count is 0, then eulerian
            If count is more than 2, then graph is not Eulerian
            Note that odd count can never be 1 for undirected graph'''
            if odd == 0:
                return 2
            elif odd == 2:
                return 1
            elif odd > 2:
                return 0

    # Function to run test cases

    def test(self):
        res = self.isEulerian()
        if res == 0:
            print("graph is not Eulerian")
        elif res == 1:
            print("graph has a Euler path")
        else:
            print("graph has a Euler cycle")
# ----------------------------------------------------- --------------------------------------------------#
if __name__ == "__main__":

    arq = open("../data/entrada.txt")
    qtvertices = arq.readline()
    qtvertices = int(qtvertices)
    matpes = Graph(qtvertices + 1)
    while True:
        try:
            linha = arq.readline()
            if not linha:
                break
            else:
                linha_limpa = linha.split(" ")
                matpes.add_edge(int(linha_limpa[0]), int(
                    linha_limpa[1]), float(linha_limpa[2]))
        except:
            print("erro")
    # matriz_aresta_retorno = [[0 for y in range(qtvertices)] for x in range(qtvertices)]
    # matpes.BFS(1,matriz_aresta_retorno)
    # print()
    # for i in range(qtvertices):
    #     for j in range(qtvertices):
    #       if matriz_aresta_retorno[i][j] == 1:
    #           print(i+1,j+1)
    #           matriz_aresta_retorno[j][i] = 0
    # if matpes.isCyclic() == True:
    #     print("Grafo com ciclo")
    # else:
    #     print("Grafo sem ciclo")
    matpes.test()
