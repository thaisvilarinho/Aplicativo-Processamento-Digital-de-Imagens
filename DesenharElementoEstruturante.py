# -*- coding:utf-8 -*-

import sys
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QTableWidget, QApplication, QTableWidgetItem, QGridLayout, QWidget, QVBoxLayout, \
    QPushButton, QAbstractItemView


class Pintar(QTableWidget):
    def __init__(self, parent):
        QTableWidget.__init__(self, parent)
        self.center = QPoint(0, 0)

    def paintEvent(self, event):
        # desenhar tabela
        QTableWidget.paintEvent(self, event)


class JanelaMatriz(QWidget):

    def __init__(self, totalLinhas, totalColunas):
        super(JanelaMatriz, self).__init__()
        self.setWindowTitle("Elemento Estruturante")
        self.setWindowIcon(QIcon("icones/icon.jpg"))
        self.setGeometry(700, 350, 250, 150)
        self.totalLinhas = totalLinhas
        self.totalColunas = totalColunas
        self.largura = 50 * totalLinhas
        self.altura = 50 * totalColunas
        self.elemento = np.zeros((self.totalLinhas, self.totalColunas), dtype=int)
        self.setFixedSize(self.largura + 39, self.altura + 76)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowModality(Qt.ApplicationModal)
        self.initUI()
        self.show()

    def initUI(self):
        self.criarWidgets()
        self.criarLayout()

    def criarWidgets(self):

        self.desenharMatriz()

        # Botão para capturar valor célula
        self.botaoEnviar = QPushButton("Enviar")

    def criarLayout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.tabela)
        layout.addWidget(self.botaoEnviar)
        self.setLayout(layout)

    def desenharMatriz(self):
        # Criar matriz
        self.tabela = Pintar(self)
        self.tabela.setRowCount(self.totalLinhas)
        self.tabela.setColumnCount(self.totalColunas)
        self.tabela.doubleClicked.connect(self.pintarCelula)
        self.tabela.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabela.setToolTip("Dê duplo clique para colorir a célula")

        for linha in range(0, self.totalLinhas):
            self.tabela.setRowHeight(linha, 50)

            for coluna in range(0, self.totalColunas):
                self.tabela.setColumnWidth(coluna, 50)

        # Cada célula contem uma própria tableWidgetItem para manipulação de cor
        for linhaCelula in range(0, self.totalLinhas):
            for colunaCelula in range(0, self.totalColunas):
                self.celula = QTableWidgetItem()
                self.celula.setTextAlignment(int(Qt.AlignHCenter) | int(Qt.AlignVCenter))
                self.tabela.setItem(linhaCelula, colunaCelula, self.celula)

    def pintarCelula(self):
        for celula in self.tabela.selectedItems():
            celula.setBackground(QColor(100, 100, 150))
            self.elemento[celula.row()][celula.column()] = 1





if __name__ == "__main__":
    app = QApplication(sys.argv)
    fen = JanelaMatriz()
    fen.show()
    sys.exit(app.exec_())
