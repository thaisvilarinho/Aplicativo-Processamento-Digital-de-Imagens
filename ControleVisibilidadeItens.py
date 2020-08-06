class ControleVisibilidadeItens():
    def __init__(self, opcaoInfoImagem, opcaoSalvarComo, opcaoRecente):
        super(ControleVisibilidadeItens, self).__init__()

        self.opcaoInfoImagem = opcaoInfoImagem
        self.opcaoSalvarComo = opcaoSalvarComo
        self.opcaoRecente = opcaoRecente
        self.listaFiltrosImgColoridaCinza = []
        self.listaFiltrosImgPretoBranco = []
        self.listaRemoverFiltrosParaEscalaDeCinza = []

    '''Contolar quais submenus e actions estão visíveis dependendo do tipo da imagem'''

    def alterarVisibilidadeItensMenuTransformacoes(self, extensao):

        self.opcaoInfoImagem.setVisible(True)
        self.opcaoSalvarComo.setDisabled(False)
        self.opcaoRecente.setDisabled(False)

        if extensao == '.ppm':
            for filtro in self.listaFiltrosImgColoridaCinza:
                filtro.setDisabled(False)

            for filtro in self.listaFiltrosImgPretoBranco:
                if filtro not in self.listaFiltrosImgColoridaCinza:
                    filtro.setDisabled(True)

        elif extensao == '.pgm':
            for filtro in self.listaFiltrosImgColoridaCinza:
                if filtro in self.listaRemoverFiltrosParaEscalaDeCinza:
                    filtro.setDisabled(True)
                else:
                    filtro.setDisabled(False)

            for filtro in self.listaFiltrosImgPretoBranco:
                if filtro not in self.listaFiltrosImgColoridaCinza:
                    filtro.setDisabled(True)

        elif extensao == '.pbm':
            for filtro in self.listaFiltrosImgColoridaCinza:
                filtro.setDisabled(True)

            for filtro in self.listaFiltrosImgPretoBranco:
                filtro.setDisabled(False)
