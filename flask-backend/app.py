import os
import config
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from os import listdir
from os.path import isfile, join
from openpyxl import Workbook

from repositorio_insumo_excel import RepositorioInsumo
from repositorio_produto_excel import RepositorioProduto
from repositorio_estoque_excel import RepositorioEstoque
from repositorio_vendas_excel import RepositorioVendas
from tipo_estoque import TipoEstoque

app = Flask(__name__, static_url_path='')
CORS(app)

repositorio_insumo = RepositorioInsumo()
repositorio_produto = RepositorioProduto(repositorio_insumo)


@app.route('/')
def get():
    return app.send_static_file('index.html')


# insumos
@app.route('/api/insumos', methods=['GET'])
def obter_insumos():
    insumos = repositorio_insumo.ObterTodos()
    result = []
    for insumo in insumos:
        result.append(insumo.serialize())

    return jsonify(result)


@app.route('/api/insumos', methods=['POST'])
def adicionar_insumo():
    insumoInputModel = request.json
    repositorio_insumo.Adicionar(insumoInputModel)

    return jsonify(success=True)


@app.route('/api/insumos/<id>', methods=['PUT'])
def atualizar_insumo(id):
    insumoInputModel = request.json
    repositorio_insumo.Atualizar(insumoInputModel)

    insumos = repositorio_insumo.ObterTodos()
    result = []
    for insumo in insumos:
        result.append(insumo.serialize())

    return jsonify(result)


@app.route('/api/insumos/<id>', methods=['DELETE'])
def excluir_insumo(id):
    repositorio_insumo.Excluir(id)
    return jsonify(success=True)


# produtos
@app.route('/api/produtos', methods=['GET'])
def obter_produtos():
    produtos = repositorio_produto.ObterTodos()
    result = []
    for produto in produtos:
        result.append(produto.serialize())

    return jsonify(result)


@app.route('/api/produtos', methods=['POST'])
def inserir_produto():
    produtoInputModel = request.json
    repositorio_produto.Adicionar(produtoInputModel)

    produtos = repositorio_produto.ObterTodos()
    result = []
    for produto in produtos:
        result.append(produto.serialize())

    return jsonify(result)


@app.route('/api/produtos/<id>', methods=['PUT'])
def atualizar_produto(id):
    produtoInputModel = request.json
    repositorio_produto.Atualizar(produtoInputModel)

    produtos = repositorio_produto.ObterTodos()
    result = []
    for produto in produtos:
        result.append(produto.serialize())

    return jsonify(result)


@app.route('/api/produtos/<id>', methods=['DELETE'])
def excluir_produto(id):
    repositorio_produto.Excluir(id)
    return jsonify(success=True)


# estoque
@app.route('/api/uploadestoque', methods=['POST'])
def upload_estoque():
    # apagar arquivos existentes
    pasta = config.estoque['pasta']
    pasta_estoque_inicial = config.estoque['pasta_estoque_inicial']
    pasta_estoque_final = config.estoque['pasta_estoque_final']
    pasta_destino = None

    if request.args.get('tipo') == 'inicial':
        pasta_destino = f'{pasta}/{pasta_estoque_inicial}'
    else:
        pasta_destino = f'{pasta}/{pasta_estoque_final}'

    arquivos_da_pasta = [f for f in listdir(
        './' + pasta_destino) if isfile(join('./' + pasta_destino, f))]
    for arquivo in arquivos_da_pasta:
        os.remove(f'{pasta_destino}/{arquivo}')

    # salva o arquivo na pasta correta indicada nos parâmetros da Url
    file = request.files['file']
    file.save(os.path.join(pasta_destino, file.filename))

    # obtém os dados do arquivo e retorna para o cliente
    tipo = TipoEstoque.INICIAL if request.args.get(
        'tipo') == 'inicial' else TipoEstoque.FINAL

    repositorio_estoque = RepositorioEstoque(tipo, repositorio_insumo)
    estoque = repositorio_estoque.Obter()

    return jsonify(estoque.serialize())


@app.route('/api/uploadrelatoriovendas', methods=['POST'])
def upload_relatorio_vendas():
    # apagar arquivos existentes
    pasta_destino = config.relatorio_de_vendas['pasta']
    arquivos_da_pasta = [f for f in listdir(
        './' + pasta_destino) if isfile(join('./' + pasta_destino, f))]
    for arquivo in arquivos_da_pasta:
        os.remove(f'{pasta_destino}/{arquivo}')

    # salva o arquivo na pasta correta indicada nos parâmetros da Url
    file = request.files['file']
    file.save(os.path.join(pasta_destino, file.filename))

    # obtém os dados do arquivo e retorna para o cliente

    repositorio_vendas = RepositorioVendas(repositorio_produto)
    vendas = repositorio_vendas.ObterTodas()

    return jsonify(vendas.serialize())


@app.route('/api/processarcontagemestoque', methods=['GET'])
def processar_contagem_estoque():
    repositorio_estoque_inicial = RepositorioEstoque(
        TipoEstoque.INICIAL, repositorio_insumo)
    repositorio_estoque_final = RepositorioEstoque(
        TipoEstoque.FINAL, repositorio_insumo)
    repositorio_vendas = RepositorioVendas(repositorio_produto)

    estoque_inicial = repositorio_estoque_inicial.Obter()
    estoque_final = repositorio_estoque_final.Obter()
    vendas = repositorio_vendas.ObterTodas()
    vendas_insumos = vendas.obterInsumos()

    relatorio_itens = []
    for estoque_item in estoque_inicial.estoque_itens:

        estoque_item_final = next(
            (x for x in estoque_final.estoque_itens if x.insumo.codigo_insumo == estoque_item.insumo.codigo_insumo), None)
        vendas_por_produto = next(
            (x for x in vendas_insumos if x.insumo.codigo_insumo == estoque_item.insumo.codigo_insumo), None)
        if vendas_por_produto == None:
            vendas_por_produto = 0
        else:
            vendas_por_produto = vendas_por_produto.quantidade

        relatorio_itens.append(
            {
                'ordem': str(estoque_item.insumo.ordem),
                'codigo_insumo': str(estoque_item.insumo.codigo_insumo),
                'descricao': estoque_item.insumo.descricao,
                'estoque_inicial_pacotes': estoque_item.pacotes,
                'estoque_inicial_unidades': estoque_item.unidades,
                'estoque_inicial_total': estoque_item.total,
                'estoque_final_pacotes': estoque_item_final.pacotes,
                'estoque_final_unidades': estoque_item_final.unidades,
                'estoque_final_total': estoque_item_final.total,
                'diferencial': estoque_item_final.total - estoque_item.total,
                'vendas': vendas_por_produto,
                'diferencial_total': estoque_item_final.total - estoque_item.total + vendas_por_produto
            })

    dadosContagemEstoque = {
        'data_estoque_inicial': estoque_inicial.data,
        'data_estoque_final': estoque_final.data,
        'relatorio_itens': relatorio_itens
    }

    return jsonify(dadosContagemEstoque)


@app.route('/api/contagemestoqueparaexcel', methods=['GET'])
def exportar_contagem_estoque():
    repositorio_estoque_inicial = RepositorioEstoque(
        TipoEstoque.INICIAL, repositorio_insumo)
    repositorio_estoque_final = RepositorioEstoque(
        TipoEstoque.FINAL, repositorio_insumo)
    repositorio_vendas = RepositorioVendas(repositorio_produto)

    estoque_inicial = repositorio_estoque_inicial.Obter()
    estoque_final = repositorio_estoque_final.Obter()
    vendas = repositorio_vendas.ObterTodas()
    vendas_insumos = vendas.obterInsumos()

    relatorio_itens = []
    for estoque_item in estoque_inicial.estoque_itens:

        estoque_item_final = next(
            (x for x in estoque_final.estoque_itens if x.insumo.codigo_insumo == estoque_item.insumo.codigo_insumo), None)
        vendas_por_produto = next(
            (x for x in vendas_insumos if x.insumo.codigo_insumo == estoque_item.insumo.codigo_insumo), None)
        if vendas_por_produto == None:
            vendas_por_produto = 0
        else:
            vendas_por_produto = vendas_por_produto.quantidade

        relatorio_itens.append(
            {
                'ordem': int(estoque_item.insumo.ordem),
                'codigo_insumo': str(estoque_item.insumo.codigo_insumo),
                'descricao': estoque_item.insumo.descricao,
                'estoque_inicial_pacotes': estoque_item.pacotes,
                'estoque_inicial_unidades': estoque_item.unidades,
                'estoque_inicial_total': estoque_item.total,
                'estoque_final_pacotes': estoque_item_final.pacotes,
                'estoque_final_unidades': estoque_item_final.unidades,
                'estoque_final_total': estoque_item_final.total,
                'diferencial_estoque': estoque_item_final.total - estoque_item.total,
                'vendas': vendas_por_produto
            })

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = 'resultado'

    sheet['A1'] = 'insumo'
    sheet['B1'] = 'estoque_final_unidades'
    sheet['C1'] = 'vendas_unidades'
    relatorio_itens_ordenados = sorted(
        relatorio_itens, key=lambda k: k['ordem'])
    for i, item in enumerate(relatorio_itens_ordenados):
        sheet['A' + str(i + 2)] = item['descricao']
        sheet['B' + str(i + 2)] = item['estoque_final_total']
        sheet['C' + str(i + 2)] = item['vendas']

    from tempfile import NamedTemporaryFile
    with NamedTemporaryFile() as tmp:
        workbook.save(tmp.name)

        tmp.seek(0)
        stream = tmp.read()

    return Response(stream, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
