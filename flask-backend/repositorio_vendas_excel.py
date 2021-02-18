import config
import openpyxl
import sys
from pathlib import Path
from os import listdir
from os.path import isfile, join
from vendas import Vendas

class RepositorioVendas:
  def __init__(self, repositorio_produtos):
    self.repositorio_produtos = repositorio_produtos
    self.vendas = self.Inicializar()

  def ObterTodas(self):
    return self.vendas

  def Inicializar(self):
    pasta = config.relatorio_de_vendas['pasta']
    arquivos_da_pasta = [f for f in listdir('./' + pasta) if isfile(join('./' + pasta, f))]
    arquivo_xlsx_vendas = next((arquivo for arquivo in arquivos_da_pasta if '~' not in arquivo), None)
    if arquivo_xlsx_vendas == None:
      print('Não foi possível localizar o arquivo do Relatório de Vendas.')
      sys.exit()

    caminho_completo_arquivo_xlsx = './' + pasta + '/' + arquivo_xlsx_vendas
    workbook = openpyxl.load_workbook(caminho_completo_arquivo_xlsx)
    sheet = workbook.active

    # descobrindo a quantidade de linhas com dados e armazenando na variável "total_linhas_dados"
    conteudo_celula = sheet[config.relatorio_de_vendas['coluna_inicial_dados'] + str(config.relatorio_de_vendas['linha_inicial_dados'])].value
    total_linhas_dados = 0
    while (conteudo_celula != None):
      total_linhas_dados+= 1
      conteudo_celula = sheet[config.relatorio_de_vendas['coluna_inicial_dados'] + str(config.relatorio_de_vendas['linha_inicial_dados'] + total_linhas_dados)].value

    # popular a classe Vendas
    vendas = Vendas()
    vendas.data = str(sheet['D14'].value)
    for x in range(config.relatorio_de_vendas['linha_inicial_dados'], total_linhas_dados + config.relatorio_de_vendas['linha_inicial_dados']):
      # algoritmo de busca de cada codigo
      codigo_produto = str(sheet['F' + str(x)].value)
      quantidade_vendida = sheet['K' + str(x)].value
      produto = self.repositorio_produtos.ObterPorCodigo(codigo_produto)
      if produto != None:
        vendas.adicionarItem(produto, int(quantidade_vendida))

    return vendas