from dicioOK import *

########################## MAIN
# Le o nome do arquivo do dicionario
firstFile = input("\nDigite o nome do arquivo de tweets com polaridade: ")
print('\n')
filename = firstFile                # arquivo original dos tweets polarizados
outFile = 'TweetsOut.csv'           # arquivo de saída dos tweets simplificados
postingsFile = 'ListaPostings.csv'  # arquivo da lista de postings
# Cria uma Trie para armazenar o dicionario
dicio = Trie()
lineCount = 0                       #contador de linhas do arquivo
postings = {}                       # dicionario dos postings

while(True):
    # Armazena os Tweets lidos e simplificados na arvore
    dicioELine = csv2trie(filename, outFile, dicio, lineCount, postings)
    dicio = dicioELine[0]
    lineCount = dicioELine[1]

    # salva lista de postings em um arquivo
    with open(postingsFile, 'w', encoding="utf8") as postFile:
        for ind in postings:
            postPrint = []
            postPrint.extend([str(ind), ' -> '])
            for post in postings[ind]:
                postPrint.extend([str(post), ', '])
            postPrint[-1] = '\n'
            postFile.write(''.join(postPrint))
        postFile.close()

    # Imprime o dicionario
    dicioVector = dataInTrie(dicio)
    for word in dicioVector:
        print(word)

    # Le o nome do arquivo com tweets
    filename = input("\nDigite o nome do arquivo a ser polarizado: ")
    # Polariza os tweets desse arquivo
    polarizeTweet(filename, dicio)

    # Funcionalidade A
    searchWord = input("\nDigite a palavra para buscar os tweets onde ela se encontra: ")
    print('\n')
    funcionalidadeA(searchWord, dicio, postings, firstFile)

    # Funcionalidade B
    while(True):
        prefix = input("\nDigite o prefixo para analisar suas variações (2 ou mais letras): ")
        if(len(prefix) > 1):
            break
    print('\n')
    funcionalidadeB(prefix, dicio)

    # Pergunta se quer adicionar mais tweets
    while(True):
        resp = input("\n\nDeseja adicionar novo arquivo de tweets? (responda com sim ou nao): ")
        if(resp.lower() == "sim" or resp.lower() == "nao"):
            break
    if(resp.lower() == "nao"):
        break
    else:                   # se sim, faz append dos novos tweets no arquivo de tweets original
        filename = input("\nDigite o nome do arquivo de tweets com polaridade: ")
        print('\n')
        with open(filename, 'r', encoding="utf8") as newFile:
            with open(firstFile, 'a', encoding="utf8") as origFile:
                for line in newFile:
                    origFile.write(line)
                origFile.close()
            newFile.close()
