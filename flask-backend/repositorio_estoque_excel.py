import config
import openpyxl
import sys
from pathlib import Path
from os import listdir
from os.path import isfile, join
from datetime import datetime

from insumo import Insumo
from estoque import Estoque
from tipo_estoque import TipoEstoque

class RepositorioEstoque:
  def __init__(self, tipo, repositorio_insumo):
    self.repositorio_insumo = repositorio_insumo
    self.estoque = self.Inicializar(tipo)

  def Inicializar(self, tipo):
    pasta = config.estoque['pasta']
    pasta_estoque_inicial = config.estoque['pasta_estoque_inicial']
    pasta_estoque_final = config.estoque['pasta_estoque_final']

    if tipo == TipoEstoque.INICIAL:
      arquivos_da_pasta = [arquivo for arquivo in listdir(f'./{pasta}/{pasta_estoque_inicial}') if isfile(join(f'./{pasta}/{pasta_estoque_inicial}', arquivo))]
    else:
      arquivos_da_pasta = [arquivo for arquivo in listdir(f'./{pasta}/{pasta_estoque_final}') if isfile(join(f'./{pasta}/{pasta_estoque_final}', arquivo))]

    arquivo_xlsx_estoque = next((arquivo for arquivo in arquivos_da_pasta if '~' not in arquivo), None)
    if arquivo_xlsx_estoque == None:
      print(f'Não foi possível localizar o arquivo do {tipo}.')
      sys.exit()

    if tipo == TipoEstoque.INICIAL:
      caminho_completo_arquivo_xlsx = f'./{pasta}/{pasta_estoque_inicial}/{arquivo_xlsx_estoque}'
    else:
      caminho_completo_arquivo_xlsx = f'./{pasta}/{pasta_estoque_final}/{arquivo_xlsx_estoque}'

    workbook = openpyxl.load_workbook(caminho_completo_arquivo_xlsx)
    sheet = workbook['estoque']

    # descobrindo a quantidade de linhas com dados e armazenando na variável "total_linhas_dados"
    linha_inicial_dados = 4
    conteudo_celula = sheet['A' + str(linha_inicial_dados)].value
    total_linhas_dados = 0
    while (conteudo_celula != None):
      total_linhas_dados+= 1
      conteudo_celula = sheet['A' + str(linha_inicial_dados + total_linhas_dados)].value

    # recupera os insumos e suas quantidades da planilha
    descricao = 'Inicial' if tipo == TipoEstoque.INICIAL else 'Final'
    data_da_contagem = str(sheet['B1'].value)
    hora_da_contagem = str(sheet['B2'].value)
    estoque = Estoque(descricao, data_da_contagem, hora_da_contagem)
    for x in range(linha_inicial_dados, total_linhas_dados + linha_inicial_dados):
      codigo_insumo = str(sheet['A' + str(x)].value)
      insumo = self.repositorio_insumo.ObterPorCodigo(codigo_insumo)
      pacotes = sheet['C' + str(x)].value
      unidades = sheet['D' + str(x)].value
      estoque.adicionarItem(insumo, pacotes, unidades)
      
    return estoque
  
  def Obter(self):
    return self.estoque