import sys
import subprocess
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer

imagemResultado = 'imagemTransformada'

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
        self.barraMenu = self.menuBar()

        # Criar menus
        self.menuArquivo = self.barraMenu.addMenu("&Arquivo")
        self.menuTransformacao = self.barraMenu.addMenu("&Transformações")
        self.menuSobre = self.barraMenu.addMenu("So&bre")

        # Crias as actions
        self.opcaoAbrir = self.menuArquivo.addAction("A&brir")
        self.opcaoAbrir.triggered.connect(self.abrirArquivo)
        self.opcaoAbrir.setShortcut("Ctrl+A")

        self.opcaoSalvarComo = self.menuArquivo.addAction("&Salvar como")
        self.opcaoSalvarComo.triggered.connect(self.salvarAquivoComo)
        self.opcaoSalvarComo.setShortcut("Ctrl+S")

        self.menuArquivo.addSeparator()
        self.opcaoFechar = self.menuArquivo.addAction("F&echar")
        self.opcaoFechar.setShortcut("Ctrl+X")
        self.opcaoFechar.triggered.connect(self.close)

        self.correcaoGama = self.menuTransformacao.addAction("Filtro Fator &Gama")
        self.correcaoGama.setShortcut("Ctrl+Shift+G")
        self.correcaoGama.triggered.connect(self.transformacao)
        self.correcaoGama.setCheckable(True)
        self.correcaoGama.setChecked(False)

        self.filtroGaussiano = self.menuTransformacao.addAction("Filtro Ga&ussiano")
        self.filtroGaussiano.setShortcut("Ctrl+Shift+U")
        self.filtroGaussiano.triggered.connect(self.transformacao)
        self.filtroGaussiano.setCheckable(True)
        self.filtroGaussiano.setChecked(False)

        self.filtroMediana = self.menuTransformacao.addAction("Filtro &Mediana")
        self.filtroMediana.setShortcut("Ctrl+Shift+M")
        self.filtroMediana.triggered.connect(self.transformacao)
        self.filtroMediana.setCheckable(True)
        self.filtroMediana.setChecked(False)

        self.filtroNegativo = self.menuTransformacao.addAction("Filtro &Negativo")
        self.filtroNegativo.setShortcut("Ctrl+Shift+N")
        self.filtroNegativo.triggered.connect(self.transformacao)
        self.filtroNegativo.setCheckable(True)
        self.filtroNegativo.setChecked(False)

        self.opcaoSobre = self.menuSobre.addAction("S&obre o Aplicativo")
        self.opcaoSobre.triggered.connect(self.mostrarInformacoesImagem)
        self.opcaoInfoImagem = self.menuSobre.addAction("&Informacões da Imagem")
        self.opcaoInfoImagem.triggered.connect(self.mostrarInformacoesImagem)

        # Criar barra de status
        self.barraStatus = self.statusBar()
        self.barraStatus.showMessage("Seja bem-vindo(a) ao meu aplicativo", 3000)

        # Criando a barra de progresso
        self.barraProgresso = QProgressBar()

        # Timer
        self.timer = QTimer()
        # self.timer.setInterval(1000)

        # Criando Labels
        self.barraProgressoTexto = QLabel("Progresso da Transformação...")

        # Criando imagens
        self.imagemOriginal = QLabel()
        self.endImagemOriginal = ''

    def layouts(self):
        # Criando janela
        self.janelaAreaVisualizacao = QWidget(self)
        self.setCentralWidget(self.janelaAreaVisualizacao)

        # Criando os layouts
        self.layoutPrincipal = QVBoxLayout()
        self.layoutTopo = QVBoxLayout()
        self.layoutRodape = QHBoxLayout()

        # Adicionando os widgets
        self.layoutTopo.addWidget(self.imagemOriginal)
        self.layoutRodape.addWidget(self.barraProgressoTexto)
        self.layoutRodape.addWidget(self.barraProgresso)

        # Adicionando layouts filhos na janela principal
        self.layoutPrincipal.addLayout(self.layoutTopo, 80)
        self.layoutPrincipal.addLayout(self.layoutRodape, 20)

        self.janelaAreaVisualizacao.setLayout(self.layoutPrincipal)

    def informacoesDaImagem(self):
        try:
            # Informações da Imagem
            self.parts = self.endImagemOriginal.rpartition('/')
            self.nomeimagem = self.parts[2]
            self.teste = self.imagem.rpartition('.')
            self.leituraimagem = open(self.endImagemOriginal, "r+")
            self.tipoimagem = self.leituraimagem.readline()  # P3
            self.comentarioimagem = self.leituraimagem.readline()  # Comentário
            self.dimensoesimagem = self.leituraimagem.readline()  # Dimensões
            self.dimensoesimagem = self.dimensoesimagem.split()
            self.larguraimagem = self.dimensoesimagem[0]
            self.alturaimagem = self.dimensoesimagem[1]
        except:
            pass

    def mostrarInformacoesImagem(self):

        self.opcaoEscolhida = self.sender().text()
        self.caixaMensagem = QMessageBox()
        self.caixaMensagem.setIcon(QMessageBox.Information)

        if self.opcaoEscolhida == "S&obre o Aplicativo":
            self.caixaMensagem.setWindowTitle("Sobre o Aplicativo")
            self.caixaMensagem.setText("Desenvolvido por Thaís Aparecida Vilarinho de Jesus")
            self.caixaMensagem.setInformativeText("Capinópolis-MG, 24 de Junho de 2020")
            self.descricao = "Este aplicativo realiza as seguintes Transformações em imagens com extensão" \
                             " ppm, pgm e pbm: Negativo; Correção gamma; Transformação logarítmica; " \
                             "Filtro Sharpen; Filtro mediana (Box blur); Filtro Gaussiano (3x3, 5x5, 7x7); " \
                             "Detecção de bordas com Filtro de Sobel; " \
                             "Transformações espaciais para detecção de bordas com filtros; " \
                             "Conversão imagem colorida para escala de cinza; " \
                             "Conversão imagem colorida para preto e branco; " \
                             "Separação das camadas R, G e B; Erosão; Dilatação; Abertura e Fechamento"
            self.caixaMensagem.setDetailedText(self.descricao)
            self.caixaMensagem.exec_()

        if self.opcaoEscolhida == "&Informacões da Imagem":
            if self.endImagemOriginal != '':
                self.caixaMensagem.setWindowTitle("Informações da Imagem")

                self.informacoesDaImagem()
                print(self.teste)

                self.caixaMensagem.setText("Arquivo: " + self.nomeimagem + "\n" + "Tipo: " + self.tipoimagem + "Comentário: " \
                                           + self.comentarioimagem + "Largura: " + self.larguraimagem \
                                           + "\n" + "Altura: " + self.alturaimagem)

                self.caixaMensagem.exec_()

    def salvarAquivoComo(self):
        global imagemResultado

        imagemSalvaComo, _ = QFileDialog.getSaveFileName(self, caption='Salvar como')
        #print("NewFileName: " + imagemSalvaComo)
        if imagemSalvaComo != '':
            imagemResultado = imagemSalvaComo

    def abrirArquivo(self):
        arquivoImagem, _ = QFileDialog.getOpenFileName(self, caption="Open Image",
                                                  directory=QtCore.QDir.currentPath(),
                                                  filter='All files(*.*);;Imagens(*.ppm; *.pgm; *.pbm)',
                                                  initialFilter='Imagens(*.ppm; *.pgm; *.pbm)')
        #print("FileName: " + arquivoImagem)
        if arquivoImagem != '':
            self.endImagemOriginal = arquivoImagem
            self.OrigImagePixmap = QPixmap(self.endImagemOriginal)
            self.exibirImagem()

    def exibirImagem(self):
        if self.OrigImagePixmap.width() > 800 or self.OrigImagePixmap.height() > 600:
            self.OrigImagePixmap = self.OrigImagePixmap.scaled(800, 600, QtCore.Qt.KeepAspectRatio,
                                                               QtCore.Qt.SmoothTransformation)

        self.imagemOriginal.setPixmap(self.OrigImagePixmap)
        self.imagemOriginal.setAlignment(QtCore.Qt.AlignCenter)

    def transformacao(self):

        global imagemResultado
        self.step = 0
        self.barraProgresso.setValue(self.step)
        self.inputImage = self.endImagemOriginal
        self.action = self.sender().text()

        try:
            if self.action == "Filtro Fator &Gama":
                self.script = 'filtrosDeTransformacao/CorrecaoGama.py'

            if self.action == "Filtro Ga&ussiano":
                self.script = 'filtrosDeTransformacao/Gaussiano.py'

            if self.action == "Filtro &Mediana":
                self.script = 'filtrosDeTransformacao/Mediana.py'

            if self.action == "Filtro &Negativo":
                if self.tipoimagem == 'P3':
                    self.script = 'filtrosDeTransformacao/ColoridaNegativo.py'
                elif self.tipoimagem == 'P2':
                    self.script = 'filtrosDeTransformacao/EscalaCinzaNegativo.py'

            self.program = 'python ' + self.script + ' \"' + self.inputImage + '\" ' + imagemResultado
            self.executeTransformation = subprocess.run(self.program, shell=True)

            while self.step < 100:
                if self.executeTransformation is not None:
                    self.step += 0.001
                    self.barraProgresso.setValue(int(self.step))
                else:
                    break

            self.dirTransfImage = imagemResultado
            self.OrigImagePixmap = QPixmap(self.dirTransfImage)
            self.exibirImagem()

            self.barraStatus.showMessage("Aplicação " + self.action.replace("&", "") + " finalizada", 5000)
        except:
            pass


def main():
    app = QApplication(sys.argv)
    win = MyWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
