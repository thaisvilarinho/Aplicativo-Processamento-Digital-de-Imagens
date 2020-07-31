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
    saida.write(largura)
    saida.write(" ")
    saida.write(altura)
    saida.write("\n")
    saida.write("255\n")
    # fator gama
    gama = int(sys.argv[3])

    # aplicar correção gama
    for i in range((len(imagem))):
        n = int(((imagem[i]/255)**gama)*255)
        n = str(n)
        saida.write(n)
        saida.write("\n")

    # fechar os dois arquivos
    entrada.close()
    saida.close()


if __name__ == "__main__":
    lerImagemEntrada()