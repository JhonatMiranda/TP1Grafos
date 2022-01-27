import math
arq=open("entrada.txt")
qtvertices=arq.readline()
qtvertices= int(qtvertices)
linhas=arq.readlines()
matadj=[[0 for j in range(qtvertices)]for i in range(qtvertices)]
matpes=[[0 for j in range(qtvertices)]for i in range(qtvertices)]
tamanho = 0
for i in linhas:
    posx=int(i[0])
    tamanho= tamanho + 1
    posy=int(i[2])
    peso = i.split(" ")
    peso = peso[2].replace('\n', "")
    peso = float(peso)
    matadj[posx-1][posy-1]=1
    matadj[posy-1][posx-1]=1
    matpes[posx-1][posy-1]=peso
    matpes[posy-1][posx-1]=peso
print("A ordem desse grafo é:",qtvertices)
print("O tamanho desse grafo é:",tamanho)
print("A densidade desse grafo é ε(G):",abs(tamanho)/abs(qtvertices))
print("Matriz adjascente:\n",matadj)
print("Matriz de pesos:\n",matpes)
numvertice=int(input("Digite o número do vértice para mostrar os vizinhos:"))
for i in range(qtvertices):
    for j in range(qtvertices):
        if i == (numvertice-1):
            if matadj[i][j]==1:
                print("O vértice",j+1,"é vizinho do vértice",numvertice)
numvertice=int(input("Digite o número do vértice para mostrar o grau:"))
grau=0
for i in range(qtvertices):
    for j in range(qtvertices):
        if i == (numvertice-1):
            if matadj[i][j]==1:
                grau=grau+1
print("O grau do vertice",numvertice,"é:",grau)








