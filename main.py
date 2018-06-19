from dicio import *

########################## MAIN DE TESTE
filename = input("Digite o nome do arquivo: ")
v = readCSVdicio(filename)

print(len(v))
for i in range(len(v)):
    print(v[i])
    
