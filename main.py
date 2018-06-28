from dicioUpdateV2 import *

########################## MAIN DE TESTE

# Le o nome do arquivo do dicionario
filename = input("Digite o nome do arquivo de entrada do dicionario: ")
MainArq = filename
# Cria uma Trie para armazenar o dicionario
dicio = Trie()
# Armazena os Tweets lidos e simplificados na arvore
dicio = csv2trie(filename, dicio)

# Le o nome do arquivo com tweets
filename = input("Digite o nome do arquivo a ser polarizado: ")
# Polariza os tweets desse arquivo
polarizeTweet(filename, dicio)

# Funcionalidade B
prefix = input("Digite o prefixo que serão analisadas as variações: ")
FuncionalidadeB(prefix, dicio)

# Imprime o dicionario
dicioVector = dataInTrie(dicio)
for word in dicioVector:
    print(word)

resp = input("Deseja adicionar novo arquivo de tweets?(responda com sim ou não)")
if resp.lower() == "sim":
    novoArq = input("Digite o novo Arquivo de Tweets que serão inseridos: ")
    dicio = AdicionaNovoArq(novoArq, MainArq, dicio)