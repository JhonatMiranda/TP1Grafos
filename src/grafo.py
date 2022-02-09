import math
import sys
import networkx as nx
from platform import node
from collections import defaultdict

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
        self.G.add_edge(u, v, weight = weight)

#    def preenche_matriz(self, qt_vertices, linhas):

    def mostraordem(self, ordem):
        print("A ordem desse grafo é:", self.ordem)

    def mostratamanho(self, tamanho):
        print("O tamanho desse grafo é:", self.tamanho)

    def mostradensidade(tamanho, qtvertices):
        print("A densidade desse grafo é ε(G):",
              abs(tamanho) / abs(qtvertices))

    def mostravizinhos(matpes):
        numvertice = int(
            input("Digite o número do vértice para mostrar os vizinhos:"))
        for i in range(qtvertices):
            for j in range(qtvertices):
                if i == (numvertice - 1):
                    if matpes[i][j] != 0:
                        print("O vértice", j + 1,
                              "é vizinho do vértice", numvertice)

    def mostragrau(matpes):
        numvertice = int(
            input("Digite o número do vértice para mostrar o grau:"))
        grau = 0
        for i in range(qtvertices):
            for j in range(qtvertices):
                if i == (numvertice - 1):
                    if matpes[i][j] != 0:
                        grau = grau + 1
        print("O grau do vertice", numvertice, "é:", grau)

    def print_graph(self):
        for i in range(1, self.V):
            print("Lista de vertices adjacentes {}\n cabecalho".format(i), end="")
            temp = self.graph[i]
            while temp:
                print(" -- {} W: {} || ".format(temp.vertice, temp.weight), end="")
                temp = temp.next
            print(" \n")

#----------------------------------------------------- --------------------------------------------------#
if __name__ == "__main__":
            
    arq = open("../data/entrada.txt")
    qtvertices = arq.readline()
    qtvertices = int(qtvertices)
    matpes = Graph(qtvertices + 1)
    for i in range(qtvertices+1):
        linha = arq.readline()
        linha_limpa = linha.split(" ")
        matpes.add_edge(int(linha_limpa[0]), int(linha_limpa[1]), float(linha_limpa[2]))
    
    matpes.print_graph()
