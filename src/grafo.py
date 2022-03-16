import math
import sys
import json
from textwrap import indent
from attr import fields
import numpy as np
import networkx as nx
from platform import node
from menu import simpleMenu, pause
from collections import defaultdict
from ipython_genutils.py3compat import xrange

class bcolors:
    Preto = '\033[1;30m'
    Vermelho = '\033[1;31m'
    Verde = '\033[1;32m'
    Amarelo = '\033[1;33m'
    Azul = '\033[1;34m'
    Magenta = '\033[1;35m'
    Cyan = '\033[1;36m'
    CinzaC = '\033[1;37m'
    CinzaE = '\033[1;90m'
    VermelhoC = '\033[1;91m'
    VerdeC = '\033[1;92m'
    AmareloC = '\033[1;93m'
    AzulC = '\033[1;94m'
    MagentaC = '\033[1;95m'
    CyanC = '\033[1;96m'
    Branco = '\033[1;97m'
    Negrito = '\033[;1m'
    Inverte = '\033[;7m'
    Reset = '\033[0;0m'


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
    for i in range(1, n-1):
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

class Graph_directed():
    def __init__(self):
        self.dir_Graph = nx.DiGraph()
    def add_edge_directed(self, u, v):
        self.dir_Graph.add_edge(u, v)

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

#___________________________________________________________________________________________________#
    '''Retornar a ordem do grafo'''

    def ordem(self):
        return self.V - 1
#___________________________________________________________________________________________________#
    '''Retornar o tamanho do grafo'''

    def tamanho(self):
        tamanho = 0
        for i in range(self.V):
            aux = self.graph[i]
            while aux:
                tamanho += 1
                aux = aux.next
        return tamanho // 2
#___________________________________________________________________________________________________#
    '''Retornar a densidade ε(G) do grafo'''

    def densidade(self):
        return self.tamanho() / (self.V - 1)
#___________________________________________________________________________________________________#
    '''Retornar os vizinhos de um vértice fornecido'''
    
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
#___________________________________________________________________________________________________#
    '''Determinar o grau de um vértice fornecido'''

    def grau(self, vertice_escolhido):
        grau = 0
        for i in range(self.V):
            aux = self.graph[i]
            while aux:
                if aux.vertice == vertice_escolhido:
                    grau += 1
                aux = aux.next
        return grau
#___________________________________________________________________________________________________#
    '''Verificar se um vértice é articulação'''

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
                self.ap_util(aux.vertice, visited, ap, parent, low, disc)

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
                return index
#___________________________________________________________________________________________________#
    '''Determinar a sequência de vértices visitados na busca em largura e informar a(s)
aresta(s) que não faz(em) parte da árvore de busca em largura.'''

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
#___________________________________________________________________________________________________#
    '''Determinar o número de componentes conexas do grafo e os vértices de cada
componente'''

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
#___________________________________________________________________________________________________#
    '''Verificar se um grafo possui ciclo'''

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
#___________________________________________________________________________________________________#
    '''Determinar a árvore geradora mínima de um grafo'''

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
#___________________________________________________________________________________________________#
    '''A árvore geradora mínima deve ser escrita em um arquivo (no mesmo
formato de entrada do grafo), assim como seu peso total'''

    def DFSUtil(self, v, visited):
        visited[v] = True

        aux=self.graph[v]
        while aux:
            if visited[aux.vertice] == False:
                self.DFSUtil(aux.vertice, visited)
            aux=aux.next


    def isConnected(self):

        
        visited = [False] * (self.V)

        for i in range(self.V):
            if matpes.grau(i) > 1:
                break

        if i == self.V - 1:
            return True

        self.DFSUtil(i, visited)

        for i in range(self.V):
            if visited[i] == False and len(self.graph[i]) > 0:
                return False

        return True

#___________________________________________________________________________________________________#
    '''Verificar se um grafo é euleriano. Em caso afirmativo, determinar uma cadeia
euleriana fechada'''

    def isEulerian(self):
        if self.isConnected() == False:
            return 0
        else:
            
            odd = 0
            for i in range(self.V):
                if (matpes.grau(i)) % 2 != 0:
                    odd += 1
            if odd == 0:
                return 2
            elif odd == 2:
                return 1
            elif odd > 2:
                return 0

    

    def test(self):
        res = self.isEulerian()
        if res == 0:
            print("Grafo não é Euleriano")
        elif res == 1:
            print("Grafo tem um caminho de Euler")
        else:
            print("Grafo tem um circuito de Euler")
    #___________________________________________________________________________________________________#
    '''DSatur'''
    def DSatur(self):
        result = nx.greedy_color(self.G, strategy='DSATUR', interchange=False)
        cores = list(result.values())
        print("Numero de cores encontradas: " + str(len(np.unique(cores))))

    #___________________________________________________________________________________________________#
    '''Determinar o conjunto independente ou estável de um grafo por meio de uma
heurística gulosa'''
    def conjuntoindependente(self):
        s = []
        n=[]
        for i in range(1,self.V):
            n.append((self.grau(i),-i))
        n = sorted(n,reverse=True)
        n = [(i,-j) for (i,j) in n]
        visitado = [False for i in range (self.V)]
        k = 0
        while k < self.V-1:
            if visitado[n[k][1]]: 
                k +=1
            else:
                visitado[n[k][1]] = True
                for x in self.vizinhos(n[k][1]):
                    visitado[x] = True
                s.append(n[k][1])
        print(s)

#___________________________________________________________________________________________________#
 
def cleanFiles():
    arq1 = open("../out/saida.txt","a")
    arq1.truncate(0)
    arq1.close()

def convert_file():
    filename = input("Digite o nome do arquivo: ")

    dict1 = {}

    fields = ['vertice 1', 'vertice 2', 'peso']

    with open(filename) as fh:

        l = 1

        for line in fh:
            description = list(line.strip().split(None, 3))

            sno = 'graph'+str(l)

            i = 0
            dict2 = {}

            while i < len(fields):

                dict2[fields[i]] = description[i]
                i += 1

            dict1[sno] = dict2
            l += 1
    
    out_file = open("../data/grafo_saida.json", "w")
    json.dump(dict1, out_file, indent = 4)
    out_file.close()



#_______________________________________________MAIN____________________________________________________#

if __name__ == "__main__":

    cleanFiles()
    with open(str(sys.argv[2]), 'r') as file_input:
        V=0
        read_file = None
        if str(sys.argv[2])[8:].split(".")[1]=="txt":
            V = file_input.readline()
        else:
            read_file = json.load(file_input)
            V = read_file['data']['nodes']['length']
        
        
        matpes = Graph(int(V)+1)
        if str(sys.argv[2])[8:].split(".")[1]=="txt":
            print("Digite N para grafos nao direcionados e D para grafos direcionados")
            choice = input()
            if (choice == 'N'):
                while True:
                    try:
                        linha = file_input.readline()
                        if not linha:
                            break
                        else:
                            linha_limpa = linha.split(" ")
                            matpes.add_edge(int(linha_limpa[0]), int(
                                linha_limpa[1]), float(linha_limpa[2]))
                    except:
                        print("erro")
            else:
                graphdir = Graph_directed()
                while True:
                    try:
                        linha = file_input.readline()
                        if not linha:
                            break
                        else:
                            linha_limpa = linha.split(" ")
                            graphdir.add_edge_directed(int(linha_limpa[0]), int(
                                linha_limpa[1]))
                    except:
                        print("erro")
                #verificar se o grafo é ciclico e fazer ordenacão topologica
                if len(list(nx.simple_cycles(graphdir.dir_Graph))) == 0:
                    print(list(nx.topological_sort(graphdir.dir_Graph)))
                else:
                    print("O Grafo possui ciclo portanto não será possivel calcular a ordenacao topologica")
                
                exit(0) 
        else:
            lines = read_file['data']['edges']['_data']
            for i in range (len(lines)):
                line = lines["{}".format(i+1)]
                matpes.add_edge(int(line['from']), int(line['to']), float(line['label']))

    def option_1():
        arq = open("../out/saida.txt", "a")
        arq.write("\n--------------------------------------------------\n")
        arq.write("\nO grafo tem ordem {}\n".format(matpes.ordem()))
        arq.close()
        print("\nO grafo tem ordem {}\n".format(matpes.ordem()))
        pause()

    def option_2():
        arq = open("../out/saida.txt", "a")
        arq.write("\n--------------------------------------------------\n")
        arq.write("\nO grafo tem tamanho {}\n".format(matpes.tamanho()))
        arq.close()
        print("\nO grafo tem tamanho {}\n".format(matpes.tamanho()))
        pause()

    def option_3():
        print("Densidade do grafo: ", matpes.densidade())
        pause()

    def option_4():
        vert = int(input("Digite o valor do vertice: "))
        vet_vizinhos = []
        vet_vizinhos = matpes.vizinhos(vert)
        for i in vet_vizinhos:
            print(i)
        pause()

    def option_5():
        vert = int(input("Digite o valor do vertice: "))
        print(matpes.grau(vert))
        pause()

    def option_6():
        vet = []
        vet.append(matpes.AP())
        vert = int(input("Digite o valor do vertice: "))
        if vert in vet:
            print("Vértice escolhido é uma articulação")
        else:
            print("Vértice escolhido não é uma articulação")
        pause()

    def option_7():
        print("A sequência de vértices visitados na busca em largura é: \n")
        matriz_aresta_retorno = [[0 for y in range(int(V))] for x in range(int(V))]
        matpes.BFS(1, matriz_aresta_retorno)
        print()
        print("A(s) aresta(s) que não faz(em) parte da árvore de busca em largura são: \n")
        for i in range(int(V)):
            for j in range(int(V)):
                if matriz_aresta_retorno[i][j] == 1:
                    print(i+1, "-", j+1)
                    matriz_aresta_retorno[j][i] = 0
        pause()

    def option_8():
        print("As componentes conexas são: \n")
        print(matpes.componentes_conexas())
        pause()

    def option_9():
        if matpes.isCyclic() == True:
            print("Grafo possui ciclo")
        else:
            print("Grafo sem ciclo")

        pause()

    def option_10():
        matpes.PrimMST()
        print("O arquivo de saída foi criado com sucesso!!!")
        pause()
    
    def option_11():
        matpes.test()
        pause()
    
    def option_12():
        print("Passar o diretorio do arquivo, ex: ../data/nome.txt")
        convert_file()
        pause()

    def option_13():
        matpes.DSatur()
        pause()

    def option_14():
        matpes.conjuntoindependente()
        pause()
    
    sMenu = simpleMenu(f'{bcolors.Branco}TRABALHO GRAFOS{bcolors.Reset}')
    sMenu.spacing = [ '0','d' ]
    sMenu.menu_option_add(option_1,'Retornar a ordem do grafo')
    sMenu.menu_option_add(option_2,'Retornar o tamanho do grafo')
    sMenu.menu_option_add(option_3,'Retornar a densidade do grafo')
    sMenu.menu_option_add(option_4,'Retornar os vizinhos de um vertice fornecido')
    sMenu.menu_option_add(option_5,'Determinar o grau de um vértice fornecido')
    sMenu.menu_option_add(option_6,'Verificar se um vértice é articulação')
    sMenu.menu_option_add(option_7,'Determinar a sequência de vértices visitados na busca em largura e informar a(s) aresta(s) que não faz(em) parte da árvore de busca em largura')
    sMenu.menu_option_add(option_8,'Determinar o número de componentes conexas do grafo e os vértices de cada componente')
    sMenu.menu_option_add(option_9,'Verificar se um grafo possui ciclo')
    sMenu.menu_option_add(option_10,'Determinar a árvore geradora mínima de um grafo')
    sMenu.menu_option_add(option_11,'Verificar se um grafo é euleriano')
    sMenu.menu_option_add(option_12,'Transformar .txt em .json')
    sMenu.menu_option_add(option_13,'Determinar o número cromático de um grafo')
    sMenu.menu_option_add(option_14,'Determinar o conjunto independente ou estável de um grafo')
    sMenu.menu_start() 