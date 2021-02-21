import config
import openpyxl
import sys
from pathlib import Path
from produto import Produto
from produto_item import ProdutoItem
from insumo import Insumo

class RepositorioProduto:
    def __init__(self, repositorio_insumo):
        self.LINHA_INICIAL_DADOS = 2
        self.repositorio_insumo = repositorio_insumo
        self.produtos = self.__Inicializar()
  
    def ObterTodos(self):
        return self.produtos
    
    def ObterPorCodigo(self, codigo_produto):
        produto = next((produto for produto in self.produtos if produto.codigo_produto == codigo_produto), None)
        return produto
  
    def Adicionar(self, produtoInputModel):
        produto_itens =  []
        for produto_item in produtoInputModel['produto_itens']:
            codigo_insumo = produto_item['insumo']['codigo_insumo']
            insumo = self.repositorio_insumo.ObterPorCodigo(codigo_insumo)
            quantidade = produto_item['quantidade']
            produto_itens.append(ProdutoItem(insumo, quantidade))

        produto = Produto(produtoInputModel['codigo_produto'], produtoInputModel['descricao'], produto_itens)
        self.produtos.append(produto)
        self.Salvar()

    def Atualizar(self, produtoInputModel):
        produto_itens =  []
        for produto_item in produtoInputModel['produto_itens']:
            codigo_insumo = produto_item['insumo']['codigo_insumo']
            insumo = self.repositorio_insumo.ObterPorCodigo(codigo_insumo)
            quantidade = produto_item['quantidade']
            produto_itens.append(ProdutoItem(insumo, quantidade))
        
        produto_atualizar = Produto(produtoInputModel['codigo_produto'], produtoInputModel['descricao'], produto_itens)
        produto_repositorio = next((produto for produto in self.produtos if produto.codigo_produto == produto_atualizar.codigo_produto), None)
        
        produto_repositorio.descricao = produto_atualizar.descricao
        produto_repositorio.produto_itens = produto_atualizar.produto_itens
        self.Salvar()

    def Excluir(self, id):
        produto = next((produto for produto in self.produtos if produto.codigo_produto == id), None)
        self.produtos.remove(produto)
        self.Salvar()
  
    def __Inicializar(self):
        arquivo_xlsx_banco_de_dados = str(Path(config.banco_de_dados['arquivo']))
        pasta = config.banco_de_dados['pasta']
        workbook = openpyxl.load_workbook(f'{pasta}/{arquivo_xlsx_banco_de_dados}')
        sheet_produto = workbook['produto']
        sheet_produto_insumo = workbook['produto_insumo']

        # descobrindo a quantidade de linhas com dados e armazenando na variável "total_linhas_dados_produto"
        total_linhas_dados_produto = self.__ObterTotalLinhasDados(sheet_produto)

        # descobrindo a quantidade de linhas com dados e armazenando na variável "total_linhas_dados_produto_insumo"
        total_linhas_dados_produto_insumo = self.__ObterTotalLinhasDados(sheet_produto_insumo)

        # recupera os produtos da planilha
        produtos = []
        for x in range(self.LINHA_INICIAL_DADOS, total_linhas_dados_produto + self.LINHA_INICIAL_DADOS):
            codigo_produto = str(sheet_produto['A' + str(x)].value)
            descricao = sheet_produto['B' + str(x)].value

            # recupera os insumos de cada produto da planilha
            produto_itens = []
            for x in range(self.LINHA_INICIAL_DADOS, total_linhas_dados_produto_insumo + self.LINHA_INICIAL_DADOS):
                codigo_produto_insumo = str(sheet_produto_insumo['A' + str(x)].value)
                if codigo_produto == codigo_produto_insumo:
                    codigo_insumo = str(sheet_produto_insumo['B' + str(x)].value)
                    insumo = self.repositorio_insumo.ObterPorCodigo(codigo_insumo)
                    quantidade = sheet_produto_insumo['C' + str(x)].value
                    produto_itens.append(ProdutoItem(insumo, quantidade))
        
            produtos.append(Produto(codigo_produto, descricao, produto_itens))

        return produtos

    def Salvar(self):
        # obter as sheets produto e produto_insumo do arquivo Excel do banco de dados
        arquivo_xlsx_banco_de_dados = str(Path(config.banco_de_dados['arquivo']))
        pasta = config.banco_de_dados['pasta']

        try:
            self.workbook = openpyxl.load_workbook(f'{pasta}/{arquivo_xlsx_banco_de_dados}')
        except:
            print('Não foi possível localizar o arquivo de Banco de Dados.')
            sys.exit()

        sheet_produto = self.workbook['produto']
        sheet_produto_insumo = self.workbook['produto_insumo']

        # apagar todos os produtos da planilha produto
        total_linhas_dados = self.__ObterTotalLinhasDados(sheet_produto)
        for x in range(self.LINHA_INICIAL_DADOS, total_linhas_dados + self.LINHA_INICIAL_DADOS):
            sheet_produto['A' + str(x)].value = ''
            sheet_produto['B' + str(x)].value = ''

        # apagar todos os produtos_insumos da planilha produto_insumo
        total_linhas_dados = self.__ObterTotalLinhasDados(sheet_produto_insumo)
        for x in range(self.LINHA_INICIAL_DADOS, total_linhas_dados + self.LINHA_INICIAL_DADOS):
            sheet_produto_insumo['A' + str(x)].value = ''
            sheet_produto_insumo['B' + str(x)].value = ''
            sheet_produto_insumo['C' + str(x)].value = ''
        
        # inserir os novos produtos na planilha
        produtos_insumos = []
        for i, produto in enumerate(self.produtos):
            sheet_produto['A' + str(i + self.LINHA_INICIAL_DADOS)].value = produto.codigo_produto
            sheet_produto['B' + str(i + self.LINHA_INICIAL_DADOS)].value = produto.descricao

            for produto_item in produto.produto_itens:
                insumo = produto_item.insumo
                produtos_insumos.append({
                    'codigo_produto': produto.codigo_produto,
                    'codigo_insumo': insumo.codigo_insumo,
                    'quantidade': produto_item.quantidade
                })

        for i, produto_item in enumerate(produtos_insumos):
            sheet_produto_insumo['A' + str(i + self.LINHA_INICIAL_DADOS)].value = produto_item['codigo_produto']
            sheet_produto_insumo['B' + str(i + self.LINHA_INICIAL_DADOS)].value = produto_item['codigo_insumo']
            sheet_produto_insumo['C' + str(i + self.LINHA_INICIAL_DADOS)].value = produto_item['quantidade']
        
        arquivo_xlsx_banco_de_dados = str(Path(config.banco_de_dados['arquivo']))
        pasta = config.banco_de_dados['pasta']
        self.workbook.save(f'{pasta}/{arquivo_xlsx_banco_de_dados}')

    def __ObterTotalLinhasDados(self, sheet):
        conteudo_celula = sheet['A' + str(self.LINHA_INICIAL_DADOS)].value
        total_linhas_dados = 0
        while (conteudo_celula != None):
            total_linhas_dados+= 1
            conteudo_celula = sheet['A' + str(self.LINHA_INICIAL_DADOS + total_linhas_dados)].value
        
        return total_linhas_dados