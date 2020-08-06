# -*- coding: utf-8 -*-

import sys
import numpy as np

def lerImagemEntrada():
    entrada = open(sys.argv[1], "r+")

    linha = entrada.readline()  # Tipo
    linha = entrada.readline()  # Comentário
    linha = entrada.readline()  # Dimensões da imagem
    dimensoes = linha.split()
    largura = int(dimensoes[0])
    altura = int(dimensoes[1])
    linha = entrada.readline() #Valor fixo
    linha = entrada.readlines()

    imagem = np.asarray(linha, dtype=int)
    imagem = np.reshape(imagem, (altura, largura))

    escreverImagemSaida(entrada, largura, altura, imagem)


def escreverImagemSaida(entrada, largura, altura, imagem):
    saida = open(sys.argv[2], "w+")
    saida.write("P2\n")
    saida.write("#Criado por Thais\n")
    saida.write(str(largura))
    saida.write(" ")
    saida.write(str(altura))
    saida.write("\n")
    saida.write("255\n")

    # matriz vazia
    imagemTransformada = np.zeros([altura, largura], dtype=int)
    for i in range(altura):
        for j in range(largura):
            imagemTransformada[i][j] = imagem[altura-i-1][largura-j-1]


    # escrever imagem transformada
    for i in range(len(imagemTransformada)):
        for j in range(len(imagemTransformada[1])):
            saida.write(str(imagemTransformada[i][j]))
            saida.write("\n")

    # fechar os arquivos
    entrada.close()
    saida.close()


if __name__ == "__main__":
    lerImagemEntrada()