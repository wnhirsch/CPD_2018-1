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
        # Para cada linha do csv ele descobre o peso do tweet e armazena no vetor
        for line in csvfile:
            idv = len(line)-2   # corrige o indice
            # se for peso 0
            if(line[idv] is '0'):
                ttVector.append(Tweet(line[:idv],0))
            # se for peso -1
            elif(line[idv-1] is '-' and line[idv] is '1'):
                ttVector.append(Tweet(line[:idv-1],-1))
            # se for peso 1
            elif(line[idv] is '1'):
                ttVector.append(Tweet(line[:idv],1))

    return ttVector

# Funcao que dado uma string (um tweet nesse contexto), simplifica da seguinte forma:
    # retira as pontuacoes
    # deixa todos os caracteres minusculos
    # elimina todas as palavras com tamanho > 2
def reduceTT(tweet):
    # deixa todos os caracteres minusculos
    tweet = tweet.lower()

    # retira as pontuacoes
    points = ['/','|','!','?','@','#','$','%','&','*',')','(','_','-','+','=','}',
         ']','[','{',':',';','.',',','>','<','^','~','\'','\"']
    reduced = ""
    for char in list(tweet):
        if char not in points:
            reduced += char

    # elimina todas as palavras com tamanho > 2
    words = reduced.split()
    reduced = ""
    for word in words:
        if len(word) > 2:
            reduced += word + " "

    return reduced
