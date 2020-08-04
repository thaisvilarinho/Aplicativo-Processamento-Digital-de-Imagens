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

    def __init__(self):
        super(JanelaMatriz, self).__init__()
        self.setWindowTitle("Elemento Estruturante")
        self.setWindowIcon(QIcon("icones/icon.jpg"))
        self.setGeometry(700, 350, 250, 150)
        self.totalLinhas = 9
        self.totalColunas = 9
        self.elemento = np.zeros((self.totalLinhas, self.totalColunas), dtype=int)
        self.setFixedSize(49 * self.totalLinhas + 48, 55 * self.totalColunas + 31)  # 9x9
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
        self.botaoEnviar.clicked.connect(self.pegarValor)

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
            print(celula.text(), celula.row(), celula.column())

    def pegarValor(self):
        for celula in self.tabela.selectedItems():
            pass





if __name__ == "__main__":
    app = QApplication(sys.argv)
    fen = JanelaMatriz()
    fen.show()
    sys.exit(app.exec_())
