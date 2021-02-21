import datetime
from estoque_item import EstoqueItem

class Estoque:
    def __init__(self, descricao, data, hora):
        self.descricao = descricao
        self.data = data
        self.hora = hora
        self.estoque_itens = []

    def adicionarItem(self, insumo, pacotes, unidades):
        self.estoque_itens.append(EstoqueItem(insumo, pacotes, unidades))
   
    def obterDiferencial(self, estoque_inicial):
        now = datetime.datetime.now()
        estoque_diferencial = Estoque('Diferencial', now.strftime("%d/%m/%Y"), now.strftime("%H:%M:%S"))

        # verificar os itens do estoque final em relação ao estoque inicial
        for estoque_item_final in self.estoque_itens:
            codigo_insumo = estoque_item_final.insumo.codigo_insumo
            estoque_item_inicial = next((item_estoque for item_estoque in estoque_inicial.estoque_itens if item_estoque.insumo.codigo_insumo == codigo_insumo), None)
            if estoque_item_inicial != None:
                total_unidades_estoque_final = estoque_item_final.pacotes * estoque_item_final.insumo.unidades_pacote + estoque_item_final.unidades
                total_unidades_estoque_inicial = estoque_item_inicial.pacotes * estoque_item_inicial.insumo.unidades_pacote + estoque_item_inicial.unidades
                
                diferencial_unidades =  total_unidades_estoque_final - total_unidades_estoque_inicial
                diferencial_pacotes = diferencial_unidades // estoque_item_final.insumo.unidades_pacote # obtém apenas a parte inteira
                estoque_diferencial.adicionarItem(estoque_item_final.insumo, diferencial_pacotes, diferencial_unidades)

        # verificar os itens do estoque inicial que não constam mais no estoque final
        for estoque_item_inicial in estoque_inicial.estoque_itens:
            codigo_insumo = estoque_item_inicial.insumo.codigo_insumo
            estoque_item_final = next((item_estoque for item_estoque in self.estoque_itens if item_estoque.insumo.codigo_insumo == codigo_insumo), None)
            if estoque_item_final == None:
                estoque_diferencial.adicionarItem(estoque_item_inicial.insumo, estoque_item_inicial.pacotes, estoque_item_inicial.unidades)

        return estoque_diferencial

    def serialize(self):
        estoque_itens = []
        for estoque_item in self.estoque_itens:
            estoque_itens.append(estoque_item.serialize())

        return {
            'descricao': self.descricao,
            'data': self.data,
            'hora': self.hora,
            'estoque_itens': estoque_itens
        }