from unicodedata import normalize # Funcao que retorna o caractere normalizado

################################################################################
# Classe Tweet que armazena o valor do sentimento do Tweet e o Tweet
class Tweet():
    def __init__(self, text = "", value = 0):
        self.text = text
        self.value = value

    def __str__(self):
        s = self.text + " >>> " + str(self.value) + "\n"
        return s
################################################################################

# Funcao que dado o nome de um arquivo.csv retorna um vetor de classes Tweet com
# os tweets do arquivo e seus pesos
def readCSVdicio(filename):
    ttVector = []
    with open(filename, 'r') as csvfile:
        # Para cada linha do csv ele descobre o peso do tweet e armazena em um vetor
        for line in csvfile:
            # se for peso 0
            if(line[-2] is '0'):
                # simplifica texto do tweet
                line = reduceTT(line[:-2])
                # armazena no vetor
                ttVector.append(Tweet(line,0))
            # se for peso -1
            elif(line[-3] is '-' and line[-2] is '1'):
                line = reduceTT(line[:-3])
                ttVector.append(Tweet(line,-1))
            # se for peso 1
            elif(line[-2] is '1'):
                line = reduceTT(line[:-2])
                ttVector.append(Tweet(line,1))

    return ttVector

# Funcao que dado uma string (um tweet nesse contexto), simplifica da seguinte forma:
    # retira as pontuacoes
    # deixa todos os caracteres minusculos
    # elimina todas as palavras com tamanho > 2
def reduceTT(tweet):
    # deixa todos os caracteres minusculos
    tweet = tweet.lower()

    # elimina as pontuacoes
    points = ['/','|','!','?','@','#','$','%','&','*',')','(','_','-','+','=','}',
         ']','[','{',':',';','.',',','>','<','^','~','\'','\"']
    reduced = ""
    for char in list(tweet):
        if char not in points:
            reduced += char
        else:
            reduced += ' '

    # elimina os acentos
    reduced = normalize('NFKD', reduced).encode('ASCII', 'ignore').decode('ASCII')

    # elimina todas as palavras com tamanho > 2
    words = reduced.split()
    reduced = ""
    for word in words:
        word = reduce2radical(word)
        if len(word) > 2:
            # Adicionamos ao tweet reduzido, além das palavras com tamanho > 2,
            # o radical da propria palavra removendo letras desnecessarias
            reduced += word + " "
    # elimina o ultimo espaço
    reduced = reduced[:-1]

    return reduced

# Funcao que dado uma palavra a reduz para o seu radical, caso já esteja reduzida
# nao a modifica
def reduce2radical(word):
    # elimina letras repetidas mais de 2 vezes na palavra
    lastChar = ''
    reduced = ""
    count = 0
    for char in list(word):
        if char == lastChar and count < 2:
            count += 1
        elif char != lastChar:
            count = 0
        if not (char == lastChar and count == 2):
            reduced += char
        lastChar = char

    return reduced
