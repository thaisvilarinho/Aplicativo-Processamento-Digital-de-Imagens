# *-* coding: utf:8 -*-

import sys
import numpy as np


def receberArquivos():

    # Abrir os arquivos de entrada e de saída
    entrada = open(sys.argv[1], "r+")
    saida = open(sys.argv[2], "w+")

    # Fazer o Processamento Digital de Imagens
    linha = entrada.readline() # Tipo
    linha = entrada.readline() # Comentário
    linha = entrada.readline() # Dimensões
    dimensoes = linha.split()
    linha = entrada.readline() # Valor Fixo
    dimensoes = np.array(dimensoes, dtype=int)

    linhas = entrada.readlines()
    imagem = np.array(list(linhas))
    imagem = np.reshape(imagem, [dimensoes[1], dimensoes[0], 3])
    imagem = imagem.astype(int)

    #Mediana(BoxBlur)
    kernel = np.ones((3, 3))
    kernel = np.asarray(kernel)/9
    ks = int((len(kernel) - 1) / 2)

    gerarImagemTransformada(entrada, saida, dimensoes, imagem, kernel, ks)


def gerarImagemTransformada(entrada, saida, dimensoes, imagem, kernel, ks):
    # escrevendo a imagem resultado
    saida.write('P3\n')
    saida.write('#Criado por Thais\n')
    largura = dimensoes[0]
    altura = dimensoes[1]
    saida.write(str(largura-(ks*2)))
    saida.write(' ')
    saida.write(str(altura-(ks*2)))
    saida.write('\n')
    saida.write('255\n')

    # aplicar filtro mediana na imagem
    for i in range(ks, len(imagem)-ks):
        #print((round((i*100)/(len(image)-ks))))
        for j in range(ks, len(imagem[1])-ks):
            for k in range(3):
                sum = 0
                for ki in range(len(kernel)):
                    for kj in range(len(kernel[1])):
                        sum = sum + (imagem[i - ks + ki][j - ks + kj][k] * kernel[ki][kj])
                sum = int(sum)
                sum = str(sum)
                saida.write(sum)
                saida.write("\n")

    #fechar os dois arquivos.
    entrada.close()
    saida.close()


if __name__ == "__main__":
    receberArquivos()
