<template>
  <v-container
    class="mt-6">

    <v-row>
      <v-col>
        <v-card
          class="mx-auto"
        >
          <v-card-text
            class="py-0"
          >
            <v-row>
              <v-col style="padding-top: 20px;">
                <span class="page-title primary--text">PRODUTOS</span>
              </v-col>
              <v-col class="text-right">
                <v-btn
                  dark
                  color="primary"
                  @click="abrirDialogoProduto({}, true)"
                  >INSERIR
                </v-btn>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <v-data-table
          show-expand
          :expanded="store.produtos"
          disable-pagination
          locale="pt"
          hide-default-footer
          :headers="headers"
          :items="store.produtos"
          item-key="codigo_produto"
        >
          <template v-slot:[`item.actions`]="{ item }">
            <v-icon
              color="primary"
              @click="abrirDialogoProduto(item, false)"
            >
              mdi-pencil
            </v-icon>
            <v-icon
              color="primary"
              @click="confimarDelecaoProduto(item)"
            >
              mdi-delete
            </v-icon>
          </template>
          <template v-slot:expanded-item="{ headers, item }">
            <td :colspan="headers.length" class="py-3">
              <v-row>
                <v-col></v-col>
                <v-col>
                  <p
                    class="mb-0"
                    v-for="produto_item in item.produto_itens"
                    :key="produto_item.insumo.codigo_insumo">
                    {{ produto_item.quantidade }} - {{ produto_item.insumo.descricao}} (código: {{ produto_item.insumo.codigo_insumo }})
                  </p>  
                </v-col>
              </v-row>
            </td>
          </template>
        </v-data-table>
      </v-col>
    </v-row>

    <v-row justify="center">
      <v-dialog v-model="produtoDialogo" persistent max-width="600px">
        <v-card>
          <v-card-text>
            <v-container>
              <v-row class="mt-4">
                <v-col cols="3">
                  <v-text-field
                    label="Código"
                    placeholder=" "
                    outlined
                    dense
                    hide-details="auto"
                    v-model="produto.codigo_produto"
                  ></v-text-field>
                </v-col>
              </v-row>

              <v-row class="mt-4">
                <v-col>
                  <v-text-field
                    label="Descrição"
                    placeholder=" "
                    outlined
                    dense
                    hide-details="auto"
                    v-model="produto.descricao"
                  ></v-text-field>
                </v-col>
              </v-row>

            </v-container>
          </v-card-text>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary dark" text @click="cancelarDialogoProduto">Cancelar</v-btn>
            <v-btn :disabled="desabilitarBotaoSalvar" class="mr-5" color="blue darken-1" text @click="salvar">Salvar</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>

    <v-snackbar
      v-model="exibirSnackbar"
      top
    >
      {{ snackbarMensagem }}
      <template v-slot:action="{ attrs }">
        <v-btn
          color="primary"
          text
          v-bind="attrs"
          @click="exibirSnackbar = false"
        >
          Fechar
        </v-btn>
      </template>
    </v-snackbar>

    <v-dialog v-model="confirmaExclusaoDialogo" persistent max-width="290">
      <v-card>
        <v-card-title class="headline">Excluir Produto</v-card-title>
        <v-card-text>Você tem certeza que deseja excluir o produto {{ this.produto.descricao }} (Código: {{ this.produto.codigo_produto }})? Esta ação não pode ser desfeita.</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="yellow darken-1" text @click="confirmaExclusaoDialogo = false">Cancelar</v-btn>
          <v-btn class="mr-5" color="red darken-1" text @click="deletarProduto">Excluir</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </v-container>
</template>

<script>
import store from '@/store/store'

export default {
  name: 'Produto',

  data: () => ({
    store,
    produtos: [],
    produto: {},
    produtoDialogo: false,
    desabilitarBotaoSalvar: false,
    ehNovoProduto: false,
    exibirSnackbar: false,
    snackbarMensagem: '',
    confirmaExclusaoDialogo: false,
    headers: [
      { text: 'Ingredientes', value: 'data-table-expand' },
      { text: 'Codigo', align: 'center', value: 'codigo_produto', sortable: true },
      { text: 'Descrição', align: 'start', sortable: true, value: 'descricao' },
      { text: 'Ações', align: 'center', value: 'actions', sortable: false }
    ]
  }),

  methods: {
    abrirDialogoProduto(item, ehNovoProduto) {
      this.ehNovoProduto = ehNovoProduto
      if (ehNovoProduto === false)
        this.produto = {...item}
      this.produtoDialogo = true
    },

    cancelarDialogoProduto() {
      this.produto = {}
      this.produtoDialogo = false
    },

    salvar() {
      if (this.ehNovoProduto) {
        // verifica se já existem um produto com o mesmo código
        const produto = store.produtos.find(i => i.codigo_produto === this.produto.codigo_produto)

        if (produto === undefined) {
          store.produtos.push(this.produto)
          store.produtos.sort((a, b) => (Number(a.codigo_produto) > Number(b.codigo_produto)) ? 1 : ((Number(b.codigo_produto) > Number(a.codigo_produto)) ? -1 : 0))
          this.persistirAlteracoes()
        }
        else {
          this.snackbarMensagem = `Já existe um produto com o código ${this.produto.codigo_produto}. Não é possível adicionar dois produtos com o mesmo código.`
          this.exibirSnackbar = true
        }
      }
      else {
        const produto = store.produtos.find(i => i.codigo_produto === this.produto.codigo_produto)
        produto.descricao = this.produto.descricao
        produto.unidades_pacote = this.produto.unidades_pacote
        this.persistirAlteracoes()
      }
    },

    async persistirAlteracoes() {
      await fetch(`${process.env.VUE_APP_BASE_URL}/api/produtos`, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(store.produtos)
      })
      this.produto = {}
      this.produtoDialogo = false
    },

    confimarDelecaoProduto(item) {
      this.produto = item
      this.confirmaExclusaoDialogo = true
    },

    deletarProduto() {
      store.produtos = store.produtos.filter(i => i.codigo_produto !== this.produto.codigo_produto)
      this.produto = {}
      this.confirmaExclusaoDialogo = false
      this.persistirAlteracoes()
    }
  }
}
</script>