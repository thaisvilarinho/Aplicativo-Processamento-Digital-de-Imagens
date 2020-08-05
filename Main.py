import sys
import os
import shutil
import subprocess
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
from win32api import GetSystemMetrics

from DesenharElementoEstruturante import JanelaMatriz
from ValorCorrecaoGama import JanelaValorGama
from ValorLimitePretoBranco import JanelaValorLimitePretoBranco
from ValorLimiteSobel import JanelaValorLimiteSobel

porcentagemProgresso = 0
imagemResultado = 'imagensResultado/imagemTransformada'
extensaoImagemResultado = '.ppm'


def excluirCopiaImgTransformada():
    global imagemResultado
    try:
        if os.path.exists(imagemResultado + "Copia" + '.ppm'):
            os.remove(imagemResultado + "Copia" + '.ppm')

        if os.path.exists(imagemResultado + "Copia" + '.pgm'):
            os.remove(imagemResultado + "Copia" + '.pgm')

        if os.path.exists(imagemResultado + "Copia" + '.pbm'):
            os.remove(imagemResultado + "Copia" + '.pbm')
    except:
        pass


def ocultarDiretorioImgResultado():
    os.system("attrib +h " + 'imagensResultado')


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setWindowTitle("Processamento Digital de Imagens - IFTM")
        self.icon = self.setWindowIcon(QIcon("icones/icon.jpg"))
        self.setGeometry(450, 150, 800, 600)
        self.initUI()
        self.listaFiltrosUsados = []

        self.show()

    '''Chamar métodos que criam a interface'''

    def initUI(self):
        self.criarListasControleVisibilidadeItens()
        self.criarWidgets()
        self.gerarLayouts()

    def criarListasControleVisibilidadeItens(self):
        self.listaFiltrosImgColoridaCinza = []
        self.listaFiltrosImgPretoBranco = []
        self.listaRemoverFiltrosParaEscalaDeCinza = []

    '''Cria os widgets que encorporam o Menu e widgets que executaram ações'''

    def criarWidgets(self):
        # Criar a barra de menu
        self.barraMenu = self.menuBar()

        # Criar menus
        self.menuArquivo = self.barraMenu.addMenu("&Arquivo")
        self.menuTransformacao = self.barraMenu.addMenu("&Transformações")
        self.menuSobre = self.barraMenu.addMenu("So&bre")

        # Crias as actions
        self.opcaoAbrir = self.menuArquivo.addAction("A&brir")
        self.opcaoAbrir.triggered.connect(self.abrirImagem)
        self.opcaoAbrir.setShortcut("Ctrl+A")

        self.opcaoRecente = self.menuArquivo.addMenu("Abrir &Recente")
        self.abrirRecente = self.opcaoRecente.addAction("arquivos...")
        self.abrirRecente.setDisabled(True)

        self.opcaoSalvarComo = self.menuArquivo.addAction("&Salvar como")
        self.opcaoSalvarComo.triggered.connect(self.salvarImagemComo)
        self.opcaoSalvarComo.setShortcut("Ctrl+S")
        self.opcaoSalvarComo.setDisabled(True)

        self.menuArquivo.addSeparator()
        self.opcaoFechar = self.menuArquivo.addAction("F&echar")
        self.opcaoFechar.setShortcut("Ctrl+X")
        self.opcaoFechar.triggered.connect(self.close)

        self.criarSubmenus()

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

    '''Utiliza métodos para criar os Submenus que irão possuir as ações com filtros e trasnformações e chama o método
    para adicionar submenus e actions em listas que irão controlar as demarcações de checagem de filtros usados'''

    def criarSubmenus(self):

        self.criarSubmenuAjustarNitidez()
        self.criarSubmenuConversao()
        self.criarSubmenuDecomporCanaisRGB()
        self.criarSubmenuDesfocar()
        self.criarSubmenuDeteccaoDeBordas()
        self.criarSubmenuInverterCores()
        self.criarSubmenuRealcarIntensidade()
        self.criarSubmenuMorfologicas()

    '''Criar Submenus'''

    def criarSubmenuAjustarNitidez(self):
        # Submenu
        self.submenuAjustarNitidez = self.menuTransformacao.addMenu("Ajustar Nitide&z")
        self.submenuAjustarNitidez.setDisabled(True)

        # Actions do submenu
        self.criarActionFiltroSharpen()

        # Listar submenu
        self.listaFiltrosImgColoridaCinza.append(self.submenuAjustarNitidez)

    def criarSubmenuRealcarIntensidade(self):
        # Submenu
        self.submenuRealcarIntensidade = self.menuTransformacao.addMenu("Real&çar Intensidade")
        self.submenuRealcarIntensidade.setDisabled(True)

        # Actions do submenu
        self.criarActionCorrecaoGama()
        self.criarActionTransformacaoLogaritmica()

        # Listar submenu
        self.listaFiltrosImgColoridaCinza.append(self.submenuRealcarIntensidade)

    def criarSubmenuConversao(self):
        # Submenu
        self.submenuConversao = self.menuTransformacao.addMenu("Con&verter")
        self.submenuConversao.setDisabled(True)

        # Actions do submenu
        self.criarActionConverterParaEscalaCinza()
        self.criarActionConverterParaPretoBranco()

        # Listar submenu
        self.listaFiltrosImgColoridaCinza.append(self.submenuConversao)

    def criarSubmenuDecomporCanaisRGB(self):
        # Submenu
        self.submenuDecomposicaoCanaisRGB = self.menuTransformacao.addMenu("Decomposição &Canais RGB")
        self.submenuDecomposicaoCanaisRGB.setDisabled(True)

        # Actions do submenu
        self.criarActionDecomporCanalR()
        self.criarActionDecomporCanalG()
        self.criarActionDecomporCanalB()

        # Listar submenu
        self.listaFiltrosImgColoridaCinza.append(self.submenuDecomposicaoCanaisRGB)
        self.listaRemoverFiltrosParaEscalaDeCinza.append(self.submenuDecomposicaoCanaisRGB)

    def criarSubmenuDesfocar(self):
        # Submenu
        self.submenuFiltrosDesfocar = self.menuTransformacao.addMenu("Des&focar")
        self.submenuFiltrosDesfocar.setDisabled(True)

        # Criar novo submenu
        self.criarSubmenuFiltroGaussiano()
        # Actions do submenu
        self.criarActionFiltroMediana()

        # Listar submenu
        self.listaFiltrosImgColoridaCinza.append(self.submenuFiltrosDesfocar)

    def criarSubmenuDeteccaoDeBordas(self):
        # Submenu
        self.submenuFiltrosDeteccaoBordas = self.menuTransformacao.addMenu("&Detectar Bordas")
        self.submenuFiltrosDeteccaoBordas.setDisabled(True)

        # Actions do submenu
        self.criarActionDeteccaoDeBordasCrono()
        self.criarActionDeteccaoDeBordasMarle()
        self.criarActionDeteccaoDeBordasPrometheus()
        self.criarActionFiltroSobel()
        self.criarActionDeteccaoDeBordasDilatacao()
        self.criarActionDeteccaoDeBordasErosao()

        # Listar submenu
        self.listaFiltrosImgColoridaCinza.append(self.submenuFiltrosDeteccaoBordas)
        self.listaFiltrosImgPretoBranco.append(self.submenuFiltrosDeteccaoBordas)

    def criarSubmenuFiltroGaussiano(self):
        # Submenu
        self.submenuFiltroGaussiano = self.submenuFiltrosDesfocar.addMenu("Filtro Ga&ussiano")
        self.submenuFiltroGaussiano.setDisabled(True)

        # Actions do submenu
        self.criarActionKernelGaussiano3x3()
        self.criarActionKernelGaussiano5x5()
        self.criarActionKernelGaussiano7x7()

        # Listar submenu
        self.listaFiltrosImgColoridaCinza.append(self.submenuFiltroGaussiano)

    def criarSubmenuInverterCores(self):
        # Submenu
        self.submenuInverterCores = self.menuTransformacao.addMenu("Inverter Cores")
        self.submenuInverterCores.setDisabled(True)

        # Actions do submenu
        self.criarActionInverterNegativo()

        # Listar submenu
        self.listaFiltrosImgColoridaCinza.append(self.submenuInverterCores)

    def criarSubmenuMorfologicas(self):
        # Submenu
        self.submenuMorfologicas = self.menuTransformacao.addMenu("&Morfológicas")
        self.submenuMorfologicas.setDisabled(True)

        # Submenus
        self.criarSubmenuAbertura()
        self.criarActionFiltroDilatacao()
        self.criarActionFiltroErosao()
        self.criarActionFiltroFechamento()

        # Listar submenu
        self.listaFiltrosImgPretoBranco.append(self.submenuMorfologicas)

    def criarSubmenuAbertura(self):
        self.submenuFiltroAbertura = self.submenuMorfologicas.addMenu("&Abertura")
        self.submenuFiltroAbertura.setDisabled(True)

        # Actions do submenu
        self.criarActionAberturaElementoEstrutura3x3()
        self.criarActionAberturaElementoEstrutura5x5()
        self.criarActionAberturaElementoEstrutura7x7()
        self.criarActionAberturaElementoEstrutura9x9()

        # Listar submenu
        self.listaFiltrosImgPretoBranco.append(self.submenuFiltroAbertura)

    '''Criar Actions'''

    def criarActionConverterParaEscalaCinza(self):
        self.converterParaEscalaCinza = self.submenuConversao.addAction("&Tons de Cinza")
        self.converterParaEscalaCinza.setShortcut("Ctrl+Alt+Z")
        self.converterParaEscalaCinza.setDisabled(True)
        self.converterParaEscalaCinza.setCheckable(True)
        self.converterParaEscalaCinza.setChecked(False)
        self.converterParaEscalaCinza.triggered.connect(lambda: self.transformarImagem(
            self.converterParaEscalaCinza, 'ConverterEscalaDeCinza', '.pgm', 'ArgumentoVazio'))

        # Listar action
        self.listaFiltrosImgColoridaCinza.append(self.converterParaEscalaCinza)
        self.listaRemoverFiltrosParaEscalaDeCinza.append(self.converterParaEscalaCinza)

    def criarActionConverterParaPretoBranco(self):
        self.converterParaPretoBranco = self.submenuConversao.addAction("Tons Pre&to e Branco")
        self.converterParaPretoBranco.setShortcut("Ctrl+Shift+T")
        self.converterParaPretoBranco.setDisabled(True)
        self.converterParaPretoBranco.setCheckable(True)
        self.converterParaPretoBranco.setChecked(False)
        self.converterParaPretoBranco.triggered.connect(self.janelaValorLimitePretoBranco)

        # Listar action
        self.listaFiltrosImgColoridaCinza.append(self.converterParaPretoBranco)

    def criarActionCorrecaoGama(self):
        self.correcaoGama = self.submenuRealcarIntensidade.addAction("Correção &Gama")
        self.correcaoGama.setShortcut("Ctrl+Shift+G")
        self.correcaoGama.setDisabled(True)
        self.correcaoGama.setCheckable(True)
        self.correcaoGama.setChecked(False)
        self.correcaoGama.triggered.connect(self.janelaValorCorrecaoGama)

        # Listar action
        self.listaFiltrosImgColoridaCinza.append(self.correcaoGama)

    def criarActionDecomporCanalR(self):
        self.decomporCanalR = self.submenuDecomposicaoCanaisRGB.addAction("Vermelho")
        self.decomporCanalR.setShortcut("Ctrl+Alt+R")
        self.decomporCanalR.setCheckable(True)
        self.decomporCanalR.setChecked(False)
        self.decomporCanalR.triggered.connect(lambda: self.transformarImagem(
            self.decomporCanalR, 'CamadaR', '.ppm', 'ArgumentoVazio'))

        # Listar action
        self.listaFiltrosImgColoridaCinza.append(self.decomporCanalR)
        self.listaRemoverFiltrosParaEscalaDeCinza.append(self.decomporCanalR)

    def criarActionDecomporCanalG(self):
        self.decomporCanalG = self.submenuDecomposicaoCanaisRGB.addAction("Verde")
        self.decomporCanalG.setShortcut("Ctrl+Alt+G")
        self.decomporCanalG.setCheckable(True)
        self.decomporCanalG.setChecked(False)
        self.decomporCanalG.triggered.connect(lambda: self.transformarImagem(
            self.decomporCanalG, 'CamadaG', '.ppm', 'ArgumentoVazio'))

        # Listar action
        self.listaFiltrosImgColoridaCinza.append(self.decomporCanalG)
        self.listaRemoverFiltrosParaEscalaDeCinza.append(self.decomporCanalG)

    def criarActionDecomporCanalB(self):
        self.decomporCanalB = self.submenuDecomposicaoCanaisRGB.addAction("Azul")
        self.decomporCanalB.setShortcut("Ctrl+Alt+B")
        self.decomporCanalB.setCheckable(True)
        self.decomporCanalB.setChecked(False)
        self.decomporCanalB.triggered.connect(lambda: self.transformarImagem(
            self.decomporCanalB, 'CamadaB', '.ppm', 'ArgumentoVazio'))

        # Listar action
        self.listaFiltrosImgColoridaCinza.append(self.decomporCanalB)
        self.listaRemoverFiltrosParaEscalaDeCinza.append(self.decomporCanalB)

    def criarActionDeteccaoDeBordasCrono(self):
        self.deteccaoDeBordasFiltroCrono = self.submenuFiltrosDeteccaoBordas.addAction("Filtro &Crono")
        self.deteccaoDeBordasFiltroCrono.setShortcut("Ctrl+Alt+C")
        self.deteccaoDeBordasFiltroCrono.setCheckable(True)
        self.deteccaoDeBordasFiltroCrono.setChecked(False)
        self.deteccaoDeBordasFiltroCrono.triggered.connect(lambda: self.transformarImagem(
            self.deteccaoDeBordasFiltroCrono, 'DeteccaoDeBordasCrono', self.extensaoImagemOriginal, 'ArgumentoVazio'))

        # Listar action
        self.listaFiltrosImgColoridaCinza.append(self.deteccaoDeBordasFiltroCrono)
        self.listaFiltrosImgPretoBranco.append(self.deteccaoDeBordasFiltroCrono)

    def criarActionDeteccaoDeBordasDilatacao(self):
        self.deteccaoDeBordasDilatacao = self.submenuFiltrosDeteccaoBordas.addAction("Filtro Detecção com &Dilatação")
        self.deteccaoDeBordasDilatacao.setShortcut("Ctrl+Alt+I")
        self.deteccaoDeBordasDilatacao.setCheckable(True)
        self.deteccaoDeBordasDilatacao.setChecked(False)
        self.deteccaoDeBordasDilatacao.triggered.connect(lambda: self.transformarImagem(
            self.deteccaoDeBordasDilatacao, 'DeteccaoDeBordasDilatacao', self.extensaoImagemOriginal, 'ArgumentoVazio'))

        # Listar action
        self.listaFiltrosImgPretoBranco.append(self.deteccaoDeBordasDilatacao)

    def criarActionDeteccaoDeBordasErosao(self):
        self.deteccaoDeBordasErosao = self.submenuFiltrosDeteccaoBordas.addAction("Filtro Detecção com &Erosão")
        self.deteccaoDeBordasErosao.setShortcut("Ctrl+Alt+O")
        self.deteccaoDeBordasErosao.setCheckable(True)
        self.deteccaoDeBordasErosao.setChecked(False)
        self.deteccaoDeBordasErosao.triggered.connect(lambda: self.transformarImagem(
            self.deteccaoDeBordasErosao, 'DeteccaoDeBordasErosao', self.extensaoImagemOriginal, 'ArgumentoVazio'))

        # Listar action
        self.listaFiltrosImgPretoBranco.append(self.deteccaoDeBordasErosao)

    def criarActionDeteccaoDeBordasMarle(self):
        self.deteccaoDeBordasFiltroMarle = self.submenuFiltrosDeteccaoBordas.addAction("Filtro Marle")
        self.deteccaoDeBordasFiltroMarle.setShortcut("Ctrl+Alt+M")
        self.deteccaoDeBordasFiltroMarle.setCheckable(True)
        self.deteccaoDeBordasFiltroMarle.setChecked(False)
        self.deteccaoDeBordasFiltroMarle.triggered.connect(lambda: self.transformarImagem(
            self.deteccaoDeBordasFiltroMarle, 'DeteccaoDeBordasMarle', self.extensaoImagemOriginal, 'ArgumentoVazio'))

        # Listar action
        self.listaFiltrosImgColoridaCinza.append(self.deteccaoDeBordasFiltroMarle)
        self.listaFiltrosImgPretoBranco.append(self.deteccaoDeBordasFiltroMarle)

    def criarActionDeteccaoDeBordasPrometheus(self):
        self.deteccaoDeBordasFiltroPrometheus = self.submenuFiltrosDeteccaoBordas.addAction("Filtro Prometheus")
        self.deteccaoDeBordasFiltroPrometheus.setShortcut("Ctrl+Alt+P")
        self.deteccaoDeBordasFiltroPrometheus.setCheckable(True)
        self.deteccaoDeBordasFiltroPrometheus.setChecked(False)
        self.deteccaoDeBordasFiltroPrometheus.triggered.connect(lambda: self.transformarImagem(
            self.deteccaoDeBordasFiltroPrometheus, 'DeteccaoDeBordasPrometheus', self.extensaoImagemOriginal,
            'ArgumentoVazio'))

        # Listar action
        self.listaFiltrosImgColoridaCinza.append(self.deteccaoDeBordasFiltroPrometheus)
        self.listaFiltrosImgPretoBranco.append(self.deteccaoDeBordasFiltroPrometheus)

    def criarActionAberturaElementoEstrutura3x3(self):
        self.aberturaElementoEstruturante3x3 = self.submenuFiltroAbertura.addAction("Elemento Estruturante 3x3")
        self.aberturaElementoEstruturante3x3.setShortcut("Ctrl+A+3")
        self.aberturaElementoEstruturante3x3.setDisabled(True)
        self.aberturaElementoEstruturante3x3.setCheckable(True)
        self.aberturaElementoEstruturante3x3.setChecked(False)
        self.aberturaElementoEstruturante3x3.triggered.connect(lambda:
                                                               self.criarJanelaDesenharElementoEstruturante(3, 3,
                                                                                                            self.aberturaElementoEstruturante3x3,
                                                                                                            'Abertura',
                                                                                                            self.extensaoImagemOriginal))

        # Listar action
        self.listaFiltrosImgPretoBranco.append(self.aberturaElementoEstruturante3x3)

    def criarActionAberturaElementoEstrutura5x5(self):
        self.aberturaElementoEstruturante5x5 = self.submenuFiltroAbertura.addAction("Elemento Estruturante 5x5")
        self.aberturaElementoEstruturante5x5.setShortcut("Ctrl+A+5")
        self.aberturaElementoEstruturante5x5.setDisabled(True)
        self.aberturaElementoEstruturante5x5.setCheckable(True)
        self.aberturaElementoEstruturante5x5.setChecked(False)
        self.aberturaElementoEstruturante5x5.triggered.connect(lambda:
                                                               self.criarJanelaDesenharElementoEstruturante(5, 5,
                                                               self.aberturaElementoEstruturante3x3, 'Abertura',
                                                               self.extensaoImagemOriginal))

        # Listar action
        self.listaFiltrosImgPretoBranco.append(self.aberturaElementoEstruturante5x5)

    def criarActionAberturaElementoEstrutura7x7(self):
        self.aberturaElementoEstruturante7x7 = self.submenuFiltroAbertura.addAction("Elemento Estruturante 7x7")
        self.aberturaElementoEstruturante7x7.setShortcut("Ctrl+A+7")
        self.aberturaElementoEstruturante7x7.setDisabled(True)
        self.aberturaElementoEstruturante7x7.setCheckable(True)
        self.aberturaElementoEstruturante7x7.setChecked(False)
        self.aberturaElementoEstruturante7x7.triggered.connect(lambda:
                                                               self.criarJanelaDesenharElementoEstruturante(7, 7,
                                                               self.aberturaElementoEstruturante7x7, 'Abertura',
                                                               self.extensaoImagemOriginal))

        # Listar action
        self.listaFiltrosImgPretoBranco.append(self.aberturaElementoEstruturante7x7)

    def criarActionAberturaElementoEstrutura9x9(self):
        self.aberturaElementoEstruturante9x9 = self.submenuFiltroAbertura.addAction("Elemento Estruturante 9x9")
        self.aberturaElementoEstruturante9x9.setShortcut("Ctrl+A+9")
        self.aberturaElementoEstruturante9x9.setDisabled(True)
        self.aberturaElementoEstruturante9x9.setCheckable(True)
        self.aberturaElementoEstruturante9x9.setChecked(False)
        self.aberturaElementoEstruturante9x9.triggered.connect(lambda:
                                                               self.criarJanelaDesenharElementoEstruturante(9, 9,
                                                               self.aberturaElementoEstruturante9x9, 'Abertura',
                                                               self.extensaoImagemOriginal))

        # Listar action
        self.listaFiltrosImgPretoBranco.append(self.aberturaElementoEstruturante9x9)

    def criarActionKernelGaussiano3x3(self):
        self.kernelGaussiano3x3 = self.submenuFiltroGaussiano.addAction("Matriz 3x3")
        self.kernelGaussiano3x3.setShortcut("Ctrl+Alt+3")
        self.kernelGaussiano3x3.setCheckable(True)
        self.kernelGaussiano3x3.setChecked(False)
        self.kernelGaussiano3x3.triggered.connect(lambda: self.transformarImagem(
            self.kernelGaussiano3x3, 'Gaussiano3x3', self.extensaoImagemOriginal, 'ArgumentoVazio'))

        # Listar action
        self.listaFiltrosImgColoridaCinza.append(self.kernelGaussiano3x3)

    def criarActionKernelGaussiano5x5(self):
        self.kernelGaussiano5x5 = self.submenuFiltroGaussiano.addAction("Matriz 5x5")
        self.kernelGaussiano5x5.setShortcut("Ctrl+Alt+5")
        self.kernelGaussiano5x5.setCheckable(True)
        self.kernelGaussiano5x5.setChecked(False)
        self.kernelGaussiano5x5.triggered.connect(lambda: self.transformarImagem(
            self.kernelGaussiano5x5, 'Gaussiano5x5', self.extensaoImagemOriginal, 'ArgumentoVazio'))

        # Listar action
        self.listaFiltrosImgColoridaCinza.append(self.kernelGaussiano5x5)

    def criarActionKernelGaussiano7x7(self):
        self.kernelGaussiano7x7 = self.submenuFiltroGaussiano.addAction("Matriz 7x7")
        self.kernelGaussiano7x7.setShortcut("Ctrl+Alt+7")
        self.kernelGaussiano7x7.setCheckable(True)
        self.kernelGaussiano7x7.setChecked(False)
        self.kernelGaussiano7x7.triggered.connect(lambda: self.transformarImagem(
            self.kernelGaussiano7x7, 'Gaussiano7x7', self.extensaoImagemOriginal, 'ArgumentoVazio'))

        # Listar action
        self.listaFiltrosImgColoridaCinza.append(self.kernelGaussiano7x7)

    def criarActionFiltroDilatacao(self):
        self.filtroDilatacao = self.submenuMorfologicas.addAction("&Dilatação")
        self.filtroDilatacao.setShortcut("Ctrl+Alt+D")
        self.filtroDilatacao.setDisabled(True)
        self.filtroDilatacao.setCheckable(True)
        self.filtroDilatacao.setChecked(False)
        self.filtroDilatacao.triggered.connect(lambda: self.transformarImagem(
            self.filtroDilatacao, 'Dilatacao', self.extensaoImagemOriginal, 'ArgumentoVazio'))

        # Listar action
        self.listaFiltrosImgPretoBranco.append(self.filtroDilatacao)

    def criarActionFiltroErosao(self):
        self.filtroErosao = self.submenuMorfologicas.addAction("&Erosão")
        self.filtroErosao.setShortcut("Ctrl+Alt+E")
        self.filtroErosao.setDisabled(True)
        self.filtroErosao.setCheckable(True)
        self.filtroErosao.setChecked(False)
        self.filtroErosao.triggered.connect(lambda: self.transformarImagem(
            self.filtroErosao, 'Erosao', self.extensaoImagemOriginal, 'ArgumentoVazio'))

        # Listar action
        self.listaFiltrosImgPretoBranco.append(self.filtroErosao)

    def criarActionFiltroFechamento(self):
        self.filtroFechamento = self.submenuMorfologicas.addAction("&Fechamento")
        self.filtroFechamento.setShortcut("Ctrl+Alt+F")
        self.filtroFechamento.setDisabled(True)
        self.filtroFechamento.setCheckable(True)
        self.filtroFechamento.setChecked(False)
        self.filtroFechamento.triggered.connect(lambda: self.transformarImagem(
            self.filtroFechamento, 'Fechamento', self.extensaoImagemOriginal, 'ArgumentoVazio'))

        # Listar action
        self.listaFiltrosImgPretoBranco.append(self.filtroFechamento)

    def criarActionFiltroMediana(self):
        self.filtroMediana = self.submenuFiltrosDesfocar.addAction("Filtro &Mediana")
        self.filtroMediana.setShortcut("Ctrl+Shift+M")
        self.filtroMediana.setDisabled(True)
        self.filtroMediana.setCheckable(True)
        self.filtroMediana.setChecked(False)
        self.filtroMediana.triggered.connect(lambda: self.transformarImagem(
            self.filtroMediana, 'Mediana', self.extensaoImagemOriginal, 'ArgumentoVazio'))

        # Listar action
        self.listaFiltrosImgColoridaCinza.append(self.filtroMediana)

    def criarActionFiltroSharpen(self):
        self.filtroSharpen = self.submenuAjustarNitidez.addAction("Filtro S&harpen")
        self.filtroSharpen.setShortcut("Ctrl+Shift+H")
        self.filtroSharpen.setDisabled(True)
        self.filtroSharpen.setCheckable(True)
        self.filtroSharpen.setChecked(False)
        self.filtroSharpen.triggered.connect(lambda: self.transformarImagem(
            self.filtroSharpen, 'Sharpen', self.extensaoImagemOriginal, 'ArgumentoVazio'))

        # Listar action
        self.listaFiltrosImgColoridaCinza.append(self.filtroSharpen)

    def criarActionFiltroSobel(self):
        self.filtroSobel = self.submenuFiltrosDeteccaoBordas.addAction("Filtro S&obel")
        self.filtroSobel.setShortcut("Ctrl+Shift+O")
        self.filtroSobel.setDisabled(True)
        self.filtroSobel.setCheckable(True)
        self.filtroSobel.setChecked(False)
        self.filtroSobel.triggered.connect(self.janelaValorLimiteSobel)

        # Listar action
        self.listaFiltrosImgColoridaCinza.append(self.filtroSobel)

    def criarActionInverterNegativo(self):
        self.filtroNegativo = self.submenuInverterCores.addAction("&Negativo")
        self.filtroNegativo.setShortcut("Ctrl+Shift+N")
        self.filtroNegativo.setDisabled(True)
        self.filtroNegativo.setCheckable(True)
        self.filtroNegativo.setChecked(False)
        self.filtroNegativo.triggered.connect(lambda: self.transformarImagem(
            self.filtroNegativo, 'Negativo', self.extensaoImagemOriginal, 'ArgumentoVazio'))

        # Listar action
        self.listaFiltrosImgColoridaCinza.append(self.filtroNegativo)

    def criarActionTransformacaoLogaritmica(self):
        self.transformacaoLogaritmica = self.submenuRealcarIntensidade.addAction("Transformação &Logarítmica")
        self.transformacaoLogaritmica.setShortcut("Ctrl+Shift+L")
        self.transformacaoLogaritmica.setDisabled(True)
        self.transformacaoLogaritmica.setCheckable(True)
        self.transformacaoLogaritmica.setChecked(False)
        self.transformacaoLogaritmica.triggered.connect(lambda: self.transformarImagem(
            self.transformacaoLogaritmica, 'TransformacaoLogaritmica', self.extensaoImagemOriginal, 'ArgumentoVazio'))

        # Listar action
        self.listaFiltrosImgColoridaCinza.append(self.transformacaoLogaritmica)

    '''Gerar Layouts'''

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

    '''Abre imagem selecionada pelo usuário e mantêm oculta diretório que mantem cópias de imagens anteriores que foram 
    transformadas, também solicita habilitar visibilidade dos menus e ações, remoção de cópias de imagens anteriores 
    transformadas, zera porcentagem da barra de progresso, defini pixmap da Imagem a ser exibida'''

    def abrirImagem(self):
        global imagemResultado

        ocultarDiretorioImgResultado()

        global porcentagemProgresso
        arquivoImagem, _ = QFileDialog.getOpenFileName(self, caption="Abrir Imagem",
                                                       directory=QtCore.QDir.currentPath(),
                                                       filter='Imagens(*.ppm; *.pgm; *.pbm)',
                                                       initialFilter='Imagens(*.ppm; *.pgm; *.pbm)')

        if arquivoImagem:
            excluirCopiaImgTransformada()
            self.removerChecagemFiltrosUsados()
            porcentagemProgresso = 0
            self.barraProgresso.setValue(porcentagemProgresso)
            self.endImagemOriginal = arquivoImagem
            self.pixmapImagem = QPixmap(self.endImagemOriginal)
            self.extensaoImagemOriginal = os.path.splitext(os.path.basename(arquivoImagem))[1]
            self.exibirImagem()
            self.alterarVisibilidadeMenus()

    def removerChecagemFiltrosUsados(self):
        for filtro in self.listaFiltrosUsados:
            filtro.setChecked(False)

        self.listaFiltrosUsados.clear()

    '''Contolar quais submenus e actions estão visíveis dependendo do tipo da imagem'''

    def alterarVisibilidadeMenus(self):
        global extensaoImagemResultado

        self.opcaoInfoImagem.setVisible(True)
        self.opcaoSalvarComo.setDisabled(False)

        if self.extensaoImagemOriginal == '.ppm':
            if not self.listaFiltrosUsados:
                for filtro in self.listaFiltrosImgColoridaCinza:
                    filtro.setDisabled(False)

                for filtro in self.listaFiltrosImgPretoBranco:
                    if filtro not in self.listaFiltrosImgColoridaCinza:
                        filtro.setDisabled(True)

        elif self.extensaoImagemOriginal == '.pgm':
            for filtro in self.listaFiltrosImgColoridaCinza:
                if filtro in self.listaRemoverFiltrosParaEscalaDeCinza:
                    filtro.setDisabled(True)
                else:
                    filtro.setDisabled(False)

            for filtro in self.listaFiltrosImgPretoBranco:
                if filtro not in self.listaFiltrosImgColoridaCinza:
                    filtro.setDisabled(True)

        elif self.extensaoImagemOriginal == '.pbm':
            for filtro in self.listaFiltrosImgColoridaCinza:
                filtro.setDisabled(True)

            for filtro in self.listaFiltrosImgPretoBranco:
                filtro.setDisabled(False)

    def criarJanelaDesenharElementoEstruturante(self, totalLinhas, totalColunas, filtro, script, extensao):
        self.janelaDesenharElementoEstruturante = JanelaMatriz(totalLinhas, totalColunas)
        self.janelaDesenharElementoEstruturante.botaoEnviar.clicked.connect \
            (lambda: self.pegarMatrizElementoEstruturante(filtro, script, extensao))

    def pegarMatrizElementoEstruturante(self, filtro, script, extensao):
        stringMatrizElementoEstruturante = ''
        matrizElementoEstruturante = self.janelaDesenharElementoEstruturante.elemento

        for linha in range(len(matrizElementoEstruturante)):
            for coluna in range(len(matrizElementoEstruturante[linha])):
                stringMatrizElementoEstruturante += str(matrizElementoEstruturante[linha][coluna])

        self.janelaDesenharElementoEstruturante.close()
        self.transformarImagem(filtro, script, extensao, stringMatrizElementoEstruturante)

    '''Instancia classe ValorCorrecaoGama e pega valor fator gama 
    escolhido pelo usuário ao apertar botão enviar valor'''

    def janelaValorCorrecaoGama(self):
        self.janelaValorFatorGama = JanelaValorGama()
        self.janelaValorFatorGama.enviarValor.clicked.connect(self.pegarValorSliderGama)

    '''Pegar valor fator Gama escolhido pelo usuário e repassa-lo como linha de argumento para script 
    externo executar aplicação da correção gama na imagem'''

    def pegarValorSliderGama(self):
        valorFatorGama = str(self.janelaValorFatorGama.valorSlider)
        self.janelaValorFatorGama.close()
        self.transformarImagem(self.correcaoGama, 'CorrecaoGama', self.extensaoImagemOriginal, valorFatorGama)

    '''Instancia classe ValorCorrecaoGama e pega valor fator gama 
    escolhido pelo usuário ao apertar botão enviar valor'''

    def janelaValorLimiteSobel(self):
        self.janelaValorLimiteSobel = JanelaValorLimiteSobel()
        self.janelaValorLimiteSobel.enviarValor.clicked.connect(self.pegarValorLimiteSobel)

    '''Pegar valor fator Gama definido na classe ValorLimiteSobel'''

    def pegarValorLimiteSobel(self):
        valorLimiteSobel = str(self.janelaValorLimiteSobel.valorSlider)
        self.janelaValorLimiteSobel.close()
        self.transformarImagem(self.filtroSobel, 'Sobel', self.extensaoImagemOriginal, valorLimiteSobel)

    def janelaValorLimitePretoBranco(self):
        self.janelaValorLimitePretoBranco = JanelaValorLimitePretoBranco()
        self.janelaValorLimitePretoBranco.enviarValor.clicked.connect(self.pegarValorLimitePretoBranco)

    def pegarValorLimitePretoBranco(self):
        valorLimitePretoBranco = str(self.janelaValorLimitePretoBranco.valorSlider)
        self.janelaValorLimitePretoBranco.close()
        self.transformarImagem(self.converterParaPretoBranco, 'ConverterImagemBinaria', '.pbm', valorLimitePretoBranco)

    '''Exibe informações sobre aplicativo e imagem quando selecionado menu Sobre'''

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

                self.extrairInfoImagem()

                self.caixaMensagem.setText("Arquivo: " + self.nomeimagem + "\n" + "Tipo: " + self.tipoimagem +
                                           "Comentário: " + self.comentarioimagem + "Largura: " + self.larguraimagem \
                                           + "\n" + "Altura: " + self.alturaimagem)

                self.caixaMensagem.exec_()

    '''Salva Imagem com nome de arquivo e diretório escolhidos pelo usuário. Procura pela imagem transformada, caso
    não exista, é salvo a imagem original com o nome que o usuário escolher'''

    def salvarImagemComo(self):
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
                        os.renames(self.endImagemResultado, self.endereco + '/' +
                                   os.path.splitext(os.path.basename(imagemSalvaComo))[0] +
                                   extensaoImagemResultado)
                    else:
                        os.renames(self.endImagemOriginal, self.endereco + '/' +
                                   os.path.splitext(os.path.basename(imagemSalvaComo))[0] +
                                   self.extensaoImagemOriginal)
        except:
            pass

    def extrairInfoImagem(self):
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

    '''Repassa linhas de argumentos para scripts externos executar aplicação de filtros e transformações nas imagens, 
    controlando valores apresentados na barra de Progresso e de Status. Quando solicitado aplicação de mais de um 
    filtro na mesma imagem é gerado um cópia da imagem para não ter nomes repetidos nos argumentos utilizados
    nos scripts externos'''

    def transformarImagem(self, filtro, script, extensao, valorArgumento3):

        global porcentagemProgresso
        global imagemResultado
        global extensaoImagemResultado

        porcentagemProgresso = 0
        self.barraProgresso.setValue(porcentagemProgresso)
        self.filtroUsado = ''

        if os.path.exists(imagemResultado + "Copia" + extensaoImagemResultado):
            self.imagemEntrada = imagemResultado + "Copia" + extensaoImagemResultado
        else:
            self.imagemEntrada = self.endImagemOriginal

        try:
            if self.extensaoImagemOriginal == '.ppm':
                self.script = 'filtrosDeTransformacao/colorida/' + script + '.py'
                extensaoImagemResultado = extensao
                self.filtroUsado = filtro

            elif self.extensaoImagemOriginal == '.pgm':
                self.script = 'filtrosDeTransformacao/escalaCinza/' + script + '.py'
                extensaoImagemResultado = extensao
                self.filtroUsado = filtro

            elif self.extensaoImagemOriginal == '.pbm':
                self.script = 'filtrosDeTransformacao/pretoBranco/' + script + '.py'
                extensaoImagemResultado = extensao
                self.filtroUsado = filtro

            self.argumentos = 'python ' + self.script + ' \"' + self.imagemEntrada + '\" ' + \
                              imagemResultado + extensaoImagemResultado + ' \" ' + valorArgumento3
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
            self.listaFiltrosUsados.append(self.filtroUsado)
            self.extensaoImagemOriginal = extensaoImagemResultado
            self.alterarVisibilidadeMenus()

            self.barraStatus.showMessage("Aplicação " + self.filtroEscolhido.replace("&", "") +
                                         " finalizada", 5000)

        except:
            pass

    def exibirImagem(self):
        if self.pixmapImagem.width() > int(GetSystemMetrics(0) / 2) or \
                self.pixmapImagem.height() > int(GetSystemMetrics(1) / 2):
            self.pixmapImagem = self.pixmapImagem.scaled(int(GetSystemMetrics(0) / 2), int(GetSystemMetrics(1) / 2),
                                                         QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

        self.imagemOriginal.setPixmap(self.pixmapImagem)
        self.imagemOriginal.setAlignment(QtCore.Qt.AlignCenter)

    '''Excluir imagens cópias ao finalizar aplicativo'''

    def closeEvent(self, event):
        global listaFiltrosUsados
        excluirCopiaImgTransformada()


def main():
    app = QApplication(sys.argv)
    win = MyWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
