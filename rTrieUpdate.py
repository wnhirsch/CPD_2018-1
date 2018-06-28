
################################################################################
# Classe Trie que representa um nodo da uma arvore R-Trie (foco no alfabeto [a-z])
class Trie():
    # Construtor
    def __init__(self, char = 'ROOT', value = None, level = 0):
        self.char = char
        self.value = value
        self.children = {}
        self.indice = 0
        self.level = level # apenas para facilitar a impressao
    # Facilita a impressao
    def __str__(self):
        s = "_"*self.level + self.char + " >>> " + str(self.value)
        for char in sorted(self.children):
            s += "\n" + str(self.children[char])
        return s
################################################################################

################################################################################
# Classe Word que armazena uma palavra e a sua pontuacao de humor
class Word():
    # Construtor
    def __init__(self, word, value):
        self.string = word
        self.value = value
        self.appears = 1
        self.mean = value
        self.tweetAtual = 0
    # Facilita a impressao
    def __str__(self):
        s = self.string + "<"
        s += str(self.mean) + ";"
        s += str(self.value) + ";"
        s += str(self.appears) + ">"
        return s
    # Dado duas palavras que sejam iguais, a soma delas retorna a soma de suas
    # estatisticas
    def __add__(self, other):
        if self.string == other.string:
            self.appears += other.appears
            self.value += other.value
            self.mean = self.value / self.appears
        return self
################################################################################

# Funcao que dada uma Trie insere uma palavra nela (adicionando ou nao varios nodos)
def insertTrie(root, word, linhaAtual):
    node = root
    lastId = None
    # Entra na arvore ate encontrar um filho vazio ou o lugar certo
    for id, char in enumerate(word.string[:-1]):
        if char in node.children:
            node = node.children[char]
        else:
            lastId = id
            break

    # Se nao encontrou entao insere os nodos que precisa
    if lastId != None:
        for char in list(word.string[lastId:]):
            lastId += 1
            node.children[char] = Trie(char, None, lastId)
            if lastId != len(word.string):
                node = node.children[char]
    else:
        lastId = len(word.string)

    char = word.string[-1]

    # Se não tem palavras que tenham essa palavra como prefixo insere normalmente
    if char not in node.children:
        node.children[char] = Trie(char, word, lastId)
        node.children[char].value.tweetAtual = linhaAtual
    # Se tiver devemos tomar mais cuidado, entao testeamos se essa palavra nao
    # esta na arvore, se nao estiver apenas mudamos os dados do nodo
    elif node.children[char].value == None:
        node.children[char].value = word
        node.children[char].value.tweetAtual = linhaAtual
    # Porem caso a palavra ja esteja na arvore, apenas atualizamos as suas estatisticas
    else:
        node.children[char].value += word
        if(node.children[char].value.tweetAtual == linhaAtual):
            node.children[char].value.appears -= 1
        else:
            node.children[char].value.tweetAtual = linhaAtual

# Funcao que encontra uma palavra na Trie e retorna os seu valor
def searchTrie(root, word):
    node = root
    # Entra na arvore ate encontrar a string
    for char in list(word):
        if char in node.children:
            node = node.children[char]
        else:
            return None # se nao encontrar retorna Nulo
    return node.value

# Função que retorna um vetor com todos os dados (palavras) contidos na Trie
def dataInTrie(root):
    vector = []
    # se achou algum palavra reconhecida pelo dicionario armazena no vetor
    if root.value != None:
        vector.append(root.value)
    # procura outras palavras recursivamente
    for char in sorted(root.children):
        vector += dataInTrie(root.children[char])
    # retorna um vetor com todas as palavras encontradas
    return vector

def writeCSVfile(buffer, csvWrite):  # escreve em arquivo CSV
    csvWrite.writerow(buffer)

def buscaTudoTrie(nodeAtual, achaPalavra, indexNodo, csvWrite):
    if(nodeAtual is not None):
        nFilhos = len(nodeAtual.children)     # número de filhos
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
        if(nodeAtual.value is not None):                            # se o nodo tiver um valor, ou seja, é fim de palavra,
            palavra = [''.join(achaPalavra)]
            writeCSVfile(palavra, csvWrite)                             # escreve a palavra no arquivo CSV
            if(nodeAtual.children == {}):                           # se não tiver mais nenhuma palavra adiante (nodo não tiver filhos)
                del achaPalavra[indexNodo+1:]                       # deleta palavra até o index do caracter do nodo com 2 ou + filhos

        for filho in nodeAtual.children.values():                     # percorre todos os filhos do nodo
            buscaTudoTrie(filho, achaPalavra, indexNodo, csvWrite)
            nFilhos -= 1                                            # ao percorrer um filho, decrementa número de filhos
            if(nFilhos == 0 and flagIndex == 1 and achaPalavra != None and achaPalavra != []):      # após percorrer todos os filhos,
                del achaPalavra[-1]

def getByPrefix(nodeAtual, prefix, n, csvWrite):
    #print(prefix)
    if(n == len(prefix)):                                   # se chegou ao fim do prefixo
        #print(n, prefix[-1])
        if(nodeAtual.children != {}):                         # e o último caracter tem filhos na árvore,
            for filho in nodeAtual.children.values():         # percorre árvore para cada filho e escreve-os no arquivo CSV
                buscaTudoTrie(filho, list(prefix), prefix.index(prefix[-1]), csvWrite)
        return
    chAtual = prefix[n]
    if(chAtual not in nodeAtual.children):                    # se caracter do prefixo não está na árvore, retorna 0
        return
    else:                                                   # se está, chama função recursiva para percorrer seu nodo
        getByPrefix(nodeAtual.children[chAtual], prefix, n+1, csvWrite)