from dicio import *

########################## MAIN DE TESTE

# Le o nome do arquivo
filename = input("Digite o nome do arquivo de entrada do dicionario: ")

# Armazena os Tweets lidos e simplificados num vetor
tweetsVector = readCSVdicio(filename)

# Cria uma Trie para armazena-los criando assim um dicionario
root = Trie()
for tweet in tweetsVector:
    for word in tweet.text.split():
        insertTrie(root, Word(word,tweet.value))

# Imprime o dicionario
dicioVector = dataInTrie(root)
for word in dicioVector:
    print(word)
