import math
import sys
import numpy as np
import networkx as nx
from platform import node
from collections import defaultdict
from ipython_genutils.py3compat import xrange


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
        encontrado = False
        for i in range(self.V):
            if i == vertice_escolhido:
                encontrado = True
                aux = self.graph[i]
                while aux:
                    print("O vértice", aux.vertice, "é vizinho do vértice", i)
                    aux = aux.next

    def grau(self, vertice_escolhido):
        grau = 0
        for i in range(self.V):
            aux = self.graph[i]
            while aux:
                if aux.vertice == vertice_escolhido:
                    grau += 1
                aux = aux.next
        print("O grau do vértice", vertice_escolhido, "é", grau)



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
            if value == True: print(index, end=" ")

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
            visited =[False]*(self.V)
            for i in range(self.V):
                if visited[i] ==False:
                    if(self.isCyclicUtil
                        (i,visited,-1)) == True:
                        return True
            return False


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
                matpes.add_edge(int(linha_limpa[0]), int(linha_limpa[1]), float(linha_limpa[2]))
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
    if matpes.isCyclic() == True:
        print("Grafo com ciclo")
    else:
        print("Grafo sem ciclo")
