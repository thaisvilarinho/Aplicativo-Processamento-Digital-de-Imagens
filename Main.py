import sys
import os
import shutil
import subprocess
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
from win32api import GetSystemMetrics
from ValorCorrecaoGama import JanelaValorGama
from ValorLimiteSobel import JanelaValorLimiteSobel

porcentagemProgresso = 0
imagemResultado = 'imagensResultado/imagemTransformada'
extensaoImagemResultado = '.ppm'


def excluirCopiaImgTransformada():
    global imagemResultado
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
        self.criarWidgets()
        self.gerarLayouts()

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

        self.criarSubmenuAjusteNitidez()
        self.criarSubmenuAjusteLuminancia()
        self.criarSubmenuConversao()
        self.criarSubmenuDecomporCanaisRGB()
        self.criarSubmenuDesfocar()
        self.criarSubmenuDeteccaoDeBordas()
        self.criarActionFiltroNegativo()
        self.criarActionTransformacaoLogaritmica()
        self.criarActionTransformacaoMorfologica()

        self.criarListasChecagemFiltros()

    '''Criar Submenus'''

    def criarSubmenuAjusteNitidez(self):
        # Submenu
        self.submenuAjusteNitidez = self.menuTransformacao.addMenu("Ajuste Nitide&z")
        self.submenuAjusteNitidez.setDisabled(True)

        # Actions do submenu
        self.criarActionFiltroSharpen()

    def criarSubmenuAjusteLuminancia(self):
        # Submenu
        self.submenuAjusteLuminancia = self.menuTransformacao.addMenu("A&juste Luminância")
        self.submenuAjusteLuminancia.setDisabled(True)

        # Actions do submenu
        self.criarActionCorrecaoGama()

    def criarSubmenuConversao(self):
        # Submenu
        self.submenuConversao = self.menuTransformacao.addMenu("Con&verter")
        self.submenuConversao.setDisabled(True)

        # Actions do submenu
        self.criarActionConverterParaEscalaCinza()
        self.criarActionConverterParaPretoBranco()

    def criarSubmenuDecomporCanaisRGB(self):
        # Submenu
        self.submenuDecomposicaoCanaisRGB = self.menuTransformacao.addMenu("Decomposição &Canais RGB")
        self.submenuDecomposicaoCanaisRGB.setDisabled(True)

        # Actions do submenu
        self.criarActionDecomporCanalR()
        self.criarActionDecomporCanalG()
        self.criarActionDecomporCanalB()

    def criarSubmenuDesfocar(self):
        # Submenu
        self.submenuFiltrosDesfocar = self.menuTransformacao.addMenu("Filtros de Des&focar")
        self.submenuFiltrosDesfocar.setDisabled(True)

        # Actions do submenu
        self.criarSubmenuFiltroGaussiano()
        self.criarActionFiltroMediana()

    def criarSubmenuDeteccaoDeBordas(self):
        # Submenu
        self.submenuFiltrosDeteccaoBordas = self.menuTransformacao.addMenu("Filtros &Detecção de Bordas")
        self.submenuFiltrosDeteccaoBordas.setDisabled(True)

        # Actions do submenu
        self.criarActionDeteccaoDeBordasCrono()
        self.criarActionDeteccaoDeBordasMarle()
        self.criarActionDeteccaoDeBordasPrometheus()
        self.criarActionFiltroSobel()

    def criarSubmenuFiltroGaussiano(self):
        # Submenu
        self.submenuFiltroGaussiano = self.submenuFiltrosDesfocar.addMenu("Filtro Ga&ussiano")
        self.submenuFiltroGaussiano.setDisabled(True)

        # Actions do submenu
        self.criarActionKernelGaussiano3x3()
        self.criarActionKernelGaussiano5x5()
        self.criarActionKernelGaussiano7x7()

    '''Criar Actions'''

    def criarActionConverterParaEscalaCinza(self):
        self.converterParaEscalaCinza = self.submenuConversao.addAction("Converter para Escala de C&inza")
        self.converterParaEscalaCinza.setShortcut("Ctrl+Shift+I")
        self.converterParaEscalaCinza.setDisabled(True)
        self.converterParaEscalaCinza.setCheckable(True)
        self.converterParaEscalaCinza.setChecked(False)
        self.converterParaEscalaCinza.triggered.connect(lambda: self.transformarImagem(
            self.converterParaEscalaCinza, 'ConverterEscalaDeCinza', '.pgm', 'ArgumentoVazio'))

    def criarActionConverterParaPretoBranco(self):
        self.converterParaPretoBranco = self.submenuConversao.addAction("Converter Para Pre&to e Branco")
        self.converterParaPretoBranco.setShortcut("Ctrl+Shift+T")
        self.converterParaPretoBranco.setDisabled(True)
        self.converterParaPretoBranco.setCheckable(True)
        self.converterParaPretoBranco.setChecked(False)
        self.converterParaPretoBranco.triggered.connect(lambda: self.transformarImagem(
            self.converterParaPretoBranco, 'ConverterImagemBinaria', '.pbm', 'ArgumentoVazio'))

    def criarActionCorrecaoGama(self):
        self.correcaoGama = self.submenuAjusteLuminancia.addAction("Correção &Gama")
        self.correcaoGama.setShortcut("Ctrl+Shift+G")
        self.correcaoGama.setDisabled(True)
        self.correcaoGama.setCheckable(True)
        self.correcaoGama.setChecked(False)
        self.correcaoGama.triggered.connect(self.janelaValorCorrecaoGama)

    def criarActionDecomporCanalR(self):
        self.decomporCanalR = self.submenuDecomposicaoCanaisRGB.addAction("Vermelho")
        self.decomporCanalR.setShortcut("Ctrl+Alt+R")
        self.decomporCanalR.setCheckable(True)
        self.decomporCanalR.setChecked(False)
        self.decomporCanalR.triggered.connect(lambda: self.transformarImagem(
            self.decomporCanalR, 'CamadaR', '.ppm', 'ArgumentoVazio'))

    def criarActionDecomporCanalG(self):
        self.decomporCanalG = self.submenuDecomposicaoCanaisRGB.addAction("Verde")
        self.decomporCanalG.setShortcut("Ctrl+Alt+G")
        self.decomporCanalG.setCheckable(True)
        self.decomporCanalG.setChecked(False)
        self.decomporCanalG.triggered.connect(lambda: self.transformarImagem(
            self.decomporCanalG, 'CamadaG', '.ppm', 'ArgumentoVazio'))

    def criarActionDecomporCanalB(self):
        self.decomporCanalB = self.submenuDecomposicaoCanaisRGB.addAction("Azul")
        self.decomporCanalB.setShortcut("Ctrl+Alt+B")
        self.decomporCanalB.setCheckable(True)
        self.decomporCanalB.setChecked(False)
        self.decomporCanalB.triggered.connect(lambda: self.transformarImagem(
            self.decomporCanalB, 'CamadaB', '.ppm', 'ArgumentoVazio'))

    def criarActionDeteccaoDeBordasCrono(self):
        self.deteccaoDeBordasFiltroCrono = self.submenuFiltrosDeteccaoBordas.addAction("Crono")
        self.deteccaoDeBordasFiltroCrono.setShortcut("Ctrl+Alt+C")
        self.deteccaoDeBordasFiltroCrono.setCheckable(True)
        self.deteccaoDeBordasFiltroCrono.setChecked(False)
        self.deteccaoDeBordasFiltroCrono.triggered.connect(lambda: self.transformarImagem(
            self.deteccaoDeBordasFiltroCrono, 'DeteccaoDeBordasCrono', self.extensaoImagemOriginal, 'ArgumentoVazio'))

    def criarActionDeteccaoDeBordasMarle(self):
        self.deteccaoDeBordasFiltroMarle = self.submenuFiltrosDeteccaoBordas.addAction("Marle")
        self.deteccaoDeBordasFiltroMarle.setShortcut("Ctrl+Alt+M")
        self.deteccaoDeBordasFiltroMarle.setCheckable(True)
        self.deteccaoDeBordasFiltroMarle.setChecked(False)
        self.deteccaoDeBordasFiltroMarle.triggered.connect(lambda: self.transformarImagem(
            self.deteccaoDeBordasFiltroMarle, 'DeteccaoDeBordasMarle', self.extensaoImagemOriginal, 'ArgumentoVazio'))

    def criarActionDeteccaoDeBordasPrometheus(self):
        self.deteccaoDeBordasFiltroPrometheus = self.submenuFiltrosDeteccaoBordas.addAction("Prometheus")
        self.deteccaoDeBordasFiltroPrometheus.setShortcut("Ctrl+Alt+P")
        self.deteccaoDeBordasFiltroPrometheus.setCheckable(True)
        self.deteccaoDeBordasFiltroPrometheus.setChecked(False)
        self.deteccaoDeBordasFiltroPrometheus.triggered.connect(lambda: self.transformarImagem(
            self.deteccaoDeBordasFiltroPrometheus, 'DeteccaoDeBordasPrometheus', self.extensaoImagemOriginal,
            'ArgumentoVazio'))

    def criarActionKernelGaussiano3x3(self):
        self.kernelGaussiano3x3 = self.submenuFiltroGaussiano.addAction("Matriz 3x3")
        self.kernelGaussiano3x3.setShortcut("Ctrl+Alt+3")
        self.kernelGaussiano3x3.setCheckable(True)
        self.kernelGaussiano3x3.setChecked(False)
        self.kernelGaussiano3x3.triggered.connect(lambda: self.transformarImagem(
            self.kernelGaussiano3x3, 'Gaussiano3x3', self.extensaoImagemOriginal, 'ArgumentoVazio'))

    def criarActionKernelGaussiano5x5(self):
        self.kernelGaussiano5x5 = self.submenuFiltroGaussiano.addAction("Matriz 5x5")
        self.kernelGaussiano5x5.setShortcut("Ctrl+Alt+5")
        self.kernelGaussiano5x5.setCheckable(True)
        self.kernelGaussiano5x5.setChecked(False)
        self.kernelGaussiano5x5.triggered.connect(lambda: self.transformarImagem(
            self.kernelGaussiano5x5, 'Gaussiano5x5', self.extensaoImagemOriginal, 'ArgumentoVazio'))

    def criarActionKernelGaussiano7x7(self):
        self.kernelGaussiano7x7 = self.submenuFiltroGaussiano.addAction("Matriz 7x7")
        self.kernelGaussiano7x7.setShortcut("Ctrl+Alt+7")
        self.kernelGaussiano7x7.setCheckable(True)
        self.kernelGaussiano7x7.setChecked(False)
        self.kernelGaussiano7x7.triggered.connect(lambda: self.transformarImagem(
            self.kernelGaussiano7x7, 'Gaussiano7x7', self.extensaoImagemOriginal, 'ArgumentoVazio'))

    def criarActionFiltroMediana(self):
        self.filtroMediana = self.submenuFiltrosDesfocar.addAction("Filtro &Mediana")
        self.filtroMediana.setShortcut("Ctrl+Shift+M")
        self.filtroMediana.setDisabled(True)
        self.filtroMediana.setCheckable(True)
        self.filtroMediana.setChecked(False)
        self.filtroMediana.triggered.connect(lambda: self.transformarImagem(
            self.filtroMediana, 'Mediana', self.extensaoImagemOriginal, 'ArgumentoVazio'))

    def criarActionFiltroNegativo(self):
        self.filtroNegativo = self.menuTransformacao.addAction("Filtro &Negativo")
        self.filtroNegativo.setShortcut("Ctrl+Shift+N")
        self.filtroNegativo.setDisabled(True)
        self.filtroNegativo.setCheckable(True)
        self.filtroNegativo.setChecked(False)
        self.filtroNegativo.triggered.connect(lambda: self.transformarImagem(
            self.filtroNegativo, 'Negativo', self.extensaoImagemOriginal, 'ArgumentoVazio'))

    def criarActionFiltroSharpen(self):
        self.filtroSharpen = self.submenuAjusteNitidez.addAction("Filtro S&harpen")
        self.filtroSharpen.setShortcut("Ctrl+Shift+H")
        self.filtroSharpen.setDisabled(True)
        self.filtroSharpen.setCheckable(True)
        self.filtroSharpen.setChecked(False)
        self.filtroSharpen.triggered.connect(lambda: self.transformarImagem(
            self.filtroSharpen, 'Sharpen', self.extensaoImagemOriginal, 'ArgumentoVazio'))

    def criarActionFiltroSobel(self):
        self.filtroSobel = self.submenuFiltrosDeteccaoBordas.addAction("Filtro S&obel")
        self.filtroSobel.setShortcut("Ctrl+Shift+O")
        self.filtroSobel.setDisabled(True)
        self.filtroSobel.setCheckable(True)
        self.filtroSobel.setChecked(False)
        self.filtroSobel.triggered.connect(self.janelaValorLimiteSobel)

    def criarActionTransformacaoLogaritmica(self):
        self.transformacaoLogaritmica = self.menuTransformacao.addAction("Transformação &Logarítmica")
        self.transformacaoLogaritmica.setShortcut("Ctrl+Shift+L")
        self.transformacaoLogaritmica.setDisabled(True)
        self.transformacaoLogaritmica.setCheckable(True)
        self.transformacaoLogaritmica.setChecked(False)
        self.transformacaoLogaritmica.triggered.connect(lambda: self.transformarImagem(
            self.transformacaoLogaritmica, 'TransformacaoLogaritmica', self.extensaoImagemOriginal, 'ArgumentoVazio'))

    def criarActionTransformacaoMorfologica(self):
        self.transformacaoMorfologica = self.menuTransformacao.addAction("Transformações &Morfológicas")
        self.transformacaoMorfologica.setShortcut("Ctrl+Shift+M")
        self.transformacaoMorfologica.setDisabled(True)
        self.transformacaoMorfologica.setCheckable(True)
        self.transformacaoMorfologica.setChecked(False)
        self.transformacaoMorfologica.triggered.connect(lambda: self.transformarImagem(
            self.transformacaoMorfologica, 'BordasDilatacao', '.pbm', 'ArgumentoVazio'))

    def criarListasChecagemFiltros(self):
        self.listaFiltrosImgColoridaCinza = [self.submenuAjusteNitidez, self.filtroSharpen,
                                             self.submenuAjusteLuminancia, self.correcaoGama,
                                             self.submenuConversao, self.converterParaEscalaCinza,
                                             self.converterParaPretoBranco, self.submenuFiltrosDesfocar,
                                             self.submenuFiltroGaussiano, self.kernelGaussiano3x3,
                                             self.kernelGaussiano5x5, self.kernelGaussiano7x7, self.filtroMediana,
                                             self.filtroNegativo, self.transformacaoLogaritmica,
                                             self.submenuFiltrosDeteccaoBordas, self.deteccaoDeBordasFiltroCrono,
                                             self.deteccaoDeBordasFiltroMarle, self.deteccaoDeBordasFiltroPrometheus,
                                             self.filtroSobel, self.submenuDecomposicaoCanaisRGB,
                                             self.decomporCanalR, self.decomporCanalG, self.decomporCanalB]

        self.listaFiltrosImgPretoBranco = [self.submenuFiltrosDeteccaoBordas, self.deteccaoDeBordasFiltroCrono,
                                           self.deteccaoDeBordasFiltroMarle, self.deteccaoDeBordasFiltroPrometheus,
                                           self.transformacaoMorfologica]

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

            self.transformacaoMorfologica.setDisabled(True)

        elif self.extensaoImagemOriginal == '.pgm':
            for filtro in self.listaFiltrosImgColoridaCinza:
                filtro.setDisabled(False)
            self.submenuDecomposicaoCanaisRGB.setDisabled(True)
            self.decomporCanalR.setDisabled(True)
            self.decomporCanalG.setDisabled(True)
            self.decomporCanalB.setDisabled(True)
            self.converterParaEscalaCinza.setDisabled(True)
            self.transformacaoMorfologica.setDisabled(True)

        elif self.extensaoImagemOriginal == '.pbm':
            for filtro in self.listaFiltrosImgColoridaCinza:
                filtro.setDisabled(True)

            for filtro in self.listaFiltrosImgPretoBranco:
                filtro.setDisabled(False)

    '''Instancia classe ValorCorrecaoGama e pega valor fator gama 
    escolhido pelo usuário ao apertar botão enviar valor'''
    def janelaValorCorrecaoGama(self):
        self.janelaGama = JanelaValorGama()
        self.janelaGama.enviarValor.clicked.connect(self.pegarValorSliderGama)

    '''Pegar valor fator Gama escolhido pelo usuário e repassa-lo como linha de argumento para script 
    externo executar aplicação da correção gama na imagem'''
    def pegarValorSliderGama(self):
        valorFatorGama = str(self.janelaGama.valorSlider)
        self.janelaGama.close()
        self.transformarImagem(self.correcaoGama, 'CorrecaoGama', self.extensaoImagemOriginal, valorFatorGama)

    '''Instancia classe ValorCorrecaoGama e pega valor fator gama 
    escolhido pelo usuário ao apertar botão enviar valor'''
    def janelaValorLimiteSobel(self):
        self.janelaSobel = JanelaValorLimiteSobel()
        self.janelaSobel.enviarValor.clicked.connect(self.pegarValorLimiteSobel)

    '''Pegar valor fator Gama definido na classe ValorLimiteSobel'''
    def pegarValorLimiteSobel(self):
        valorLimiteSobel = str(self.janelaSobel.valorSlider)
        self.janelaSobel.close()
        self.transformarImagem(self.filtroSobel, 'Sobel', self.extensaoImagemOriginal, valorLimiteSobel)

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

        '''Salva Cópia de Imagem com nome de arquivo e diretório escolhidos pelo usuário'''
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
                        shutil.copyfile(self.endImagemResultado, self.endereco + '/' +
                                        os.path.splitext(os.path.basename(imagemSalvaComo))[0] +
                                        extensaoImagemResultado)
                    else:
                        shutil.copyfile(self.endImagemOriginal, self.endereco + '/' +
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
