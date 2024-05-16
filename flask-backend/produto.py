from produto_item import ProdutoItem

class Produto:
    def __init__(self, codigo_produto, descricao, produto_itens):
        self.codigo_produto = codigo_produto
        self.descricao = descricao
        self.produto_itens = produto_itens

    def verificarQuantidadeDeInsumo(self, codigo_insumo):
        result = next(produto_item for produto_item in self.produto_itens if produto_item.insumo.codigo_insumo == codigo_insumo)
        return result.quantidade

    def serialize(self):
        produto_itens = []
        for produto_item in self.produto_itens:
            produto_itens.append(produto_item.serialize())

        return {           
            'codigo_produto': self.codigo_produto, 
            'descricao': self.descricao,
            'produto_itens': produto_itens
        }