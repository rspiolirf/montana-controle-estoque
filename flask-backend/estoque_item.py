class EstoqueItem:
    def __init__(self, insumo, pacotes, unidades):
        self.insumo = insumo
        self.pacotes = int(pacotes)
        self.unidades = int(unidades)
        self.total = self.unidades + (self.pacotes * self.insumo.unidades_pacote)

    def serialize(self):
        return {
            'insumo': self.insumo.serialize(),
            'pacotes': self.pacotes,
            'unidades': self.unidades,
            'total': self.total
        }