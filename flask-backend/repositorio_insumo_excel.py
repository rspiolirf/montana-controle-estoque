import config
import openpyxl
import sys
from pathlib import Path
from insumo import Insumo

class RepositorioInsumo:
  def __init__(self):
    self.LINHA_INICIAL_DADOS = 2
    self.workbook = None
    self.insumos = self.__Inicializar()

  def ObterTodos(self):
    return self.insumos
  
  def ObterPorCodigo(self, codigo_insumo):
    insumo = next((insumo for insumo in self.insumos if insumo.codigo_insumo == codigo_insumo), None)
    return insumo
  
  def Adicionar(self, insumoInputModel):
    insumo = Insumo(insumoInputModel['codigo_insumo'], insumoInputModel['descricao'], insumoInputModel['unidades_pacote'])
    self.insumos.append(insumo)
    self.Salvar()

  def Excluir(self, id):
    insumo = next((insumo for insumo in self.insumos if insumo.codigo_insumo == id), None)
    self.insumos.remove(insumo)
    self.Salvar()

  def Salvar(self):
    sheet = self.__ObterSheet()
    total_linhas_dados = self.__ObterTotalLinhasDados(sheet)

    # apagar todos os insumos da planilha
    for x in range(self.LINHA_INICIAL_DADOS, total_linhas_dados + self.LINHA_INICIAL_DADOS):
      sheet['A' + str(x)].value = ''
      sheet['B' + str(x)].value = ''
      sheet['C' + str(x)].value = ''
    
    # inserir os novos insumos na planilha
    for i, insumo in enumerate(self.insumos):
      sheet['A' + str(i + self.LINHA_INICIAL_DADOS)].value = insumo.codigo_insumo
      sheet['B' + str(i + self.LINHA_INICIAL_DADOS)].value = insumo.descricao
      sheet['C' + str(i + self.LINHA_INICIAL_DADOS)].value = insumo.unidades_pacote
    
    arquivo_xlsx_banco_de_dados = str(Path(config.banco_de_dados['arquivo']))
    pasta = config.banco_de_dados['pasta']
    self.workbook.save(f'{pasta}/{arquivo_xlsx_banco_de_dados}')

  def __Inicializar(self):
    sheet = self.__ObterSheet()
    total_linhas_dados = self.__ObterTotalLinhasDados(sheet)
    
    # recupera os insumos da planilha    
    insumos = []
    for x in range(self.LINHA_INICIAL_DADOS, total_linhas_dados + self.LINHA_INICIAL_DADOS):
      codigo_insumo = str(sheet['A' + str(x)].value)
      descricao = sheet['B' + str(x)].value
      unidades_pacote = sheet['C' + str(x)].value
      insumos.append(Insumo(codigo_insumo, descricao, unidades_pacote))
      
    return insumos

  def __ObterSheet(self):
    arquivo_xlsx_banco_de_dados = str(Path(config.banco_de_dados['arquivo']))
    pasta = config.banco_de_dados['pasta']

    try:
      self.workbook = openpyxl.load_workbook(f'{pasta}/{arquivo_xlsx_banco_de_dados}')
    except:
      print('Não foi possível localizar o arquivo de Banco de Dados.')
      sys.exit()

    sheet = self.workbook['insumo']
    return sheet

  def __ObterTotalLinhasDados(self, sheet):
    conteudo_celula = sheet['A' + str(self.LINHA_INICIAL_DADOS)].value
    total_linhas_dados = 0
    while (conteudo_celula != None):
      total_linhas_dados+= 1
      conteudo_celula = sheet['A' + str(self.LINHA_INICIAL_DADOS + total_linhas_dados)].value
    
    return total_linhas_dados