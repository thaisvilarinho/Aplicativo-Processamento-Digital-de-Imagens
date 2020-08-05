from JanelaMatrizElementoEstruturante import JanelaMatrizElementoEstruturante
from JanelaValorGama import JanelaValorGama
from JanelaValorLimitePretoBranco import JanelaValorLimitePretoBranco
from JanelaValorLimiteSobel import JanelaValorLimiteSobel


class ItensMenuTransformacoes():
    def __init__(self, controleVisibilidadeItens, manipulacaoImagens, menuTransformacao, transformacaoImagens):
        super(ItensMenuTransformacoes, self).__init__()
        self.controleVisibilidadeItens = controleVisibilidadeItens
        self.manipulacaoImagens = manipulacaoImagens
        self.menuTransformacao = menuTransformacao
        self.transformacaoImagens = transformacaoImagens

        self.criarSubmenus()

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
        self.controleVisibilidadeItens.listaFiltrosImgColoridaCinza.append(self.submenuAjustarNitidez)

    def criarSubmenuRealcarIntensidade(self):
        # Submenu
        self.submenuRealcarIntensidade = self.menuTransformacao.addMenu("Real&çar Intensidade")
        self.submenuRealcarIntensidade.setDisabled(True)

        # Actions do submenu
        self.criarActionCorrecaoGama()
        self.criarActionTransformacaoLogaritmica()

        # Listar submenu
        self.controleVisibilidadeItens.listaFiltrosImgColoridaCinza.append(self.submenuRealcarIntensidade)

    def criarSubmenuConversao(self):
        # Submenu
        self.submenuConversao = self.menuTransformacao.addMenu("Con&verter")
        self.submenuConversao.setDisabled(True)

        # Actions do submenu
        self.criarActionConverterParaEscalaCinza()
        self.criarActionConverterParaPretoBranco()

        # Listar submenu
        self.controleVisibilidadeItens.listaFiltrosImgColoridaCinza.append(self.submenuConversao)

    def criarSubmenuDecomporCanaisRGB(self):
        # Submenu
        self.submenuDecomposicaoCanaisRGB = self.menuTransformacao.addMenu("Decomposição &Canais RGB")
        self.submenuDecomposicaoCanaisRGB.setDisabled(True)

        # Actions do submenu
        self.criarActionDecomporCanalR()
        self.criarActionDecomporCanalG()
        self.criarActionDecomporCanalB()

        # Listar submenu
        self.controleVisibilidadeItens.listaFiltrosImgColoridaCinza.append(self.submenuDecomposicaoCanaisRGB)
        self.controleVisibilidadeItens.listaRemoverFiltrosParaEscalaDeCinza.append(self.submenuDecomposicaoCanaisRGB)

    def criarSubmenuDesfocar(self):
        # Submenu
        self.submenuFiltrosDesfocar = self.menuTransformacao.addMenu("Des&focar")
        self.submenuFiltrosDesfocar.setDisabled(True)

        # Criar novo submenu
        self.criarSubmenuFiltroGaussiano()
        # Actions do submenu
        self.criarActionFiltroMediana()

        # Listar submenu
        self.controleVisibilidadeItens.listaFiltrosImgColoridaCinza.append(self.submenuFiltrosDesfocar)

    def criarSubmenuDeteccaoDeBordas(self):
        # Submenu
        self.submenuFiltrosDeteccaoBordas = self.menuTransformacao.addMenu("&Detectar Bordas")
        self.submenuFiltrosDeteccaoBordas.setDisabled(True)

        # Actions do submenu
        self.criarActionDeteccaoDeBordasCrono()
        self.criarActionDeteccaoDeBordasMarle()
        self.criarActionDeteccaoDeBordasPrometheus()
        self.criarActionFiltroSobel()

        # Criar novos submenus
        self.criarSubmenuDeteccaoDeBordasDilatacao()
        self.criarSubmenuDeteccaoDeBordasErosao()


        # Listar submenu
        self.controleVisibilidadeItens.listaFiltrosImgColoridaCinza.append(self.submenuFiltrosDeteccaoBordas)
        self.controleVisibilidadeItens.listaFiltrosImgPretoBranco.append(self.submenuFiltrosDeteccaoBordas)

    def criarSubmenuFiltroGaussiano(self):
        # Submenu
        self.submenuFiltroGaussiano = self.submenuFiltrosDesfocar.addMenu("Filtro Ga&ussiano")
        self.submenuFiltroGaussiano.setDisabled(True)

        # Actions do submenu
        self.criarActionKernelGaussiano3x3()
        self.criarActionKernelGaussiano5x5()
        self.criarActionKernelGaussiano7x7()

        # Listar submenu
        self.controleVisibilidadeItens.listaFiltrosImgColoridaCinza.append(self.submenuFiltroGaussiano)

    def criarSubmenuInverterCores(self):
        # Submenu
        self.submenuInverterCores = self.menuTransformacao.addMenu("Inverter Cores")
        self.submenuInverterCores.setDisabled(True)

        # Actions do submenu
        self.criarActionInverterNegativo()

        # Listar submenu
        self.controleVisibilidadeItens.listaFiltrosImgColoridaCinza.append(self.submenuInverterCores)

    def criarSubmenuMorfologicas(self):
        # Submenu
        self.submenuMorfologicas = self.menuTransformacao.addMenu("&Morfológicas")
        self.submenuMorfologicas.setDisabled(True)

        # Submenus
        self.criarSubmenuAbertura()
        self.criarSubmenuDilatacao()
        self.criarSubmenuErosao()
        self.criarSubmenuFechamento()

        # Listar submenu
        self.controleVisibilidadeItens.listaFiltrosImgPretoBranco.append(self.submenuMorfologicas)

    def criarSubmenuAbertura(self):
        self.submenuFiltroAbertura = self.submenuMorfologicas.addMenu("&Abertura")
        self.submenuFiltroAbertura.setDisabled(True)

        # Actions do submenu
        self.criarActionAberturaElementoEstrutura3x3()
        self.criarActionAberturaElementoEstrutura5x5()
        self.criarActionAberturaElementoEstrutura7x7()
        self.criarActionAberturaElementoEstrutura9x9()

        # Listar submenu
        self.controleVisibilidadeItens.listaFiltrosImgPretoBranco.append(self.submenuFiltroAbertura)

    def criarSubmenuDilatacao(self):
        self.submenuFiltroDilatacao = self.submenuMorfologicas.addMenu("&Dilatação")
        self.submenuFiltroDilatacao.setDisabled(True)

        # Actions do submenu
        self.criarActionDilatacaoElementoEstrutura3x3()
        self.criarActionDilatacaoElementoEstrutura5x5()
        self.criarActionDilatacaoElementoEstrutura7x7()
        self.criarActionDilatacaoElementoEstrutura9x9()

        # Listar submenu
        self.controleVisibilidadeItens.listaFiltrosImgPretoBranco.append(self.submenuFiltroDilatacao)

    def criarSubmenuErosao(self):
        self.submenuFiltroErosao = self.submenuMorfologicas.addMenu("&Erosão")
        self.submenuFiltroErosao.setDisabled(True)

        # Actions do submenu
        self.criarActionErosaoElementoEstrutura3x3()
        self.criarActionErosaoElementoEstrutura5x5()
        self.criarActionErosaoElementoEstrutura7x7()
        self.criarActionErosaoElementoEstrutura9x9()

        # Listar submenu
        self.controleVisibilidadeItens.listaFiltrosImgPretoBranco.append(self.submenuFiltroErosao)

    def criarSubmenuFechamento(self):
        self.submenuFiltroFechamento = self.submenuMorfologicas.addMenu("&Fechamento")
        self.submenuFiltroFechamento.setDisabled(True)

        # Actions do submenu
        self.criarActionFechamentoElementoEstrutura3x3()
        self.criarActionFechamentoElementoEstrutura5x5()
        self.criarActionFechamentoElementoEstrutura7x7()
        self.criarActionFechamentoElementoEstrutura9x9()

        # Listar submenu
        self.controleVisibilidadeItens.listaFiltrosImgPretoBranco.append(self.submenuFiltroFechamento)

    def criarSubmenuDeteccaoDeBordasDilatacao(self):
        self.submenuDeteccaoDeBordasDilatacao = self.submenuFiltrosDeteccaoBordas.addMenu("Filtro Detecção com "
                                                                                          "&Dilatação")
        self.submenuDeteccaoDeBordasDilatacao.setDisabled(True)

        # Actions do submenu
        self.criarActionDeteccaoDeBordasDilatacao3x3()
        self.criarActionDeteccaoDeBordasDilatacao5x5()
        self.criarActionDeteccaoDeBordasDilatacao7x7()
        self.criarActionDeteccaoDeBordasDilatacao9x9()

        # Listar submenu
        self.controleVisibilidadeItens.listaFiltrosImgPretoBranco.append(self.submenuDeteccaoDeBordasDilatacao)


    def criarSubmenuDeteccaoDeBordasErosao(self):
        self.submenuDeteccaoDeBordasErosao = self.submenuFiltrosDeteccaoBordas.addMenu("Filtro Detecção com &Erosão")
        self.submenuDeteccaoDeBordasErosao.setDisabled(True)

        # Actions do submenu
        self.criarActionDeteccaoDeBordasErosaoElementoEstrutura3x3()
        self.criarActionDeteccaoDeBordasErosaoElementoEstrutura5x5()
        self.criarActionDeteccaoDeBordasErosaoElementoEstrutura7x7()
        self.criarActionDeteccaoDeBordasErosaoElementoEstrutura9x9()

        # Listar submenu
        self.controleVisibilidadeItens.listaFiltrosImgPretoBranco.append(self.submenuDeteccaoDeBordasErosao)

    '''Criar Actions'''

    def criarActionConverterParaEscalaCinza(self):
        self.converterParaEscalaCinza = self.submenuConversao.addAction("&Tons de Cinza")
        self.converterParaEscalaCinza.setShortcut("Ctrl+Alt+Z")
        self.converterParaEscalaCinza.setDisabled(True)
        self.converterParaEscalaCinza.setCheckable(True)
        self.converterParaEscalaCinza.setChecked(False)
        self.converterParaEscalaCinza.triggered.connect(lambda: self.conectarMetodosEntreClasses(
            self.converterParaEscalaCinza, 'ConverterEscalaDeCinza', '.pgm', 'ArgumentoVazio'))

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgColoridaCinza.append(self.converterParaEscalaCinza)
        self.controleVisibilidadeItens.listaRemoverFiltrosParaEscalaDeCinza.append(self.converterParaEscalaCinza)

    def criarActionConverterParaPretoBranco(self):
        self.converterParaPretoBranco = self.submenuConversao.addAction("Tons Pre&to e Branco")
        self.converterParaPretoBranco.setShortcut("Ctrl+Shift+T")
        self.converterParaPretoBranco.setDisabled(True)
        self.converterParaPretoBranco.setCheckable(True)
        self.converterParaPretoBranco.setChecked(False)
        self.converterParaPretoBranco.triggered.connect(self.janelaValorLimitePretoBranco)

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgColoridaCinza.append(self.converterParaPretoBranco)

    def criarActionCorrecaoGama(self):
        self.correcaoGama = self.submenuRealcarIntensidade.addAction("Correção &Gama")
        self.correcaoGama.setShortcut("Ctrl+Shift+G")
        self.correcaoGama.setDisabled(True)
        self.correcaoGama.setCheckable(True)
        self.correcaoGama.setChecked(False)
        self.correcaoGama.triggered.connect(self.janelaValorCorrecaoGama)

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgColoridaCinza.append(self.correcaoGama)

    def criarActionDecomporCanalR(self):
        self.decomporCanalR = self.submenuDecomposicaoCanaisRGB.addAction("Vermelho")
        self.decomporCanalR.setShortcut("Ctrl+Alt+R")
        self.decomporCanalR.setCheckable(True)
        self.decomporCanalR.setChecked(False)
        self.decomporCanalR.triggered.connect(lambda: self.transformacaoImagens.transformarImagem(
            self.decomporCanalR, 'CamadaR', self.manipulacaoImagens.extensaoImagemOriginal, 'ArgumentoVazio'))

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgColoridaCinza.append(self.decomporCanalR)
        self.controleVisibilidadeItens.listaRemoverFiltrosParaEscalaDeCinza.append(self.decomporCanalR)

    def criarActionDecomporCanalG(self):
        self.decomporCanalG = self.submenuDecomposicaoCanaisRGB.addAction("Verde")
        self.decomporCanalG.setShortcut("Ctrl+Alt+G")
        self.decomporCanalG.setCheckable(True)
        self.decomporCanalG.setChecked(False)
        self.decomporCanalG.triggered.connect(lambda: self.transformacaoImagens.transformarImagem(
            self.decomporCanalG, 'CamadaG', self.manipulacaoImagens.extensaoImagemOriginal, 'ArgumentoVazio'))

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgColoridaCinza.append(self.decomporCanalG)
        self.controleVisibilidadeItens.listaRemoverFiltrosParaEscalaDeCinza.append(self.decomporCanalG)

    def criarActionDecomporCanalB(self):
        self.decomporCanalB = self.submenuDecomposicaoCanaisRGB.addAction("Azul")
        self.decomporCanalB.setShortcut("Ctrl+Alt+B")
        self.decomporCanalB.setCheckable(True)
        self.decomporCanalB.setChecked(False)
        self.decomporCanalB.triggered.connect(lambda: self.transformacaoImagens.transformarImagem(
            self.decomporCanalB, 'CamadaB', self.manipulacaoImagens.extensaoImagemOriginal, 'ArgumentoVazio'))

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgColoridaCinza.append(self.decomporCanalB)
        self.controleVisibilidadeItens.listaRemoverFiltrosParaEscalaDeCinza.append(self.decomporCanalB)

    def criarActionDeteccaoDeBordasCrono(self):
        self.deteccaoDeBordasFiltroCrono = self.submenuFiltrosDeteccaoBordas.addAction("Filtro &Crono")
        self.deteccaoDeBordasFiltroCrono.setShortcut("Ctrl+Alt+C")
        self.deteccaoDeBordasFiltroCrono.setCheckable(True)
        self.deteccaoDeBordasFiltroCrono.setChecked(False)
        self.deteccaoDeBordasFiltroCrono.triggered.connect(lambda: self.transformacaoImagens.transformarImagem(
            self.deteccaoDeBordasFiltroCrono, 'DeteccaoDeBordasCrono', self.manipulacaoImagens.extensaoImagemOriginal,
            'ArgumentoVazio'))

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgColoridaCinza.append(self.deteccaoDeBordasFiltroCrono)
        self.controleVisibilidadeItens.listaFiltrosImgPretoBranco.append(self.deteccaoDeBordasFiltroCrono)


    def criarActionDeteccaoDeBordasMarle(self):
        self.deteccaoDeBordasFiltroMarle = self.submenuFiltrosDeteccaoBordas.addAction("Filtro Marle")
        self.deteccaoDeBordasFiltroMarle.setShortcut("Ctrl+Alt+M")
        self.deteccaoDeBordasFiltroMarle.setCheckable(True)
        self.deteccaoDeBordasFiltroMarle.setChecked(False)
        self.deteccaoDeBordasFiltroMarle.triggered.connect(lambda: self.transformacaoImagens.transformarImagem(
            self.deteccaoDeBordasFiltroMarle, 'DeteccaoDeBordasMarle', self.manipulacaoImagens.extensaoImagemOriginal,
            'ArgumentoVazio'))

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgColoridaCinza.append(self.deteccaoDeBordasFiltroMarle)
        self.controleVisibilidadeItens.listaFiltrosImgPretoBranco.append(self.deteccaoDeBordasFiltroMarle)

    def criarActionDeteccaoDeBordasPrometheus(self):
        self.deteccaoDeBordasFiltroPrometheus = self.submenuFiltrosDeteccaoBordas.addAction("Filtro Prometheus")
        self.deteccaoDeBordasFiltroPrometheus.setShortcut("Ctrl+Alt+P")
        self.deteccaoDeBordasFiltroPrometheus.setCheckable(True)
        self.deteccaoDeBordasFiltroPrometheus.setChecked(False)
        self.deteccaoDeBordasFiltroPrometheus.triggered.connect(lambda: self.transformacaoImagens.transformarImagem(
            self.deteccaoDeBordasFiltroPrometheus, 'DeteccaoDeBordasPrometheus',
            self.manipulacaoImagens.extensaoImagemOriginal, 'ArgumentoVazio'))

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgColoridaCinza.append(self.deteccaoDeBordasFiltroPrometheus)
        self.controleVisibilidadeItens.listaFiltrosImgPretoBranco.append(self.deteccaoDeBordasFiltroPrometheus)

    def criarActionAberturaElementoEstrutura3x3(self):
        self.aberturaElementoEstruturante3x3 = self.submenuFiltroAbertura.addAction("Elemento Estruturante 3x3")
        self.aberturaElementoEstruturante3x3.setShortcut("Ctrl+A+3")
        self.aberturaElementoEstruturante3x3.setDisabled(True)
        self.aberturaElementoEstruturante3x3.setCheckable(True)
        self.aberturaElementoEstruturante3x3.setChecked(False)
        self.aberturaElementoEstruturante3x3.triggered.connect(lambda: self.criarJanelaDesenharElementoEstruturante
        (3, 3, self.aberturaElementoEstruturante3x3, 'Abertura',
         self.manipulacaoImagens.extensaoImagemOriginal))

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgPretoBranco.append(self.aberturaElementoEstruturante3x3)

    def criarActionAberturaElementoEstrutura5x5(self):
        self.aberturaElementoEstruturante5x5 = self.submenuFiltroAbertura.addAction("Elemento Estruturante 5x5")
        self.aberturaElementoEstruturante5x5.setShortcut("Ctrl+A+5")
        self.aberturaElementoEstruturante5x5.setDisabled(True)
        self.aberturaElementoEstruturante5x5.setCheckable(True)
        self.aberturaElementoEstruturante5x5.setChecked(False)
        self.aberturaElementoEstruturante5x5.triggered.connect(lambda: self.criarJanelaDesenharElementoEstruturante
        (5, 5, self.aberturaElementoEstruturante5x5, 'Abertura', self.manipulacaoImagens.extensaoImagemOriginal))

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgPretoBranco.append(self.aberturaElementoEstruturante5x5)

    def criarActionAberturaElementoEstrutura7x7(self):
        self.aberturaElementoEstruturante7x7 = self.submenuFiltroAbertura.addAction("Elemento Estruturante 7x7")
        self.aberturaElementoEstruturante7x7.setShortcut("Ctrl+A+7")
        self.aberturaElementoEstruturante7x7.setDisabled(True)
        self.aberturaElementoEstruturante7x7.setCheckable(True)
        self.aberturaElementoEstruturante7x7.setChecked(False)
        self.aberturaElementoEstruturante7x7.triggered.connect(lambda: self.criarJanelaDesenharElementoEstruturante
        (7, 7, self.aberturaElementoEstruturante7x7, 'Abertura', self.manipulacaoImagens.extensaoImagemOriginal))

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgPretoBranco.append(self.aberturaElementoEstruturante7x7)

    def criarActionAberturaElementoEstrutura9x9(self):
        self.aberturaElementoEstruturante9x9 = self.submenuFiltroAbertura.addAction("Elemento Estruturante 9x9")
        self.aberturaElementoEstruturante9x9.setShortcut("Ctrl+A+9")
        self.aberturaElementoEstruturante9x9.setDisabled(True)
        self.aberturaElementoEstruturante9x9.setCheckable(True)
        self.aberturaElementoEstruturante9x9.setChecked(False)
        self.aberturaElementoEstruturante9x9.triggered.connect(lambda: self.criarJanelaDesenharElementoEstruturante
        (9, 9, self.aberturaElementoEstruturante9x9, 'Abertura', self.manipulacaoImagens.extensaoImagemOriginal))

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgPretoBranco.append(self.aberturaElementoEstruturante9x9)

    def criarActionDilatacaoElementoEstrutura3x3(self):
        self.dilatacaoElementoEstruturante3x3 = self.submenuFiltroDilatacao.addAction("Elemento Estruturante 3x3")
        self.dilatacaoElementoEstruturante3x3.setShortcut("Ctrl+D+3")
        self.dilatacaoElementoEstruturante3x3.setDisabled(True)
        self.dilatacaoElementoEstruturante3x3.setCheckable(True)
        self.dilatacaoElementoEstruturante3x3.setChecked(False)
        self.dilatacaoElementoEstruturante3x3.triggered.connect(lambda: self.criarJanelaDesenharElementoEstruturante
        (3, 3, self.dilatacaoElementoEstruturante3x3, 'Dilatacao', self.manipulacaoImagens.extensaoImagemOriginal))

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgPretoBranco.append(self.dilatacaoElementoEstruturante3x3)

    def criarActionDilatacaoElementoEstrutura5x5(self):
        self.dilatacaoElementoEstruturante5x5 = self.submenuFiltroDilatacao.addAction("Elemento Estruturante 5x5")
        self.dilatacaoElementoEstruturante5x5.setShortcut("Ctrl+D+5")
        self.dilatacaoElementoEstruturante5x5.setDisabled(True)
        self.dilatacaoElementoEstruturante5x5.setCheckable(True)
        self.dilatacaoElementoEstruturante5x5.setChecked(False)
        self.dilatacaoElementoEstruturante5x5.triggered.connect(lambda: self.criarJanelaDesenharElementoEstruturante
        (5, 5, self.dilatacaoElementoEstruturante5x5, 'Dilatacao', self.manipulacaoImagens.extensaoImagemOriginal))

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgPretoBranco.append(self.dilatacaoElementoEstruturante5x5)

    def criarActionDilatacaoElementoEstrutura7x7(self):
        self.dilatacaoElementoEstruturante7x7 = self.submenuFiltroDilatacao.addAction("Elemento Estruturante 7x7")
        self.dilatacaoElementoEstruturante7x7.setShortcut("Ctrl+D+7")
        self.dilatacaoElementoEstruturante7x7.setDisabled(True)
        self.dilatacaoElementoEstruturante7x7.setCheckable(True)
        self.dilatacaoElementoEstruturante7x7.setChecked(False)
        self.dilatacaoElementoEstruturante7x7.triggered.connect(lambda: self.criarJanelaDesenharElementoEstruturante
        (7, 7, self.dilatacaoElementoEstruturante7x7, 'Dilatacao', self.manipulacaoImagens.extensaoImagemOriginal))

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgPretoBranco.append(self.dilatacaoElementoEstruturante7x7)

    def criarActionDilatacaoElementoEstrutura9x9(self):
        self.dilatacaoElementoEstruturante9x9 = self.submenuFiltroDilatacao.addAction("Elemento Estruturante 9x9")
        self.dilatacaoElementoEstruturante9x9.setShortcut("Ctrl+D+9")
        self.dilatacaoElementoEstruturante9x9.setDisabled(True)
        self.dilatacaoElementoEstruturante9x9.setCheckable(True)
        self.dilatacaoElementoEstruturante9x9.setChecked(False)
        self.dilatacaoElementoEstruturante9x9.triggered.connect(lambda: self.criarJanelaDesenharElementoEstruturante
        (9, 9, self.dilatacaoElementoEstruturante9x9, 'Dilatacao', self.manipulacaoImagens.extensaoImagemOriginal))

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgPretoBranco.append(self.dilatacaoElementoEstruturante9x9)

    def criarActionErosaoElementoEstrutura3x3(self):
        self.erosaoElementoEstruturante3x3 = self.submenuFiltroErosao.addAction("Elemento Estruturante 3x3")
        self.erosaoElementoEstruturante3x3.setShortcut("Ctrl+E+3")
        self.erosaoElementoEstruturante3x3.setDisabled(True)
        self.erosaoElementoEstruturante3x3.setCheckable(True)
        self.erosaoElementoEstruturante3x3.setChecked(False)
        self.erosaoElementoEstruturante3x3.triggered.connect(lambda: self.criarJanelaDesenharElementoEstruturante
        (3, 3, self.erosaoElementoEstruturante3x3, 'Erosao', self.manipulacaoImagens.extensaoImagemOriginal))

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgPretoBranco.append(self.erosaoElementoEstruturante3x3)

    def criarActionErosaoElementoEstrutura5x5(self):
        self.erosaoElementoEstruturante5x5 = self.submenuFiltroErosao.addAction("Elemento Estruturante 5x5")
        self.erosaoElementoEstruturante5x5.setShortcut("Ctrl+E+5")
        self.erosaoElementoEstruturante5x5.setDisabled(True)
        self.erosaoElementoEstruturante5x5.setCheckable(True)
        self.erosaoElementoEstruturante5x5.setChecked(False)
        self.erosaoElementoEstruturante5x5.triggered.connect(lambda: self.criarJanelaDesenharElementoEstruturante
        (5, 5, self.erosaoElementoEstruturante5x5, 'Erosao', self.manipulacaoImagens.extensaoImagemOriginal))

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgPretoBranco.append(self.erosaoElementoEstruturante5x5)

    def criarActionErosaoElementoEstrutura7x7(self):
        self.erosaoElementoEstruturante7x7 = self.submenuFiltroErosao.addAction("Elemento Estruturante 7x7")
        self.erosaoElementoEstruturante7x7.setShortcut("Ctrl+E+7")
        self.erosaoElementoEstruturante7x7.setDisabled(True)
        self.erosaoElementoEstruturante7x7.setCheckable(True)
        self.erosaoElementoEstruturante7x7.setChecked(False)
        self.erosaoElementoEstruturante7x7.triggered.connect(lambda: self.criarJanelaDesenharElementoEstruturante
        (7, 7, self.erosaoElementoEstruturante7x7, 'Erosao', self.manipulacaoImagens.extensaoImagemOriginal))

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgPretoBranco.append(self.erosaoElementoEstruturante7x7)

    def criarActionErosaoElementoEstrutura9x9(self):
        self.erosaoElementoEstruturante9x9 = self.submenuFiltroErosao.addAction("Elemento Estruturante 9x9")
        self.erosaoElementoEstruturante9x9.setShortcut("Ctrl+E+9")
        self.erosaoElementoEstruturante9x9.setDisabled(True)
        self.erosaoElementoEstruturante9x9.setCheckable(True)
        self.erosaoElementoEstruturante9x9.setChecked(False)
        self.erosaoElementoEstruturante9x9.triggered.connect(lambda: self.criarJanelaDesenharElementoEstruturante
        (9, 9, self.erosaoElementoEstruturante9x9, 'Erosao', self.manipulacaoImagens.extensaoImagemOriginal))

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgPretoBranco.append(self.erosaoElementoEstruturante9x9)

    def criarActionFechamentoElementoEstrutura3x3(self):
        self.fechamentoElementoEstruturante3x3 = self.submenuFiltroFechamento.addAction("Elemento Estruturante 3x3")
        self.fechamentoElementoEstruturante3x3.setShortcut("Ctrl+F+3")
        self.fechamentoElementoEstruturante3x3.setDisabled(True)
        self.fechamentoElementoEstruturante3x3.setCheckable(True)
        self.fechamentoElementoEstruturante3x3.setChecked(False)
        self.fechamentoElementoEstruturante3x3.triggered.connect(lambda: self.criarJanelaDesenharElementoEstruturante
        (3, 3, self.fechamentoElementoEstruturante3x3, 'Fechamento', self.manipulacaoImagens.extensaoImagemOriginal))

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgPretoBranco.append(self.fechamentoElementoEstruturante3x3)

    def criarActionFechamentoElementoEstrutura5x5(self):
        self.fechamentoElementoEstruturante5x5 = self.submenuFiltroFechamento.addAction("Elemento Estruturante 5x5")
        self.fechamentoElementoEstruturante5x5.setShortcut("Ctrl+F+5")
        self.fechamentoElementoEstruturante5x5.setDisabled(True)
        self.fechamentoElementoEstruturante5x5.setCheckable(True)
        self.fechamentoElementoEstruturante5x5.setChecked(False)
        self.fechamentoElementoEstruturante5x5.triggered.connect(lambda: self.criarJanelaDesenharElementoEstruturante
        (5, 5, self.fechamentoElementoEstruturante5x5, 'Fechamento', self.manipulacaoImagens.extensaoImagemOriginal))

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgPretoBranco.append(self.fechamentoElementoEstruturante5x5)

    def criarActionFechamentoElementoEstrutura7x7(self):
        self.fechamentoElementoEstruturante7x7 = self.submenuFiltroFechamento.addAction("Elemento Estruturante 7x7")
        self.fechamentoElementoEstruturante7x7.setShortcut("Ctrl+F+7")
        self.fechamentoElementoEstruturante7x7.setDisabled(True)
        self.fechamentoElementoEstruturante7x7.setCheckable(True)
        self.fechamentoElementoEstruturante7x7.setChecked(False)
        self.fechamentoElementoEstruturante7x7.triggered.connect(lambda: self.criarJanelaDesenharElementoEstruturante
        (7, 7, self.fechamentoElementoEstruturante7x7, 'Fechamento', self.manipulacaoImagens.extensaoImagemOriginal))

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgPretoBranco.append(self.fechamentoElementoEstruturante7x7)

    def criarActionFechamentoElementoEstrutura9x9(self):
        self.fechamentoElementoEstruturante9x9 = self.submenuFiltroFechamento.addAction("Elemento Estruturante 9x9")
        self.fechamentoElementoEstruturante9x9.setShortcut("Ctrl+F+9")
        self.fechamentoElementoEstruturante9x9.setDisabled(True)
        self.fechamentoElementoEstruturante9x9.setCheckable(True)
        self.fechamentoElementoEstruturante9x9.setChecked(False)
        self.fechamentoElementoEstruturante9x9.triggered.connect(lambda: self.criarJanelaDesenharElementoEstruturante
        (9, 9, self.fechamentoElementoEstruturante9x9, 'Fechamento', self.manipulacaoImagens.extensaoImagemOriginal))

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgPretoBranco.append(self.fechamentoElementoEstruturante9x9)

    def criarActionDeteccaoDeBordasDilatacao3x3(self):
        self.deteccaoDeBordasDilatacaoElementoEstruturante3x3 = self.submenuDeteccaoDeBordasDilatacao.addAction("Elemento Estruturante 3x3")
        self.deteccaoDeBordasDilatacaoElementoEstruturante3x3.setShortcut("Ctrl+B+3")
        self.deteccaoDeBordasDilatacaoElementoEstruturante3x3.setDisabled(True)
        self.deteccaoDeBordasDilatacaoElementoEstruturante3x3.setCheckable(True)
        self.deteccaoDeBordasDilatacaoElementoEstruturante3x3.setChecked(False)
        self.deteccaoDeBordasDilatacaoElementoEstruturante3x3.triggered.connect(lambda: self.criarJanelaDesenharElementoEstruturante
        (3, 3, self.deteccaoDeBordasDilatacaoElementoEstruturante3x3, 'DeteccaoDeBordasDilatacao',
         self.manipulacaoImagens.extensaoImagemOriginal))

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgPretoBranco.append(self.deteccaoDeBordasDilatacaoElementoEstruturante3x3)

    def criarActionDeteccaoDeBordasDilatacao5x5(self):
        self.deteccaoDeBordasDilatacaoElementoEstruturante5x5 = self.submenuDeteccaoDeBordasDilatacao.addAction("Elemento Estruturante 5x5")
        self.deteccaoDeBordasDilatacaoElementoEstruturante5x5.setShortcut("Ctrl+B+5")
        self.deteccaoDeBordasDilatacaoElementoEstruturante5x5.setDisabled(True)
        self.deteccaoDeBordasDilatacaoElementoEstruturante5x5.setCheckable(True)
        self.deteccaoDeBordasDilatacaoElementoEstruturante5x5.setChecked(False)
        self.deteccaoDeBordasDilatacaoElementoEstruturante5x5.triggered.connect(lambda: self.criarJanelaDesenharElementoEstruturante
        (5, 5, self.deteccaoDeBordasDilatacaoElementoEstruturante5x5, 'DeteccaoDeBordasDilatacao', self.manipulacaoImagens.extensaoImagemOriginal))

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgPretoBranco.append(self.deteccaoDeBordasDilatacaoElementoEstruturante5x5)

    def criarActionDeteccaoDeBordasDilatacao7x7(self):
        self.deteccaoDeBordasDilatacaoElementoEstruturante7x7 = self.submenuDeteccaoDeBordasDilatacao.addAction("Elemento Estruturante 7x7")
        self.deteccaoDeBordasDilatacaoElementoEstruturante7x7.setShortcut("Ctrl+B+7")
        self.deteccaoDeBordasDilatacaoElementoEstruturante7x7.setDisabled(True)
        self.deteccaoDeBordasDilatacaoElementoEstruturante7x7.setCheckable(True)
        self.deteccaoDeBordasDilatacaoElementoEstruturante7x7.setChecked(False)
        self.deteccaoDeBordasDilatacaoElementoEstruturante7x7.triggered.connect(lambda: self.criarJanelaDesenharElementoEstruturante
        (7, 7, self.deteccaoDeBordasDilatacaoElementoEstruturante7x7, 'DeteccaoDeBordasDilatacao', self.manipulacaoImagens.extensaoImagemOriginal))

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgPretoBranco.append(self.deteccaoDeBordasDilatacaoElementoEstruturante7x7)

    def criarActionDeteccaoDeBordasDilatacao9x9(self):
        self.deteccaoDeBordasDilatacaoElementoEstruturante9x9 = self.submenuDeteccaoDeBordasDilatacao.addAction("Elemento Estruturante 9x9")
        self.deteccaoDeBordasDilatacaoElementoEstruturante9x9.setShortcut("Ctrl+B+9")
        self.deteccaoDeBordasDilatacaoElementoEstruturante9x9.setDisabled(True)
        self.deteccaoDeBordasDilatacaoElementoEstruturante9x9.setCheckable(True)
        self.deteccaoDeBordasDilatacaoElementoEstruturante9x9.setChecked(False)
        self.deteccaoDeBordasDilatacaoElementoEstruturante9x9.triggered.connect(lambda: self.criarJanelaDesenharElementoEstruturante
        (9, 9, self.deteccaoDeBordasDilatacaoElementoEstruturante9x9, 'DeteccaoDeBordasDilatacao', self.manipulacaoImagens.extensaoImagemOriginal))

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgPretoBranco.append(self.deteccaoDeBordasDilatacaoElementoEstruturante9x9)

    def criarActionDeteccaoDeBordasErosaoElementoEstrutura3x3(self):
        self.deteccaoDeBordasErosaoElementoEstruturante3x3 = self.submenuDeteccaoDeBordasErosao.addAction("Elemento Estruturante 3x3")
        self.deteccaoDeBordasErosaoElementoEstruturante3x3.setShortcut("Ctrl+R+3")
        self.deteccaoDeBordasErosaoElementoEstruturante3x3.setDisabled(True)
        self.deteccaoDeBordasErosaoElementoEstruturante3x3.setCheckable(True)
        self.deteccaoDeBordasErosaoElementoEstruturante3x3.setChecked(False)
        self.deteccaoDeBordasErosaoElementoEstruturante3x3.triggered.connect(lambda: self.criarJanelaDesenharElementoEstruturante
        (3, 3, self.deteccaoDeBordasErosaoElementoEstruturante3x3, 'DeteccaoDeBordasErosao',
         self.manipulacaoImagens.extensaoImagemOriginal))

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgPretoBranco.append(self.deteccaoDeBordasErosaoElementoEstruturante3x3)

    def criarActionDeteccaoDeBordasErosaoElementoEstrutura5x5(self):
        self.deteccaoDeBordasErosaoElementoEstruturante5x5 = self.submenuDeteccaoDeBordasErosao.addAction("Elemento Estruturante 5x5")
        self.deteccaoDeBordasErosaoElementoEstruturante5x5.setShortcut("Ctrl+R+5")
        self.deteccaoDeBordasErosaoElementoEstruturante5x5.setDisabled(True)
        self.deteccaoDeBordasErosaoElementoEstruturante5x5.setCheckable(True)
        self.deteccaoDeBordasErosaoElementoEstruturante5x5.setChecked(False)
        self.deteccaoDeBordasErosaoElementoEstruturante5x5.triggered.connect(lambda: self.criarJanelaDesenharElementoEstruturante
        (5, 5, self.deteccaoDeBordasErosaoElementoEstruturante5x5, 'DeteccaoDeBordasDilatacao', self.manipulacaoImagens.extensaoImagemOriginal))

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgPretoBranco.append(self.deteccaoDeBordasErosaoElementoEstruturante5x5)

    def criarActionDeteccaoDeBordasErosaoElementoEstrutura7x7(self):
        self.deteccaoDeBordasErosaoElementoEstruturante7x7 = self.submenuDeteccaoDeBordasErosao.addAction("Elemento Estruturante 7x7")
        self.deteccaoDeBordasErosaoElementoEstruturante7x7.setShortcut("Ctrl+R+7")
        self.deteccaoDeBordasErosaoElementoEstruturante7x7.setDisabled(True)
        self.deteccaoDeBordasErosaoElementoEstruturante7x7.setCheckable(True)
        self.deteccaoDeBordasErosaoElementoEstruturante7x7.setChecked(False)
        self.deteccaoDeBordasErosaoElementoEstruturante7x7.triggered.connect(lambda: self.criarJanelaDesenharElementoEstruturante
        (7, 7, self.deteccaoDeBordasErosaoElementoEstruturante7x7, 'DeteccaoDeBordasDilatacao', self.manipulacaoImagens.extensaoImagemOriginal))

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgPretoBranco.append(self.deteccaoDeBordasErosaoElementoEstruturante7x7)

    def criarActionDeteccaoDeBordasErosaoElementoEstrutura9x9(self):
        self.deteccaoDeBordasErosaoElementoEstruturante9x9 = self.submenuDeteccaoDeBordasErosao.addAction("Elemento Estruturante 9x9")
        self.deteccaoDeBordasErosaoElementoEstruturante9x9.setShortcut("Ctrl+R+9")
        self.deteccaoDeBordasErosaoElementoEstruturante9x9.setDisabled(True)
        self.deteccaoDeBordasErosaoElementoEstruturante9x9.setCheckable(True)
        self.deteccaoDeBordasErosaoElementoEstruturante9x9.setChecked(False)
        self.deteccaoDeBordasErosaoElementoEstruturante9x9.triggered.connect(lambda: self.criarJanelaDesenharElementoEstruturante
        (9, 9, self.deteccaoDeBordasErosaoElementoEstruturante9x9, 'DeteccaoDeBordasDilatacao', self.manipulacaoImagens.extensaoImagemOriginal))

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgPretoBranco.append(self.deteccaoDeBordasErosaoElementoEstruturante9x9)

    def criarActionKernelGaussiano3x3(self):
        self.kernelGaussiano3x3 = self.submenuFiltroGaussiano.addAction("Matriz 3x3")
        self.kernelGaussiano3x3.setShortcut("Ctrl+Alt+3")
        self.kernelGaussiano3x3.setCheckable(True)
        self.kernelGaussiano3x3.setChecked(False)
        self.kernelGaussiano3x3.triggered.connect(lambda: self.transformacaoImagens.transformarImagem(
            self.kernelGaussiano3x3, 'Gaussiano3x3', self.manipulacaoImagens.extensaoImagemOriginal, 'ArgumentoVazio'))

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgColoridaCinza.append(self.kernelGaussiano3x3)

    def criarActionKernelGaussiano5x5(self):
        self.kernelGaussiano5x5 = self.submenuFiltroGaussiano.addAction("Matriz 5x5")
        self.kernelGaussiano5x5.setShortcut("Ctrl+Alt+5")
        self.kernelGaussiano5x5.setCheckable(True)
        self.kernelGaussiano5x5.setChecked(False)
        self.kernelGaussiano5x5.triggered.connect(lambda: self.transformacaoImagens.transformarImagem(
            self.kernelGaussiano5x5, 'Gaussiano5x5', self.manipulacaoImagens.extensaoImagemOriginal, 'ArgumentoVazio'))

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgColoridaCinza.append(self.kernelGaussiano5x5)

    def criarActionKernelGaussiano7x7(self):
        self.kernelGaussiano7x7 = self.submenuFiltroGaussiano.addAction("Matriz 7x7")
        self.kernelGaussiano7x7.setShortcut("Ctrl+Alt+7")
        self.kernelGaussiano7x7.setCheckable(True)
        self.kernelGaussiano7x7.setChecked(False)
        self.kernelGaussiano7x7.triggered.connect(lambda: self.transformacaoImagens.transformarImagem(
            self.kernelGaussiano7x7, 'Gaussiano7x7', self.manipulacaoImagens.extensaoImagemOriginal, 'ArgumentoVazio'))

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgColoridaCinza.append(self.kernelGaussiano7x7)

    def criarActionFiltroMediana(self):
        self.filtroMediana = self.submenuFiltrosDesfocar.addAction("Filtro &Mediana")
        self.filtroMediana.setShortcut("Ctrl+Shift+M")
        self.filtroMediana.setDisabled(True)
        self.filtroMediana.setCheckable(True)
        self.filtroMediana.setChecked(False)
        self.filtroMediana.triggered.connect(lambda: self.transformacaoImagens.transformarImagem(
            self.filtroMediana, 'Mediana', self.manipulacaoImagens.extensaoImagemOriginal, 'ArgumentoVazio'))

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgColoridaCinza.append(self.filtroMediana)

    def criarActionFiltroSharpen(self):
        self.filtroSharpen = self.submenuAjustarNitidez.addAction("Filtro S&harpen")
        self.filtroSharpen.setShortcut("Ctrl+Shift+H")
        self.filtroSharpen.setDisabled(True)
        self.filtroSharpen.setCheckable(True)
        self.filtroSharpen.setChecked(False)
        self.filtroSharpen.triggered.connect(lambda: self.transformacaoImagens.transformarImagem(
            self.filtroSharpen, 'Sharpen', self.manipulacaoImagens.extensaoImagemOriginal, 'ArgumentoVazio'))

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgColoridaCinza.append(self.filtroSharpen)

    def criarActionFiltroSobel(self):
        self.filtroSobel = self.submenuFiltrosDeteccaoBordas.addAction("Filtro S&obel")
        self.filtroSobel.setShortcut("Ctrl+Shift+O")
        self.filtroSobel.setDisabled(True)
        self.filtroSobel.setCheckable(True)
        self.filtroSobel.setChecked(False)
        self.filtroSobel.triggered.connect(self.janelaValorLimiteSobel)

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgColoridaCinza.append(self.filtroSobel)

    def criarActionInverterNegativo(self):
        self.filtroNegativo = self.submenuInverterCores.addAction("&Negativo")
        self.filtroNegativo.setShortcut("Ctrl+Shift+N")
        self.filtroNegativo.setDisabled(True)
        self.filtroNegativo.setCheckable(True)
        self.filtroNegativo.setChecked(False)
        self.filtroNegativo.triggered.connect(lambda: self.transformacaoImagens.transformarImagem(
            self.filtroNegativo, 'Negativo', self.manipulacaoImagens.extensaoImagemOriginal, 'ArgumentoVazio'))

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgColoridaCinza.append(self.filtroNegativo)

    def criarActionTransformacaoLogaritmica(self):
        self.transformacaoLogaritmica = self.submenuRealcarIntensidade.addAction("Transformação &Logarítmica")
        self.transformacaoLogaritmica.setShortcut("Ctrl+Shift+L")
        self.transformacaoLogaritmica.setDisabled(True)
        self.transformacaoLogaritmica.setCheckable(True)
        self.transformacaoLogaritmica.setChecked(False)
        self.transformacaoLogaritmica.triggered.connect(lambda: self.transformacaoImagens.transformarImagem(
            self.transformacaoLogaritmica, 'TransformacaoLogaritmica', self.manipulacaoImagens.extensaoImagemOriginal,
            'ArgumentoVazio'))

        # Listar action
        self.controleVisibilidadeItens.listaFiltrosImgColoridaCinza.append(self.transformacaoLogaritmica)

    def criarJanelaDesenharElementoEstruturante(self, totalLinhas, totalColunas, filtro, script, extensao):
        self.janelaDesenharElementoEstruturante = JanelaMatrizElementoEstruturante(totalLinhas, totalColunas)
        self.janelaDesenharElementoEstruturante.botaoEnviar.clicked.connect \
            (lambda: self.pegarMatrizElementoEstruturante(filtro, script, extensao))

    def pegarMatrizElementoEstruturante(self, filtro, script, extensao):
        stringMatrizElementoEstruturante = ''
        matrizElementoEstruturante = self.janelaDesenharElementoEstruturante.elemento

        for linha in range(len(matrizElementoEstruturante)):
            for coluna in range(len(matrizElementoEstruturante[linha])):
                stringMatrizElementoEstruturante += str(matrizElementoEstruturante[linha][coluna])

        self.janelaDesenharElementoEstruturante.close()
        self.transformacaoImagens.transformarImagem(filtro, script, extensao, stringMatrizElementoEstruturante)

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
        self.transformacaoImagens.transformarImagem(self.correcaoGama, 'CorrecaoGama',
                                                    self.manipulacaoImagens.extensaoImagemOriginal, valorFatorGama)

    '''Instancia classe ValorCorrecaoGama e pega valor fator gama 
    escolhido pelo usuário ao apertar botão enviar valor'''

    def janelaValorLimiteSobel(self):
        self.janelaValorLimiteSobel = JanelaValorLimiteSobel()
        self.janelaValorLimiteSobel.enviarValor.clicked.connect(self.pegarValorLimiteSobel)

    '''Pegar valor fator Gama definido na classe ValorLimiteSobel'''

    def pegarValorLimiteSobel(self):
        valorLimiteSobel = str(self.janelaValorLimiteSobel.valorSlider)
        self.janelaValorLimiteSobel.close()
        self.transformacaoImagens.transformarImagem(self.filtroSobel, 'Sobel',
                                                    self.manipulacaoImagens.extensaoImagemOriginal, valorLimiteSobel)

    def janelaValorLimitePretoBranco(self):
        self.janelaValorLimitePretoBranco = JanelaValorLimitePretoBranco()
        self.janelaValorLimitePretoBranco.enviarValor.clicked.connect(self.pegarValorLimitePretoBranco)

    def pegarValorLimitePretoBranco(self):
        valorLimitePretoBranco = str(self.janelaValorLimitePretoBranco.valorSlider)
        self.janelaValorLimitePretoBranco.close()
        self.conectarMetodosEntreClasses(self.converterParaPretoBranco, 'ConverterImagemBinaria', '.pbm', valorLimitePretoBranco)

    ''' Invocar método de transformar Imagens e alterarVisibilidade Itens do Menu para quando uma imagem for 
    transformanda em outra tipo'''
    def conectarMetodosEntreClasses(self, filtro, script, extensao, valorArgumento3):
        self.transformacaoImagens.transformarImagem(filtro, script, extensao, valorArgumento3)

        self.controleVisibilidadeItens.alterarVisibilidadeItensMenuTransformacoes(extensao)

