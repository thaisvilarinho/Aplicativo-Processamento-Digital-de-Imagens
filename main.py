import sys
import subprocess
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize, QTimer

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setWindowTitle("Processamento Digital de Imagens - IFTM")
        self.setWindowIcon(QIcon("images/icon.jpg"))
        self.setGeometry(450, 150, 800, 600)
        self.initUI()
        self.show()

    def initUI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        # Criar a barra de menu
        self.menuBar = self.menuBar()

        #Criar menus
        self.menuFile = self.menuBar.addMenu("&Arquivo")
        self.menuTransformation = self.menuBar.addMenu("&Transformações")
        self.menuAbout = self.menuBar.addMenu("&Sobre")

        #Crias as actions
        self.optionOpen = self.menuFile.addAction("A&brir")
        self.optionOpen.triggered.connect(self.openFile)
        self.optionOpen.setShortcut("Ctrl+A")

        self.menuFile.addSeparator()
        self.optionClose = self.menuFile.addAction("F&echar")
        self.optionClose.setShortcut("Ctrl+X")
        self.optionClose.triggered.connect(self.close)

        self.correcaoGama = self.menuTransformation.addAction("Filtro Fator &Gama")
        self.correcaoGama.setShortcut("Ctrl+Shift+G")
        self.correcaoGama.triggered.connect(self.transformation)
        self.correcaoGama.setCheckable(True)
        self.correcaoGama.setChecked(False)

        self.filtroGaussiano = self.menuTransformation.addAction("Filtro Ga&ussiano")
        self.filtroGaussiano.setShortcut("Ctrl+Shift+U")
        self.filtroGaussiano.triggered.connect(self.transformation)
        self.filtroGaussiano.setCheckable(True)
        self.filtroGaussiano.setChecked(False)

        self.filtroMediana = self.menuTransformation.addAction("Filtro &Mediana")
        self.filtroMediana.setShortcut("Ctrl+Shift+M")
        self.filtroMediana.triggered.connect(self.transformation)
        self.filtroMediana.setCheckable(True)
        self.filtroMediana.setChecked(False)

        self.optionAbout = self.menuAbout.addAction("S&obre o Aplicativo")
        self.optionAbout.triggered.connect(self.showInformation)
        self.optionInfoImage = self.menuAbout.addAction("&Informacões da Imagem")
        self.optionInfoImage.triggered.connect(self.showInformation)

        # Criar barra de status
        self.statusBar = self.statusBar()
        self.statusBar.showMessage("Seja bem-vindo(a) ao meu aplicativo", 3000)

        # Criando a barra de progresso
        self.progressBar = QProgressBar()
        #self.progressBar.setAlignment(QtCore.Qt.AlignCenter)

        # Timer
        self.timer = QTimer()
        #self.timer.setInterval(1000)

        # Criando Labels
        self.progressBarLabel = QLabel("Progresso da Transformação...")

        # Criando imagens
        self.origImage = QLabel()
        self.dirOrigImage = 'images/Lucca_Prometheus.ppm'
        self.origImage.setPixmap(QPixmap(self.dirOrigImage))
        #self.pixmapOrigImage = self.pixmapOrigImage.scaled(250, 250, QtCore.Qt.KeepAspectRatio)
        self.origImage.setAlignment(QtCore.Qt.AlignCenter)

    def layouts(self):
        # Criando janela
        self.window = QWidget(self)
        self.setCentralWidget(self.window)

        # Criando os layouts
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QHBoxLayout()

        # Adicionando os widgets
        self.topLayout.addWidget(self.origImage)
        self.bottomLayout.addWidget(self.progressBarLabel)
        self.bottomLayout.addWidget(self.progressBar)

        # Adicionando layouts filhos na janela principal
        self.mainLayout.addLayout(self.topLayout, 80)
        self.mainLayout.addLayout(self.bottomLayout, 20)

        self.window.setLayout(self.mainLayout)


    def showInformation(self):

        self.option = self.sender().text()
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Information)

        if self.option == "S&obre o Aplicativo":

            self.msg.setWindowTitle("Sobre o Aplicativo")
            self.msg.setText("Desenvolvido por Thaís Aparecida Vilarinho de Jesus")
            self.msg.setInformativeText("Capinópolis-MG, 24 de Junho de 2020")
            self.descricao = "Este aplicativo realiza as seguintes Transformações: " \
                         "Fator Gama com correção 1.8, Filtro Gaussiano " \
                         "e Filtro Mediana em Imagens coloridas"
            self.msg.setDetailedText(self.descricao)

        if self.option == "&Informacões da Imagem":
            self.msg.setWindowTitle("Informações da Imagem")

            # Informações da Imagem
            self.parts = self.dirOrigImage.rpartition('/')
            self.nomeimagem = self.parts[2]
            self.leituraimagem = open(self.dirOrigImage, "r+")
            self.tipoimagem = self.leituraimagem.readline()  # P3
            self.comentarioimagem = self.leituraimagem.readline()  # Comentário
            self.dimensoesimagem = self.leituraimagem.readline()  # Dimensões
            self.dimensoesimagem = self.dimensoesimagem.split()
            self.larguraimagem = self.dimensoesimagem[0]
            self.alturaimagem = self.dimensoesimagem[1]

            self.msg.setText("Arquivo: " + self.nomeimagem + "\n" + "Tipo: " + self.tipoimagem + "Comentário: " \
                             + self.comentarioimagem + "Largura: " + self.larguraimagem\
                             + "\n" + "Altura: " + self.alturaimagem)

        self.msg.exec_() # exibir a caixa de mensagem/diálogo


    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, caption="Open Image",
                                                            directory=QtCore.QDir.currentPath(),
                                                            filter='All files(*.*);;Imagens(*.ppm; *.pgm; *.pbm)',
                                                            initialFilter='Imagens(*.ppm; *.pgm; *.pbm)')
        #print(fileName)
        if fileName != '':
            self.dirOrigImage = fileName
            self.origImage.setPixmap(QPixmap(self.dirOrigImage))

    def transformation(self):
        self.step = 0
        self.progressBar.setValue(self.step)
        self.inputImage = self.dirOrigImage
        self.action = self.sender().text()
        self.nameTransformation = ''

        if self.action == "Filtro Fator &Gama":
            self.script = 'filtrosDeTransformacao/CorrecaoGama.py'
            self.resultImage = 'images/imagem_com_filtro_fatorGama1_8.ppm'
            self.nameTransformation = "Transformação Fator Gama (Correção 1.8)"

        if self.action == "Filtro Ga&ussiano":
            self.script = 'filtrosDeTransformacao/Gaussiano.py'
            self.resultImage = 'images/imagem_com_filtro_gaussiano.ppm'
            self.nameTransformation = "Transformação Filtro Gaussiano"

        if self.action == "Filtro &Mediana":
            self.script = 'filtrosDeTransformacao/Mediana.py'
            self.resultImage = 'images/imagem_com_filtro_mediana.ppm'
            self.nameTransformation = "Transformação Filtro Mediana"

        self.program = 'python ' + self.script + ' \"' + self.inputImage + '\" ' + self.resultImage
        self.executeTransformation = subprocess.run(self.program, shell=True)

        while self.step < 100:
            if self.executeTransformation is not None:
                self.step += 0.001
                self.progressBar.setValue(int(self.step))
            else:
                break

        self.dirTransfImage = self.resultImage
        self.origImage.setPixmap(QPixmap(self.dirTransfImage))

        self.statusBar.showMessage(self.nameTransformation + " finalizada", 5000)

def main():
    app = QApplication(sys.argv)
    win = MyWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
