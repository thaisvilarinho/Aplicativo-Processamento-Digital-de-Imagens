import fnmatch
import glob
import os
import shutil
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer

from ControleChecagemFiltros import ControleChecagemFiltros
from ControleVisibilidadeItens import ControleVisibilidadeItens
from ItensMenuTransformacoes import ItensMenuTransformacoes
from ManipulacaoImagens import ManipulacaoImagens
from TransformacaoImagens import TransformacaoImagens


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setWindowTitle("Processamento Digital de Imagens - IFTM")
        self.icon = self.setWindowIcon(QIcon("icones/icon.jpg"))
        self.setGeometry(450, 150, 800, 600)
        self.initUI()



        self.show()

    def criarInstancias(self):
        # Instâncias classes
        self.controleVisibilidadeItens = ControleVisibilidadeItens(self.opcaoInfoImagem, self.opcaoSalvarComo)
        self.controleChecagemFiltros = ControleChecagemFiltros()
        self.manipulacaoImagens = ManipulacaoImagens(self.imagemOriginal, self.controleVisibilidadeItens,
                                                     self.controleChecagemFiltros)
        self.transformacaoImagens = TransformacaoImagens(self.manipulacaoImagens, self.barraProgresso, self.barraStatus)
        self.itensBarraMenu = ItensMenuTransformacoes(self.controleVisibilidadeItens, self.manipulacaoImagens,
                                                      self.menuTransformacao, self.transformacaoImagens)


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
        self.opcaoAbrir.setShortcut("Ctrl+A")

        self.opcaoRecente = self.menuArquivo.addMenu("Abrir &Recente")
        self.abrirRecente = self.opcaoRecente.addAction("arquivos...")
        self.abrirRecente.setDisabled(True)

        self.opcaoSalvarComo = self.menuArquivo.addAction("&Salvar como")
        self.opcaoSalvarComo.setShortcut("Ctrl+S")
        self.opcaoSalvarComo.setDisabled(True)

        self.menuArquivo.addSeparator()
        self.opcaoFechar = self.menuArquivo.addAction("F&echar")
        self.opcaoFechar.setShortcut("Esc")
        self.opcaoFechar.triggered.connect(self.close)

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

        self.criarInstancias()

        # Criando conexao menus com métodos de outras classes
        self.opcaoAbrir.triggered.connect(self.manipulacaoImagens.abrirImagem)
        self.opcaoSalvarComo.triggered.connect(self.manipulacaoImagens.salvarImagemComo)

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
            if self.manipulacaoImagens.endImagemOriginal != '':
                self.caixaMensagem.setWindowTitle("Informações da Imagem")

                self.caixaMensagem.setText("Arquivo: " + self.manipulacaoImagens.nomeimagem + "\n" + "Tipo: " +
                                           self.manipulacaoImagens.tipoimagem + "Comentário: " +
                                           self.manipulacaoImagens.comentarioimagem +
                                           "Largura: " + self.manipulacaoImagens.larguraimagem + "\n" + "Altura: "
                                           + self.manipulacaoImagens.alturaimagem)

                self.caixaMensagem.exec_()

    def close(self):
        self.manipulacaoImagens.excluirCopiaImgTransformada()

        if self.manipulacaoImagens.procurarImagemTransformadaNaoSalva():
            caixaAviso = QMessageBox.question(self, "Sair do Aplicativo",
                                                   "Há uma imagem transformada sem salvar, "
                                                   "deseja salvar imagem antes de sair?",
                                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if caixaAviso == QMessageBox.Yes:
                self.manipulacaoImagens.salvarImagemComo()

        self.manipulacaoImagens.excluirImagemTransformadaNaoSalva()
        sys.exit()



def main():
    app = QApplication(sys.argv)
    win = MyWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
