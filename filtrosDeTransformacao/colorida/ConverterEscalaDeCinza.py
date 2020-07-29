# *-* coding: utf:8 -*-

import sys
import numpy as np


def receberArquivos():
    # Abrir os arquivos de entrada e de saída
    entrada = open(sys.argv[1], "r+")
    saida = open(sys.argv[2], "w+")

    linha = entrada.readline() # Tipo
    linha = entrada.readline() # Comentário
    linha = entrada.readline() # Dimensões
    dimensoes = linha.split()
    largura = int(dimensoes[0])
    altura = int(dimensoes[1])
    linha = entrada.readline() # Valor fixo
    linha = entrada.readlines()

    #converter de lista para array
    imagem = np.asarray(linha, dtype=int)
    imagem = np.reshape(imagem, (altura, largura, 3))

    gerarImagemTransformada(entrada, saida, largura, altura, imagem)


def gerarImagemTransformada(entrada, saida, largura, altura, imagem):
    # escrevendo a imagem resultado
    saida.write("P2\n")
    saida.write("#Criado por Thais\n")
    saida.write(str(largura))
    saida.write(" ")
    saida.write(str(altura))
    saida.write("\n")
    saida.write("255\n")

    # fazer conversão da imagem colorida para escala de cinza
    for i in range(len(imagem)):
        for j in range(len(imagem[1])):
            sum = 0
            for k in range(3):
                sum = sum + imagem[i][j][k]
            sum = int(sum / 3)
            sum = str(sum)
            saida.write(sum)
            saida.write("\n")

    # fechar os arquivos
    entrada.close()
    saida.close()

if __name__ == "__main__":
    receberArquivos()
