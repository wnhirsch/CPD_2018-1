from unicodedata import normalize # Funcao que retorna o caractere normalizado
from rTrie import *

################################################################################
# Classe Tweet que armazena o valor do sentimento do Tweet e o Tweet
class Tweet():
    # Construtor
    def __init__(self, text = "", value = 0):
        self.text = text
        self.value = value
    # Facilita a impressão
    def __str__(self):
        return self.text + " >>> " + str(self.value)
################################################################################

# Funcao que dado o nome de um arquivo.csv retorna um vetor de classes Tweet com
# os tweets do arquivo e seus pesos
def csv2trie(inName, root):
    # Começamos criando o arquivo "Tweets.csv" para armazenar os tweets simplificados
    outFile = open("Tweets.csv", 'w')

    # Abrimos o arquivo de entrada
    with open(inName, 'r') as inFile:
        # Para cada linha do csv ele descobre o peso do tweet e armazena em um vetor
        for line in inFile:
            # Traduz a linha lida para um Tweet
            # se for peso 0
            if(line[-2] is '0'):
                # simplifica texto do tweet
                line = reduceTT(line[:-2])
                # armazena no vetor
                tweet = Tweet(line,0)
            # se for peso -1
            elif(line[-3] is '-' and line[-2] is '1'):
                line = reduceTT(line[:-3])
                tweet = Tweet(line,-1)
            # se for peso 1
            elif(line[-2] is '1'):
                line = reduceTT(line[:-2])
                tweet = Tweet(line,1)

            # Insiro o tweet na Trie
            for word in tweet.text.split():
                insertTrie(root, Word(word,tweet.value))

            # Escrevemos o tweet atual no arquivo
            outFile.write(tweet.text + "\n")

    outFile.close()
    return root

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

    # elimina todas as palavras com tamanho > 2
    words = reduced.split()
    reduced = ""
    for word in words:
        word = reduce2radical(word) ##### FUNCIONALIDADE B
        if len(word) > 2:
            # Adicionamos ao tweet reduzido, além das palavras com tamanho > 2,
            # o radical da propria palavra removendo letras desnecessarias
            reduced += word + " "
    # elimina o ultimo espaço
    reduced = reduced[:-1]

    return reduced

# Funcao que le um arquivo com Tweets, polariza e os armazena em outro arquivo
def polarizeTweet(filename, dicio):
    # Começamos criando o arquivo "TweetsPolarizados.csv" para armazenar os
    # tweets polarizados
    outFile = open("NovosTweets.csv", 'w')

    # Abrimos o arquivo de entrada
    with open(filename, 'r') as inFile:
        for line in inFile:
            # Simplificamos o tweet para facilitar os calculos
            text = reduceTT(line)
            # Calculamos a media de humor desses tweets usando o dicionario
            polarMean = 0
            for word in text.split():
                data = searchTrie(dicio, word)
                if data is not None:
                    polarMean += data.mean
            # Determinamos o humor discreto real do tweet
            if polarMean > 0.1:     # Positivo
                polarValue = 1
            elif polarMean < -0.1:  # Negativo
                polarValue = -1
            else:                   # Neutro
                polarValue = 0

            # Escrevemos o tweet atual no arquivo
            outFile.write(line.replace("\n","") + "; " + str(polarValue) + "\n")

    outFile.close()

########################### FUNCIONALIDADE B ###################################
# Funcao que dado uma palavra a reduz para o seu radical, caso já esteja reduzida
# nao a modifica
def reduce2radical(word):
    # elimina os acentos
    word = normalize('NFKD', word).encode('ASCII', 'ignore').decode('ASCII')

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

    # elimina palavras que contenham qualquer caractere que nao esteja no [a-z]
    for char in list(reduced):
        if ord(char) not in range(ord('a'),ord('z')+1):
            reduced = ""
            break

    return reduced
