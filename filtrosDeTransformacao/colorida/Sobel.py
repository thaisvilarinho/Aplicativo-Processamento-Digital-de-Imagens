# *-* coding: utf:8 -*-

import sys
import numpy as np
import math

def receberArquivos():

    # Abrir os arquivos de entrada e de saída
    entrada = open(sys.argv[1], "r+")
    saida = open(sys.argv[2], "w+")

    # Fazer o Processamento Digital de Imagens
    linha = entrada.readline()  # Tipo
    linha = entrada.readline()  # Comentário
    linha = entrada.readline()  # Dimensões
    dimensoes = linha.split()
    linha = entrada.readline()  # Valor Fixo
    dimensoes = np.array(dimensoes, dtype=int)

    linhas = entrada.readlines()
    imagem = np.array(list(linhas))
    imagem = np.reshape(imagem, [dimensoes[1], dimensoes[0], 3])
    imagem = imagem.astype(int)

    #Matrizes filtro Sobel
    kernelx = [[-1, 0, 1], [2, 0, -2], [1, 0, -1]]
    kernelx = np.asarray(kernelx)
    kernely = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]
    kernely = np.asarray(kernely)
    ks = int((len(kernelx)-1)/2)
    threshold = 200

    gerarImagemTransformada(entrada, saida, dimensoes, imagem, kernelx, kernely, ks, threshold)


def gerarImagemTransformada(entrada, saida, dimensoes, imagem, kernelx, kernely, ks, threshold):

    # escrevendo a imagem resultado
    saida.write('P3\n')
    saida.write('#Criado por Thais\n')
    largura = dimensoes[0]
    altura = dimensoes[1]
    saida.write(str(largura - (ks * 2)))
    saida.write(' ')
    saida.write(str(altura - (ks * 2)))
    saida.write('\n')
    saida.write('255\n')

    #fazer a transformação
    for i in range(ks, len(imagem)-ks):
        for j in range(ks, len(imagem[1])-ks):
            for k in range(3):
                sumx = 0
                sumy = 0
                for ki in range(len(kernelx)):
                    for kj in range(len(kernelx[1])):
                        sumx = sumx + (imagem[i-ks+ki][j-ks+kj][k]*kernelx[ki][kj])
                        sumy = sumy + (imagem[i-ks+ki][j-ks+kj][k]*kernely[ki][kj])
                sumxy = math.sqrt((sumx**2)+(sumy**2))
                #Threshold
                sum = max(sumxy, threshold)
                sum = int(sum) if sum != threshold else 0
                sum = str(sum)
                saida.write(sum)
                saida.write("\n")

    #fechar os arquivos
    entrada.close()
    saida.close()


if __name__ == "__main__":
    receberArquivos()
