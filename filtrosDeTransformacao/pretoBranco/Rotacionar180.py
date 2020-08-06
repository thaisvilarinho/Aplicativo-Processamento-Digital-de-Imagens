# -*- coding: utf-8 -*-

import sys
import numpy as np


def lerImagemEntrada():
    entrada = open(sys.argv[1], "r+")

    linha = entrada.readline()  # P1
    linha = entrada.readline()  # Comentário
    linha = entrada.readline()  # Dimensões da imagem
    dimensoes = linha.split()  # Lista com as dimensões
    largura = int(dimensoes[0])
    altura = int(dimensoes[1])
    dimensoes = np.asarray(dimensoes, dtype=int)

    linhas = entrada.readlines()
    linhas = [x.strip() for x in linhas]

    stringLonga = concatenarLista(linhas)
    imagem = np.array(list(stringLonga))
    imagem = np.reshape(imagem, [dimensoes[1], dimensoes[0]])
    imagem = imagem.astype(int)

    escreverImagemSaida(entrada,largura,altura,imagem)

def concatenarLista(list):
    result = ''
    for element in list:
        result += str(element)
    return result


def escreverImagemSaida(entrada, largura, altura, imagem):
    saida = open(sys.argv[2], "w+")
    saida.write("P1\n")
    saida.write("#Criado por Thais\n")
    saida.write(str(largura))
    saida.write(" ")
    saida.write(str(altura))
    saida.write("\n")

    # rotacionar imagem
    imagemTransformada = np.zeros([altura, largura], dtype=int)
    for i in range(altura):
        for j in range(largura):
            imagemTransformada[i][j] = imagem[altura-i-1][largura-j-1]

    for linha in range(len(imagemTransformada)):
        for coluna in range(len(imagemTransformada[1])):
            saida.write(str(imagemTransformada[linha][coluna]))
            saida.write("\n")

    # fechar os arquivos
    entrada.close()
    saida.close()


if __name__ == "__main__":
    lerImagemEntrada()
