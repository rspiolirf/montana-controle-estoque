from insumo import Insumo

class ProdutoItem:
    def __init__(self, insumo, quantidade):
        self.insumo = insumo
        self.quantidade = int(quantidade)

    def serialize(self):
        return {
            'insumo': self.insumo.serialize(),
            'quantidade': self.quantidade
        }