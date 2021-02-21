class VendasItem:
    def __init__(self, produto, quantidade):
        self.produto = produto
        self.quantidade = quantidade
  
    def serialize(self):
        return {
            'produto': self.produto.serialize(),
            'quantidade': self.quantidade
        }