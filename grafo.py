arq=open("entrada.txt")
qtvertices=arq.readline()
qtvertices= int(qtvertices)
linhas=arq.readlines()
matadj=[[0 for j in range(qtvertices)]for i in range(qtvertices)]
for i in linhas:
    posx=int(i[0])
    posy=int(i[2])
    matadj[posx-1][posy-1]=1
    matadj[posy-1][posx-1]=1
print(matadj)



