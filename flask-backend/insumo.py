class Insumo:
  def __init__(self, codigo_insumo, descricao, unidades_pacote):
    self.codigo_insumo = codigo_insumo
    self.descricao = descricao
    self.unidades_pacote = unidades_pacote

  def serialize(self):  
    return {           
      'codigo_insumo': self.codigo_insumo, 
      'descricao': self.descricao,
      'unidades_pacote': self.unidades_pacote
    }