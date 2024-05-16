from produto_item import ProdutoItem
from vendas_item import VendasItem


class Vendas:
    def __init__(self):
        self.data = None
        self.vendas_itens = []
        self.vendas_insumos = []

    def adicionarItem(self, produto, quantidade):
        self.vendas_itens.append(VendasItem(produto, quantidade))

    def obterInsumos(self):
        # obter um array de códigos de insumos vendidos distintos
        codigosInsumosDistintos = []
        for vendas_item in self.vendas_itens:
            for produto_item in vendas_item.produto.produto_itens:
                if produto_item.insumo.codigo_insumo not in codigosInsumosDistintos:
                    codigosInsumosDistintos.append(
                        produto_item.insumo.codigo_insumo)

        # realiza a somatória de vendas por insumo (consolidação)
        vendas_insumos = []
        for codigoInsumo in codigosInsumosDistintos:
            total = 0
            insumo = None
            for vendas_item in self.vendas_itens:
                for produto_item in vendas_item.produto.produto_itens:
                    if (produto_item.insumo.codigo_insumo == codigoInsumo):
                        total += int(produto_item.quantidade) * \
                            int(vendas_item.quantidade)
                        insumo = produto_item.insumo

            vendas_insumos.append(ProdutoItem(insumo, total))

        return vendas_insumos

    def serialize(self):
        vendas_itens = []
        for venda_item in self.vendas_itens:
            vendas_itens.append(venda_item.serialize())

        return {
            'data': self.data,
            'vendas_itens': vendas_itens
        }
