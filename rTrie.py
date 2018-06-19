import csv

class Nodo():
   def __init__(self):
       self.filhos = {}
       self.char = None
       self.valor = None


def insereTrie(nodeAtual, pal, tam):
    if(tam == len(pal)):                    # se chegou ao fim da palavra a inserir
        if(nodeAtual.valor is None):
            nodeAtual.valor = 1             # se ela não está na árvore ainda, põe 1 no valor
        else:
            nodeAtual.valor += 1            # se ela já estiver, incrementa o valor
        return nodeAtual
    charAtual = pal[tam]                    # avança ao próximo caracter da palavra
    if(charAtual not in nodeAtual.filhos):          # se nodo do caracter não estiver na árvore ainda,
        nodeAtual.filhos[charAtual] = Nodo()        # cria object (um nodo) para ele como filho do nodo atual
        nodeAtual.filhos[charAtual].char = charAtual        # e guarda seu caracter nele
    nodeAtual.filhos[charAtual] = insereTrie(nodeAtual.filhos[charAtual], pal, tam+1)   # chama o filho por recursão
    return nodeAtual


def buscaTudoTrie(nodeAtual, achaPalavra, indexNodo, csvWrite):
    if(nodeAtual is not None):
        nFilhos = len(nodeAtual.filhos)     # número de filhos
        flagIndex = 0                       # flag para nodos com 2 ou + filhos
        #print(nodeAtual.char, nFilhos)
        if(nodeAtual.char is not None):
            if(achaPalavra is None):        # inicializa vetor da palavra (no caso de estar na raiz da árvore)
                achaPalavra = []
            achaPalavra.append(nodeAtual.char)      # insere no vetor
            #print(achaPalavra)
            if(nFilhos >= 2):                                       # se tiver 2 ou + filhos,
                indexNodo = achaPalavra.index(achaPalavra[-1])      # pega o index do caracter no nodo para poder retroceder e percorrer a(s) outra(s) palavra(s)
                flagIndex = 1                                       # e seta o flag
        if(nodeAtual.valor is not None):                            # se o nodo tiver um valor, ou seja, é fim de palavra,
            palEChave = [''.join(achaPalavra), nodeAtual.valor]     # une-a com seu valor
            writeCSVfile(palEChave, csvWrite)                       # e escreve no arquivo CSV
            if(nodeAtual.filhos == {}):                             # se não tiver mais nenhuma palavra adiante (nodo não tiver filhos)
                del achaPalavra[indexNodo+1:]                       # deleta palavra até o index do caracter do nodo com 2 ou + filhos

        for filho in nodeAtual.filhos.values():                     # percorre todos os filhos do nodo
            buscaTudoTrie(filho, achaPalavra, indexNodo, csvWrite)
            nFilhos -= 1                                            # ao percorrer um filho, decrementa número de filhos
            if(nFilhos == 0 and flagIndex == 1 and achaPalavra != None and achaPalavra != []):      # após percorrer todos os filhos,
                del achaPalavra[-1]                                                                 # deleta caracter do nodo com 2 ou + filhos


def chamaGetPalavra(nodeAtual, palavra, n, csvWrite):
    quantPalavra = getPalavra(raiz, palavra, n)             # chama a função que retorna o valor da palavra
    writeCSVfile([palavra, quantPalavra], csvWrite)         # e escreve no arquivo

def getPalavra(nodeAtual, palavra, n):
    if(n == len(palavra)):                                  # se chegou ao fim da palavra
        if(nodeAtual.valor is not None):                    # e o valor existe,
            return nodeAtual.valor                          # retorna-o
        else:
            return 0                                        # se não existe, retorna 0
    chAtual = palavra[n]
    if(chAtual not in nodeAtual.filhos):                    # se caracter da palavra não está na árvore, retorna 0
        return 0
    else:                                                   # se está, chama função recursiva para percorrer seu nodo
        return getPalavra(nodeAtual.filhos[chAtual], palavra, n+1)


def getByPrefix(nodeAtual, prefix, n, csvWrite):
    #print(prefix)
    if(n == len(prefix)):                                   # se chegou ao fim do prefixo
        #print(n, prefix[-1])
        if(nodeAtual.filhos != {}):                         # e o último caracter tem filhos na árvore,
            for filho in nodeAtual.filhos.values():         # percorre árvore para cada filho e escreve-os no arquivo CSV
                buscaTudoTrie(filho, list(prefix), prefix.index(prefix[-1]), csvWrite)
        return
    chAtual = prefix[n]
    if(chAtual not in nodeAtual.filhos):                    # se caracter do prefixo não está na árvore, retorna 0
        return
    else:                                                   # se está, chama função recursiva para percorrer seu nodo
        getByPrefix(nodeAtual.filhos[chAtual], prefix, n+1, csvWrite)


def readCSVfile(fileName):                                  # lê arquivo CSV (não precisou usar)
    with open(fileName, newline='') as csvfile:
        csvRead = csv.reader(csvfile, delimiter=',')
        vetorNum = []
        for linha in csvRead:
            for i in range(len(linha)):
                vetorNum.append(int(linha[i]))
        csvfile.close()
        return vetorNum

def writeCSVfile(buffer, csvWrite):                     # escreve em arquivo CSV
        csvWrite.writerow(buffer)


raiz = Nodo()                                           # inicializa raiz
strTeste1 = 'O rato roeu a roupa do rei de roma'
strTeste2 = 'Em rapido rapto um rapido rato raptou tres ratos sem deixar rastros'
listaStr1 = strTeste1.split( )                          # separa cada palavra das strings de teste
listaStr2 = strTeste2.split( )
for palavra in listaStr1:
    raiz = insereTrie(raiz, palavra, 0)                 # e insere-as na árvore
for palavra in listaStr2:
    raiz = insereTrie(raiz, palavra, 0)

with open('saida.csv', "w", newline='') as csvfile:
    csvWrite = csv.writer(csvfile, delimiter=',')
    buscaTudoTrie(raiz, None, 0, csvWrite)              # busca todas as palavras e escreve-as no arquivo CSV

    writeCSVfile('', csvWrite)
    chamaGetPalavra(raiz, 'rato', 0, csvWrite)          # busca palavras na Trie
    chamaGetPalavra(raiz, 'rapto', 0, csvWrite)
    chamaGetPalavra(raiz, 'rapido', 0, csvWrite)
    #chamaGetPalavra(raiz, 'zebra', 0, csvWrite)
    #chamaGetPalavra(raiz, 'ra', 0, csvWrite)

    writeCSVfile('', csvWrite)
    prefixo = 'rap'
    getByPrefix(raiz, prefixo, 0, csvWrite)             # busca todas as palavras com o prefixo indicado

    csvfile.close()
