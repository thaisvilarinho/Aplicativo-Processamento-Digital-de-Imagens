import os
import shutil
from win32api import GetSystemMetrics
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap


def ocultarDiretorioImgResultado():
    os.system("attrib +h " + 'imagensResultado')


class ManipulacaoImagens(QWidget):
    def __init__(self, imagemExibida, controleVisibilidadeItens, controleChecagemFiltros, submenuAbrirRecente,
                 barraStatus):
        super(ManipulacaoImagens, self).__init__()
        self.imagemExibida = imagemExibida
        self.controleVisibilidadeItens = controleVisibilidadeItens
        self.controleChecagemFiltros = controleChecagemFiltros
        self.submenuAbrirRecente = submenuAbrirRecente
        self.barraStatus = barraStatus
        self.imagemResultado = 'imagensResultado/imagemTransformada'
        self.extensaoImagemResultado = '.ppm'
        self.extensaoImagemOriginal = ''
        self.endImagemOriginal = ''
        self.endImagemResultado = ''
        self.listaImagensRecentes = []
        self.rotacao = 0

    '''Abre imagem selecionada pelo usuário'''

    def abrirImagem(self):
        ocultarDiretorioImgResultado()

        arquivoImagemAberta, tipos = QFileDialog.getOpenFileName(self, caption="Abrir Imagem",
                                                                 directory=QtCore.QDir.currentPath(),
                                                                 filter='Imagens(*.ppm; *.pgm; *.pbm)',
                                                                 initialFilter='Imagens(*.ppm; *.pgm; *.pbm)')

        if arquivoImagemAberta:
            self.excluirCopiaImgTransformada()
            self.controleChecagemFiltros.removerChecagemFiltrosUsados()
            self.substituirEnderecoImgOriginal(arquivoImagemAberta)
            self.controlarListaImagensRecentes(arquivoImagemAberta)
            self.controleVisibilidadeItens.alterarVisibilidadeItensMenuTransformacoes(self.extensaoImagemOriginal)

    def substituirEnderecoImgOriginal(self, arquivoImagemAberta):
        self.endImagemOriginal = arquivoImagemAberta
        self.pixmapImagem = QPixmap(self.endImagemOriginal)
        self.extensaoImagemOriginal = os.path.splitext(os.path.basename(arquivoImagemAberta))[1]
        self.exibirImagem()
        self.extrairInfoImagem()
        self.barraStatus.showMessage('Usuário carregou a imagem ' + self.nomeimagem, 3000)

    def controlarListaImagensRecentes(self, arquivoImagemRecente):
        imagemRecente = ''
        if arquivoImagemRecente not in self.listaImagensRecentes:
            self.listaImagensRecentes.append(arquivoImagemRecente)

            for arquivo in self.listaImagensRecentes:
                imagemRecente = QtWidgets.QAction(arquivo, self)
            self.submenuAbrirRecente.addAction(imagemRecente)
            imagemRecente.triggered.connect(lambda: self.abrirImagemRecente(arquivo))

    def abrirImagemRecente(self, arquivoImagemAberta):
        self.excluirCopiaImgTransformada()
        self.substituirEnderecoImgOriginal(arquivoImagemAberta)
        self.controleChecagemFiltros.removerChecagemFiltrosUsados()
        self.controleVisibilidadeItens.alterarVisibilidadeItensMenuTransformacoes(self.extensaoImagemOriginal)

    '''Exibe informações sobre aplicativo e imagem quando selecionado menu Sobre'''

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

    def exibirImagem(self):
        if self.pixmapImagem.width() > int(GetSystemMetrics(0) / 2) or \
                self.pixmapImagem.height() > int(GetSystemMetrics(1) / 2):
            self.pixmapImagem = self.pixmapImagem.scaled(int(GetSystemMetrics(0) / 2), int(GetSystemMetrics(1) / 2),
                                                         QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

        self.imagemExibida.setPixmap(self.pixmapImagem)
        self.imagemExibida.setAlignment(QtCore.Qt.AlignCenter)

    '''Salva Imagem com nome de arquivo e diretório escolhidos pelo usuário. Procura pela imagem transformada, caso
    não exista, é salvo a imagem original com o nome que o usuário escolher'''

    def salvarImagemComo(self):
        try:
            if self.endImagemOriginal != '':
                imagemSalvaComo, tipos = QFileDialog.getSaveFileName(self, caption='Salvar como',
                                                                     directory=QtCore.QDir.currentPath(),
                                                                     filter='Imagens(*.ppm; *.pgm; *.pbm)',
                                                                     initialFilter='Imagens(*.ppm; *.pgm; *.pbm)')
                if imagemSalvaComo:
                    self.parts = imagemSalvaComo.rpartition('/')
                    self.enderecoSalvo = self.parts[0]
                    nomeImagemSalva = os.path.splitext(os.path.basename(imagemSalvaComo))[0]
                    novoDiretorio = ''

                    if self.endImagemResultado != '':
                        novoDiretorio = self.enderecoSalvo + '/' + nomeImagemSalva + self.extensaoImagemResultado
                        shutil.move(self.endImagemResultado, novoDiretorio)
                    else:
                        novoDiretorio = self.enderecoSalvo + '/' + nomeImagemSalva + self.extensaoImagemOriginal
                        shutil.copyfile(self.endImagemOriginal, novoDiretorio)

                    self.barraStatus.showMessage('Usuário salvou a imagem como ' + nomeImagemSalva +
                                                 self.extensaoImagemResultado, 3000)
                    self.controlarListaImagensRecentes(novoDiretorio)
        except:
            pass

    def procurarImagemTransformadaNaoSalva(self):
        return os.path.exists(self.imagemResultado + self.extensaoImagemResultado)

    def excluirCopiaImgTransformada(self):
        try:
            if os.path.exists(self.imagemResultado + "Copia" + '.ppm'):
                os.remove(self.imagemResultado + "Copia" + '.ppm')

            if os.path.exists(self.imagemResultado + "Copia" + '.pgm'):
                os.remove(self.imagemResultado + "Copia" + '.pgm')

            if os.path.exists(self.imagemResultado + "Copia" + '.pbm'):
                os.remove(self.imagemResultado + "Copia" + '.pbm')

        except:
            pass

    def excluirImagemTransformadaNaoSalva(self):
        try:
            if os.path.exists(self.imagemResultado + '.ppm'):
                os.remove(self.imagemResultado + '.ppm')

            if os.path.exists(self.imagemResultado + '.pgm'):
                os.remove(self.imagemResultado + '.pgm')

            if os.path.exists(self.imagemResultado + '.pbm'):
                os.remove(self.imagemResultado + '.pbm')
        except:
            pass
