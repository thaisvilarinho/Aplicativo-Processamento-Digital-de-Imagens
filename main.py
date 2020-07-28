import sys
import os
import shutil
import subprocess
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
from win32api import GetSystemMetrics

porcentagemProgresso = 0
imagemResultado = 'images/imagemTransformada'
extensaoImagemResultado = '.ppm'
listaFiltrosUsados = []
listaFiltrosColoridaCinza = []

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setWindowTitle("Processamento Digital de Imagens - IFTM")
        self.setWindowIcon(QIcon("images/icon.jpg"))
        self.setGeometry(450, 150, 800, 600)
        self.initUI()
        self.show()

    def initUI(self):
        self.criarWidgets()
        self.gerarLayouts()

    def criarWidgets(self):
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

        self.opcaoRecente = self.menuArquivo.addMenu("Abrir &Recente")
        self.abrirRecente = self.opcaoRecente.addAction("arquivos...")
        self.abrirRecente.setDisabled(True)

        self.opcaoSalvarComo = self.menuArquivo.addAction("&Salvar como")
        self.opcaoSalvarComo.triggered.connect(self.salvarAquivoComo)
        self.opcaoSalvarComo.setShortcut("Ctrl+S")
        self.opcaoSalvarComo.setDisabled(True)

        self.menuArquivo.addSeparator()
        self.opcaoFechar = self.menuArquivo.addAction("F&echar")
        self.opcaoFechar.setShortcut("Ctrl+X")
        self.opcaoFechar.triggered.connect(self.close)

        self.criarFiltros()

        self.opcaoSobre = self.menuSobre.addAction("S&obre o Aplicativo")
        self.opcaoSobre.triggered.connect(self.mostrarInformacoesSobre)
        self.opcaoInfoImagem = self.menuSobre.addAction("&Informacões da Imagem")
        self.opcaoInfoImagem.triggered.connect(self.mostrarInformacoesSobre)
        self.opcaoInfoImagem.setVisible(False)

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
        self.endImagemResultado = ''

    def criarFiltros(self):
        global listaFiltrosColoridaCinza

        self.correcaoGama = self.menuTransformacao.addAction("Filtro Fator &Gama")
        self.correcaoGama.setShortcut("Ctrl+Shift+G")
        self.correcaoGama.triggered.connect(self.transformarImagem)
        self.correcaoGama.setDisabled(True)
        self.correcaoGama.setCheckable(True)
        self.correcaoGama.setChecked(False)

        self.filtroGaussiano = self.menuTransformacao.addAction("Filtro Ga&ussiano")
        self.filtroGaussiano.setShortcut("Ctrl+Shift+U")
        self.filtroGaussiano.triggered.connect(self.transformarImagem)
        self.filtroGaussiano.setDisabled(True)
        self.filtroGaussiano.setCheckable(True)
        self.filtroGaussiano.setChecked(False)

        self.filtroMediana = self.menuTransformacao.addAction("Filtro &Mediana")
        self.filtroMediana.setShortcut("Ctrl+Shift+M")
        self.filtroMediana.triggered.connect(self.transformarImagem)
        self.filtroMediana.setDisabled(True)
        self.filtroMediana.setCheckable(True)
        self.filtroMediana.setChecked(False)

        self.filtroNegativo = self.menuTransformacao.addAction("Filtro &Negativo")
        self.filtroNegativo.setShortcut("Ctrl+Shift+N")
        self.filtroNegativo.triggered.connect(self.transformarImagem)
        self.filtroNegativo.setDisabled(True)
        self.filtroNegativo.setCheckable(True)
        self.filtroNegativo.setChecked(False)

        self.transformacaoLogaritmica = self.menuTransformacao.addAction("Transformação &Logarítmica")
        self.transformacaoLogaritmica.setShortcut("Ctrl+Shift+L")
        self.transformacaoLogaritmica.triggered.connect(self.transformarImagem)
        self.transformacaoLogaritmica.setDisabled(True)
        self.transformacaoLogaritmica.setCheckable(True)
        self.transformacaoLogaritmica.setChecked(False)

        self.filtroDeteccaoDeBordas = self.menuTransformacao.addAction("Filtros &Detecção de Bordas")
        self.filtroDeteccaoDeBordas.setShortcut("Ctrl+Shift+D")
        self.filtroDeteccaoDeBordas.triggered.connect(self.transformarImagem)
        self.filtroDeteccaoDeBordas.setDisabled(True)
        self.filtroDeteccaoDeBordas.setCheckable(True)
        self.filtroDeteccaoDeBordas.setChecked(False)

        self.filtroSharpen = self.menuTransformacao.addAction("Filtro S&harpen")
        self.filtroSharpen.setShortcut("Ctrl+Shift+H")
        self.filtroSharpen.triggered.connect(self.transformarImagem)
        self.filtroSharpen.setDisabled(True)
        self.filtroSharpen.setCheckable(True)
        self.filtroSharpen.setChecked(False)

        self.filtroSobel = self.menuTransformacao.addAction("Filtro S&obel")
        self.filtroSobel.setShortcut("Ctrl+Shift+O")
        self.filtroSobel.triggered.connect(self.transformarImagem)
        self.filtroSobel.setDisabled(True)
        self.filtroSobel.setCheckable(True)
        self.filtroSobel.setChecked(False)

        self.extrairCamadaRGB = self.menuTransformacao.addAction("Extrair &Camadas RGB")
        self.extrairCamadaRGB.setShortcut("Ctrl+Shift+C")
        self.extrairCamadaRGB.triggered.connect(self.transformarImagem)
        self.extrairCamadaRGB.setDisabled(True)
        self.extrairCamadaRGB.setCheckable(True)
        self.extrairCamadaRGB.setChecked(False)

        self.converterEscalaCinza = self.menuTransformacao.addAction("Converter para Escala de C&inza")
        self.converterEscalaCinza.setShortcut("Ctrl+Shift+I")
        self.converterEscalaCinza.triggered.connect(self.transformarImagem)
        self.converterEscalaCinza.setDisabled(True)
        self.converterEscalaCinza.setCheckable(True)
        self.converterEscalaCinza.setChecked(False)

        self.converterPretoBranco = self.menuTransformacao.addAction("Converter Pre&to e Branco")
        self.converterPretoBranco.setShortcut("Ctrl+Shift+T")
        self.converterPretoBranco.triggered.connect(self.transformarImagem)
        self.converterPretoBranco.setDisabled(True)
        self.converterPretoBranco.setCheckable(True)
        self.converterPretoBranco.setChecked(False)

        listaFiltrosColoridaCinza = [self.correcaoGama, self.filtroGaussiano, self.filtroMediana,
                                     self.filtroNegativo, self.transformacaoLogaritmica,
                                     self.filtroDeteccaoDeBordas, self.filtroSharpen, self.filtroSobel,
                                     self.extrairCamadaRGB, self.converterEscalaCinza, self.converterPretoBranco]

    def gerarLayouts(self):
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
            self.parts = self.endImagemOriginal.rpartition('/')
            self.nomeimagem = self.parts[2]
            self.leituraimagem = open(self.endImagemOriginal, "r+")
            self.tipoimagem = self.leituraimagem.readline()
            self.comentarioimagem = self.leituraimagem.readline()
            self.dimensoesimagem = self.leituraimagem.readline()
            self.dimensoesimagem = self.dimensoesimagem.split()
            self.larguraimagem = self.dimensoesimagem[0]
            self.alturaimagem = self.dimensoesimagem[1]
        except:
            pass

    def mostrarInformacoesSobre(self):

        self.opcaoEscolhida = self.sender().text()
        self.caixaMensagem = QMessageBox()
        self.caixaMensagem.setIcon(QMessageBox.Information)

        if self.opcaoEscolhida == "S&obre o Aplicativo":
            self.caixaMensagem.setWindowTitle("Sobre o Aplicativo")
            self.caixaMensagem.setText("Desenvolvido por Thaís Aparecida Vilarinho de Jesus")
            self.caixaMensagem.setInformativeText("Capinópolis-MG, 24 de Junho de 2020")
            self.descricao = "Este aplicativo realiza Transformações em imagens com extensão ppm, pgm e pbm e " \
                             "foi elaborado como forma de trabalho apresentado a disciplina de Processamento Digital" \
                             "de Imagens no Curso Superior em Análise e Desenvolvimento de Sistemas, do Instituto " \
                             "Federal de Educação, Ciência e Tecnologia do Triângulo Mineiro (IFTM) - Campus Ituiutaba"

            self.caixaMensagem.setDetailedText(self.descricao)
            self.caixaMensagem.exec_()

        if self.opcaoEscolhida == "&Informacões da Imagem":
            if self.endImagemOriginal != '':
                self.caixaMensagem.setWindowTitle("Informações da Imagem")

                self.informacoesDaImagem()

                self.caixaMensagem.setText("Arquivo: " + self.nomeimagem + "\n" + "Tipo: " + self.tipoimagem +
                                           "Comentário: " + self.comentarioimagem + "Largura: " + self.larguraimagem \
                                           + "\n" + "Altura: " + self.alturaimagem)

                self.caixaMensagem.exec_()

    def salvarAquivoComo(self):
        global extensaoImagemResultado
        try:
            if self.endImagemOriginal != '':
                imagemSalvaComo, tipos = QFileDialog.getSaveFileName(self, caption='Salvar como',
                                                                     directory=QtCore.QDir.currentPath(),
                                                                     filter='Imagens(*.ppm; *.pgm; *.pbm)',
                                                                     initialFilter='Imagens(*.ppm; *.pgm; *.pbm)')
                if imagemSalvaComo:
                    self.parts = imagemSalvaComo.rpartition('/')
                    self.endereco = self.parts[0]
                    if self.endImagemResultado != '':
                        shutil.copyfile(self.endImagemResultado, self.endereco + '/' +
                                        os.path.splitext(os.path.basename(imagemSalvaComo))[0] +
                                        extensaoImagemResultado)
                    else:
                        shutil.copyfile(self.endImagemOriginal, self.endereco + '/' +
                                        os.path.splitext(os.path.basename(imagemSalvaComo))[0] +
                                        self.extensaoImagemOriginal)
        except:
            pass

    def abrirArquivo(self):
        global imagemResultado
        global extensaoImagemResultado

        self.ocultarArquivos()

        global porcentagemProgresso
        arquivoImagem, _ = QFileDialog.getOpenFileName(self, caption="Open Image",
                                                       directory=QtCore.QDir.currentPath(),
                                                       filter='Imagens(*.ppm; *.pgm; *.pbm)',
                                                       initialFilter='Imagens(*.ppm; *.pgm; *.pbm)')

        if arquivoImagem:
            self.excluirCopiaTransformada()
            self.removerChecagemFiltroUsado()
            porcentagemProgresso = 0
            self.barraProgresso.setValue(porcentagemProgresso)
            self.endImagemOriginal = arquivoImagem
            self.pixmapImagem = QPixmap(self.endImagemOriginal)
            self.exibirImagem()
            self.extensaoImagemOriginal = os.path.splitext(os.path.basename(arquivoImagem))[1]
            self.alterarVisibilidadeMenus()
        else:
            self.desocultarArquivos()

    def exibirImagem(self):
        if self.pixmapImagem.width() > int(GetSystemMetrics(0) / 2) or \
                self.pixmapImagem.height() > int(GetSystemMetrics(1) / 2):
            self.pixmapImagem = self.pixmapImagem.scaled(int(GetSystemMetrics(0) / 2), int(GetSystemMetrics(1) / 2),
                                                         QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

        self.imagemOriginal.setPixmap(self.pixmapImagem)
        self.imagemOriginal.setAlignment(QtCore.Qt.AlignCenter)

    def excluirCopiaTransformada(self):
        global imagemResultado
        global extensaoImagemResultado
        try:
            if os.path.exists(imagemResultado + "Copia" + '.ppm') or os.path.exists(imagemResultado + '.ppm'):
                os.remove(imagemResultado + "Copia" + '.ppm')
                os.remove(imagemResultado + '.ppm')

            if os.path.exists(imagemResultado + "Copia" + '.pgm') or os.path.exists(imagemResultado + '.pgm'):
                os.remove(imagemResultado + "Copia" + '.pgm')
                os.remove(imagemResultado + '.pgm')

            if os.path.exists(imagemResultado + "Copia" + '.pbm') or os.path.exists(imagemResultado + '.pbm'):
                os.remove(imagemResultado + "Copia" + '.pbm')
                os.remove(imagemResultado + '.pbm')
        except:
            pass

    def transformarImagem(self):

        global porcentagemProgresso
        global imagemResultado
        global extensaoImagemResultado
        global listaFiltrosUsados

        porcentagemProgresso = 0
        self.barraProgresso.setValue(porcentagemProgresso)
        self.filtroEscolhido = self.sender().text()
        self.filtroUsado = ''

        if os.path.exists(imagemResultado + "Copia" + extensaoImagemResultado):
            self.argumentoEntrada = imagemResultado + "Copia" + extensaoImagemResultado
        else:
            self.argumentoEntrada = self.endImagemOriginal

        try:
            if self.filtroEscolhido == "Filtro Fator &Gama":
                if self.extensaoImagemOriginal == '.ppm':
                    self.script = 'filtrosDeTransformacao/colorida/CorrecaoGama.py'
                    extensaoImagemResultado = '.ppm'

                elif self.extensaoImagemOriginal == '.pgm':
                    self.script = 'filtrosDeTransformacao/escalaCinza/CorrecaoGama.py'
                    extensaoImagemResultado = '.pgm'

                self.filtroUsado = self.correcaoGama

            if self.filtroEscolhido == "Filtro Ga&ussiano":
                if self.extensaoImagemOriginal == '.ppm':
                    self.script = 'filtrosDeTransformacao/colorida/Gaussiano3x3.py'
                    extensaoImagemResultado = '.ppm'

                elif self.extensaoImagemOriginal == '.pgm':
                    self.script = 'filtrosDeTransformacao/escalaCinza/Gaussiano3x3.py'
                    extensaoImagemResultado = '.pgm'

                self.filtroUsado = self.filtroGaussiano

            if self.filtroEscolhido == "Filtro &Mediana":
                if self.extensaoImagemOriginal == '.ppm':
                    self.script = 'filtrosDeTransformacao/colorida/Mediana.py'
                    extensaoImagemResultado = '.ppm'

                elif self.extensaoImagemOriginal == '.pgm':
                    self.script = 'filtrosDeTransformacao/escalaCinza/Mediana.py'
                    extensaoImagemResultado = '.pgm'

                self.filtroUsado = self.filtroMediana

            if self.filtroEscolhido == "Filtro &Negativo":
                if self.extensaoImagemOriginal == '.ppm':
                    self.script = 'filtrosDeTransformacao/colorida/Negativo.py'
                    extensaoImagemResultado = '.ppm'

                elif self.extensaoImagemOriginal == '.pgm':
                    self.script = 'filtrosDeTransformacao/escalaCinza/Negativo.py'
                    extensaoImagemResultado = '.pgm'

                self.filtroUsado = self.filtroNegativo

            if self.filtroEscolhido == 'Transformação &Logarítmica':
                if self.extensaoImagemOriginal == '.ppm':
                    self.script = 'filtrosDeTransformacao/colorida/TransformacaoLogaritmica.py'
                    extensaoImagemResultado = '.ppm'

                elif self.extensaoImagemOriginal == '.pgm':
                    self.script = 'filtrosDeTransformacao/escalaCinza/TransformacaoLogaritmica.py'
                    extensaoImagemResultado = '.pgm'

                self.filtroUsado = self.transformacaoLogaritmica

            if self.filtroEscolhido == 'Filtros &Detecção de Bordas':
                if self.extensaoImagemOriginal == '.ppm':
                    print("ACRESCENTAR AQUI O CÓDIGO DETECÇÃO DE BORDAS EM IMAGEM COLORIDA")

                elif self.extensaoImagemOriginal == '.pgm':
                    self.script = 'filtrosDeTransformacao/escalaCinza/EdgeDetection.py'
                    extensaoImagemResultado = '.pgm'

                elif self.extensaoImagemOriginal == '.pbm':
                    self.script = 'filtrosDeTransformacao/pretoBranco/EdgeDetection.py'
                    extensaoImagemResultado = '.pbm'

                self.filtroUsado = self.filtroDeteccaoDeBordas

            if self.filtroEscolhido == 'Filtro S&harpen':
                if self.extensaoImagemOriginal == '.ppm':
                    self.script = 'filtrosDeTransformacao/colorida/Sharpen.py'

                elif self.extensaoImagemOriginal == '.pgm':
                    self.script = 'filtrosDeTransformacao/escalaCinza/Sharpen.py'
                    extensaoImagemResultado = '.pgm'

                self.filtroUsado = self.filtroSharpen

            if self.filtroEscolhido == 'Filtro S&obel':
                if self.extensaoImagemOriginal == '.ppm':
                    self.script = 'filtrosDeTransformacao/colorida/Sobel.py'

                elif self.extensaoImagemOriginal == '.pgm':
                    self.script = 'filtrosDeTransformacao/escalaCinza/Sobel.py'
                    extensaoImagemResultado = '.pgm'

                self.filtroUsado = self.filtroSobel

            if self.filtroEscolhido == 'Extrair &Camadas RGB':
                if self.extensaoImagemOriginal == '.ppm':
                    self.script = 'filtrosDeTransformacao/colorida/CamadaR.py'
                    extensaoImagemResultado = '.ppm'
                    self.filtroUsado = self.extrairCamadaRGB

            if self.filtroEscolhido == 'Converter para Escala de C&inza':
                if self.extensaoImagemOriginal == '.ppm':
                    self.script = 'filtrosDeTransformacao/colorida/ConverterEscalaDeCinza.py'
                    extensaoImagemResultado = '.pgm'

                    self.filtroUsado = self.converterEscalaCinza

            if self.filtroEscolhido == 'Converter Pre&to e Branco':
                if self.extensaoImagemOriginal == '.ppm':
                    pass

                elif self.extensaoImagemOriginal == '.pgm':
                    self.script = 'filtrosDeTransformacao/escalaCinza/Binaria.py'
                    extensaoImagemResultado = '.pbm'

                self.filtroUsado = self.converterPretoBranco

            self.argumentos = 'python ' + self.script + ' \"' + self.argumentoEntrada + '\" ' + \
                              imagemResultado + extensaoImagemResultado
            self.executarTransformacao = subprocess.run(self.argumentos, shell=True)

            while porcentagemProgresso < 100:
                if self.executarTransformacao is not None:
                    porcentagemProgresso += 0.001
                    self.barraProgresso.setValue(int(porcentagemProgresso))
                else:
                    break

            self.endImagemResultado = imagemResultado + extensaoImagemResultado
            self.pixmapImagem = QPixmap(self.endImagemResultado)
            shutil.copyfile(self.endImagemResultado, imagemResultado + "Copia" + extensaoImagemResultado)
            self.exibirImagem()
            listaFiltrosUsados.append(self.filtroUsado)
            self.extensaoImagemOriginal = extensaoImagemResultado
            self.alterarVisibilidadeMenus()

            self.barraStatus.showMessage("Aplicação " + self.filtroEscolhido.replace("&", "") +
                                         " finalizada", 5000)
        except:
            pass

    def alterarVisibilidadeMenus(self):
        global listaFiltrosColoridaCinza

        self.opcaoInfoImagem.setVisible(True)
        self.opcaoSalvarComo.setDisabled(False)

        if self.extensaoImagemOriginal == '.ppm':
            for filtro in listaFiltrosColoridaCinza:
                filtro.setDisabled(False)

        elif self.extensaoImagemOriginal == '.pgm':
            for filtro in listaFiltrosColoridaCinza:
                    filtro.setDisabled(False)
            self.extrairCamadaRGB.setDisabled(True)
            self.converterEscalaCinza.setDisabled(True)

        elif self.extensaoImagemOriginal == '.pbm':
            for filtro in listaFiltrosColoridaCinza:
                    filtro.setDisabled(True)

            self.filtroDeteccaoDeBordas.setDisabled(False)

    def removerChecagemFiltroUsado(self):
        global listaFiltrosUsados
        for filtro in listaFiltrosUsados:
            filtro.setChecked(False)

        listaFiltrosUsados.clear()

    def ocultarArquivos(self):
        global imagemResultado
        global extensaoImagemResultado

        if os.path.exists(imagemResultado + "Copia.ppm"):
            os.system("attrib +h " + imagemResultado + "Copia" + extensaoImagemResultado)
            os.system("attrib +h " + imagemResultado + ".ppm")

        if os.path.exists(imagemResultado + "Copia.pgm"):
            os.system("attrib +h " + imagemResultado + "Copia" + extensaoImagemResultado)
            os.system("attrib +h " + imagemResultado + ".pgm")

        if os.path.exists(imagemResultado + "Copia.pbm"):
            os.system("attrib +h " + imagemResultado + "Copia" + extensaoImagemResultado)
            os.system("attrib +h " + imagemResultado + ".pbm")

    def desocultarArquivos(self):
        os.system("attrib -h " + imagemResultado + "Copia" + extensaoImagemResultado)
        os.system("attrib -h " + self.endImagemResultado)

    def closeEvent(self, event):
        global listaFiltrosUsados
        self.excluirCopiaTransformada()


def main():
    app = QApplication(sys.argv)
    win = MyWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
