################################################################################
# Classe Trie que representa um nodo da uma arvore R-Trie (foco no alfabeto [a-z])
class Trie():
    # Construtor
    def __init__(self, char = 'ROOT', value = None, level = 0):
        self.char = char            # caracter do nodo
        self.value = value          # palavra (se é nodo folha)
        self.children = {}          # nodos filhos
        self.level = level          # apenas para facilitar a impressao
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
        self.string = word          # palavra do tweet
        self.value = value          # polaridade acumulada da palavra
        self.appears = 1            # número de tweets em que a palavra aparece
        self.mean = value           # polaridade média da palavra
        self.tweetAtual = 0         # flag para verificar se palavra aparece + de 1 vez no mesmo tweet
        self.indice = 0             # índice para a lista de postings
    # Facilita a impressao
    def __str__(self):
        s = str(self.indice)
        s += ") " + self.string + " -> <"
        s += str(self.mean) + "; "
        s += str(self.value) + "; "
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
def insertTrie(root, word, linhaAtual, postings):
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
            if lastId != len(word.string):
                node.children[char] = Trie(char, None, lastId)
                node = node.children[char]
    else:
        lastId = len(word.string)

    char = word.string[-1]

    # Se não tem palavras que tenham essa palavra como prefixo insere normalmente
    if char not in node.children:
        node.children[char] = Trie(char, word, lastId)
        node.children[char].value.tweetAtual = linhaAtual
        if(postings == {}):             # se é o primeiro elemento da lista de postings, adiciona-o
            node.children[char].value.indice = 0
            postings[0] = [linhaAtual]
        else:                           # se não é, a chave é a anterior somada a 1 e o posting é a linha do arquivo onde o tweet se encontra
            node.children[char].value.indice = list(postings.keys())[-1]+1
            postings[node.children[char].value.indice] = [linhaAtual]

    # Se tiver devemos tomar mais cuidado, entao testeamos se essa palavra nao
    # esta na arvore, se nao estiver apenas mudamos os dados do nodo
    elif node.children[char].value == None:
        node.children[char].value = word
        node.children[char].value.tweetAtual = linhaAtual
        node.children[char].value.indice = list(postings.keys())[-1]+1      # adiciona na lista de postings
        postings[node.children[char].value.indice] = [linhaAtual]
    # Porem caso a palavra ja esteja na arvore, apenas atualizamos as suas estatisticas
    else:
        node.children[char].value += word
        if(node.children[char].value.tweetAtual == linhaAtual):
            node.children[char].value.appears -= 1          # decrementa 'appears' em 1 se a palavra aparecer + de 1 vez no mesmo tweet
        else:
            node.children[char].value.tweetAtual = linhaAtual
            postings[node.children[char].value.indice].append(linhaAtual)   # faz append na lista de postings pois a chave da palavra já existe

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

# abaixo: funções para a funcionalidade B
# Função que, dado um prefixo, percorre Trie até o fim do prefixo e chama dataPrefix
def getByPrefix(nodeAtual, prefix, n):
    if(n == len(prefix)):                                   # se chegou ao fim do prefixo
        if(nodeAtual.children != {}):                       # e o último caracter tem filhos na árvore,
            with open('WordsPrefixo.csv', "w", encoding="utf8") as csvFile:
                dataPrefix(nodeAtual, csvFile)
                csvFile.close()
        else:
            print('Não há palavras com esse prefixo nos tweets.')
        return
    chAtual = prefix[n]
    if(chAtual not in nodeAtual.children):                    # se caracter do prefixo não está na árvore, retorna
        print('Não há palavras com esse prefixo nos tweets.')
        return
    else:                                                   # se está, chama função recursiva para percorrer seu nodo
        getByPrefix(nodeAtual.children[chAtual], prefix, n+1)

# Função que imprime palavras com mesmo prefixo e as salva em um arquivo
def dataPrefix(root, csvFile):
    if root.value != None:
        print(root.value)
        csvFile.write(str(root.value))
        csvFile.write("\n")
    # procura outras palavras recursivamente
    for char in sorted(root.children):
        dataPrefix(root.children[char], csvFile)
