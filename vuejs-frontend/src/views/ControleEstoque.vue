<template>
<v-container class="mt-3">
  <v-stepper
    non-linear
    v-model="e1"
    class="mb-3"
  >
    <v-stepper-header>
      <v-stepper-step
        editable
        :complete="e1 > 1"
        step="1"
      >
        Estoque Inicial
      </v-stepper-step>

      <v-divider></v-divider>

      <v-stepper-step
        editable
        :complete="e1 > 2"
        step="2"
      >
        Estoque Final
      </v-stepper-step>

      <v-divider></v-divider>

      <v-stepper-step
        editable
        :complete="e1 > 3"
        step="3">
        Relatório de Vendas
      </v-stepper-step>

      <v-divider></v-divider>

      <v-stepper-step
        :editable="habilitarContagemEstoque"
        step="4">
        Contagem do Estoque
      </v-stepper-step>
    </v-stepper-header>

    <v-stepper-items
      class="mb-3"
    >
      <v-stepper-content step="1">
        
        <v-row class="mt-3">
          <v-col>
            <v-form>
              <v-file-input
                label="Estoque Inicial"
                outlined
                dense
                truncate-length="50"
                accept=".xlsx"
                v-model="arquivoExcelEstoqueInicial"
              ></v-file-input>
            </v-form>
          </v-col>
          <v-col>
            <v-btn
              :disabled="arquivoExcelEstoqueInicial === null"
              color="primary"
              @click="importarEstoque('inicial')"
            >
              IMPORTAR ARQUIVO
            </v-btn>
          </v-col>
        </v-row>
        <v-row>
          <v-col class="text-center">
            <p class="mb-0" v-if="dadosEstoqueInicial.data">Data: {{ dadosEstoqueInicial.data }}</p>
            <p v-if="dadosEstoqueInicial.hora">Hora: {{ dadosEstoqueInicial.hora }}</p>
            <v-data-table
              sort-by="insumo.ordem"
              :loading="loading"
              loading-text="Carregando..."
              disable-pagination
              locale="pt"
              hide-default-footer
              :headers="headersEstoque"
              :items="dadosEstoqueInicial.estoque_itens"
              class="elevation-1"
              item-key="insumo.codigo_insumo"
            ></v-data-table>
          </v-col>
        </v-row>
      </v-stepper-content>

      <v-stepper-content step="2">
        <v-row class="mt-3">
          <v-col>
            <v-form>
              <v-file-input
                label="Estoque Final"
                outlined
                dense
                truncate-length="50"
                accept=".xlsx"
                v-model="arquivoExcelEstoqueFinal"
              ></v-file-input>
            </v-form>
          </v-col>
          <v-col>
            <v-btn
              :disabled="arquivoExcelEstoqueFinal === null"
              color="primary"
              @click="importarEstoque('final')"
            >
              IMPORTAR ARQUIVO
            </v-btn>
          </v-col>
        </v-row>
        <v-row>
          <v-col class="text-center">
            <p class="mb-0" v-if="dadosEstoqueFinal.data">Data: {{ dadosEstoqueFinal.data }}</p>
            <p v-if="dadosEstoqueFinal.hora">Hora: {{ dadosEstoqueFinal.hora }}</p>
            <v-data-table
              sort-by="insumo.ordem"
              :loading="loading"
              loading-text="Carregando..."
              disable-pagination
              locale="pt"
              hide-default-footer
              :headers="headersEstoque"
              :items="dadosEstoqueFinal.estoque_itens"
              class="elevation-1"
              item-key="insumo.codigo_insumo"
            ></v-data-table>
          </v-col>
        </v-row>
      </v-stepper-content>

      <v-stepper-content step="3">
        <v-row class="mt-3">
          <v-col>
            <v-form>
              <v-file-input
                label="Relatório de Vendas"
                outlined
                dense
                truncate-length="50"
                accept=".xlsx"
                v-model="arquivoExcelRelatorioVendas"
              ></v-file-input>
            </v-form>
          </v-col>
          <v-col>
            <v-btn
              :disabled="arquivoExcelRelatorioVendas === null"
              color="primary"
              @click="importarRelatorioVendas()"
            >
              IMPORTAR ARQUIVO
            </v-btn>
          </v-col>
        </v-row>
        <v-row>
          <v-col class="text-center">
            <p class="mb-0" v-if="dadosRelatorioVendas">{{ dadosRelatorioVendas.data }}</p>
            <v-data-table v-if="dadosRelatorioVendas"
              :loading="loading"
              loading-text="Carregando..."
              disable-pagination
              locale="pt"
              hide-default-footer
              :headers="headersRelatorioVendas"
              :items="dadosRelatorioVendas.vendas_itens"
              class="elevation-1"
              item-key="produto.codigo_produto"
            ></v-data-table>
          </v-col>
        </v-row>
      </v-stepper-content>

      <v-stepper-content step="4">
        <v-row>
          <v-col class="text-center">
            <v-btn
              color="primary"
              @click="processarContagemEstoque"
            >
              PROCESSAR
            </v-btn>
            <v-btn
              :loading="loadingExportarContagemEstoque"
              class="ml-3"
              color="success"
              @click="exportarParaExcel"
            >
              EXPORTAR PARA EXCEL
            </v-btn>
          </v-col>
        </v-row>
        <v-row class="mb-6">
          <v-col class="text-center">
            <v-data-table
              id="tabela"
              ref="tabela"
              sort-by="ordem"
              :loading="loading"
              loading-text="Carregando..."
              disable-pagination
              locale="pt"
              hide-default-footer
              :headers="headersContagemEstoque"
              :items="store.dadosContagemEstoque.relatorio_itens"
              class="elevation-1"
              item-key="produto.codigo_produto"
            >
              <template v-slot:[`header.estoque_inicial`]="{ header }">
                <v-row>
                  <v-col class="pb-0">
                    {{ header.text }}
                    <p class="text-body-2 mb-0">{{ store.dadosContagemEstoque.data_estoque_inicial }}</p>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col>Pct</v-col>
                  <v-col>Un</v-col>
                  <v-col>Total</v-col>
                </v-row>
              </template>

              <template v-slot:[`header.estoque_final`]="{ header }">
                <v-row>
                  <v-col class="pb-0">
                    {{ header.text }}
                    <p class="text-body-2 mb-0">{{ store.dadosContagemEstoque.data_estoque_final }}</p>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col>Pct</v-col>
                  <v-col>Un</v-col>
                  <v-col>Total</v-col>
                </v-row>
              </template>
              
              <template v-slot:[`item.estoque_inicial`]="{ item }">
                <v-row>
                  <v-col style="background-color: lavender;">{{ item.estoque_inicial_pacotes }}</v-col>
                  <v-col style="background-color: lightblue;">{{ item.estoque_inicial_unidades }}</v-col>
                  <v-col style="background-color: bisque;">{{ item.estoque_inicial_total }}</v-col>
                </v-row>
              </template>

              <template v-slot:[`item.estoque_final`]="{ item }">
                <v-row>
                  <v-col style="background-color: lavender;">{{ item.estoque_final_pacotes }}</v-col>
                  <v-col style="background-color: lightblue;">{{ item.estoque_final_unidades }}</v-col>
                  <v-col style="background-color: bisque;">{{ item.estoque_final_total }}</v-col>
                </v-row>
              </template>

              <template v-slot:[`item.flag`]="{ item }">
                  <v-icon
                    :color="obterCor(item.diferencial, item.vendas)"
                  >
                    {{ Math.abs(item.diferencial) === Math.abs(item.vendas) ? 'mdi-thumb-up' : 'mdi-thumb-down' }}
                  </v-icon>
              </template>
            </v-data-table>
          </v-col>
        </v-row>
      </v-stepper-content>
    </v-stepper-items>
  </v-stepper>
</v-container>
</template>

<script>
import store from '../store/store'

export default {
  name: 'ControleEstoque',

  data: () => ({
    store,
    e1: 1,
    arquivoExcelEstoqueInicial: null,
    dadosEstoqueInicial: [],
    loading: false,
    
    arquivoExcelEstoqueFinal: null,
    dadosEstoqueFinal: [],

    arquivoExcelRelatorioVendas: null,
    dadosRelatorioVendas: [],

    loadingContagemEstoque: false,
    loadingExportarContagemEstoque: false,

    headersEstoque: [
      { text: 'Codigo', align: ' d-none', value: 'insumo.codigo_insumo', sortable: true },
      { text: 'Descrição', align: 'start', sortable: true, value: 'insumo.descricao' },
      { text: 'Pacotes', align: 'center', sortable: false, value: 'pacotes' },
      { text: 'Unidades', align: 'center', sortable: false, value: 'unidades' },
      { text: 'Total', align: 'center', sortable: false, value: 'total' }
    ],

    headersRelatorioVendas: [
      { text: 'Codigo', align: 'center', value: 'produto.codigo_produto', sortable: true },
      { text: 'Descrição', align: 'start', sortable: true, value: 'produto.descricao' },
      { text: 'Quantidade', align: 'center', sortable: false, value: 'quantidade' },
    ],

    headersContagemEstoque: [
      { text: 'Codigo', align: ' d-none', value: 'codigo_insumo', sortable: true },
      { text: 'Descrição', align: 'start', sortable: true, value: 'descricao' },
      { text: 'Estoque Inicial', align: 'center', sortable: false, value: 'estoque_inicial' },
      { text: 'Estoque Final', align: 'center', sortable: false, value: 'estoque_final' },
      { text: 'Diferencial', align: 'center', sortable: false, value: 'diferencial' },
      { text: 'Vendas', align: 'center', sortable: false, value: 'vendas' },
      { text: '', align: 'center', sortable: false, value: 'flag' },
    ]
  }),

  mounted() {
    window.scrollTo(0, 0)
  },

  methods: {
    async importarEstoque(tipo) {
      this.loading = true
      const arquivoExcelEstoque = tipo === 'inicial' ? this.arquivoExcelEstoqueInicial : this.arquivoExcelEstoqueFinal

      const formData = new FormData()
      formData.append("file", arquivoExcelEstoque, arquivoExcelEstoque.name)

      const response = await fetch(`${process.env.VUE_APP_BASE_URL}/api/uploadestoque?tipo=${tipo}`, {
        method: 'POST',
        body: formData
      })

      if (tipo === 'inicial') {
        this.dadosEstoqueInicial = await response.json()
      }
      else {
        this.dadosEstoqueFinal = await response.json()        
      }
      this.loading = false
    },

    async importarRelatorioVendas() {
      this.loading = true
      const formData = new FormData()
      formData.append("file", this.arquivoExcelRelatorioVendas, this.arquivoExcelRelatorioVendas.name)

      const response = await fetch(`${process.env.VUE_APP_BASE_URL}/api/uploadrelatoriovendas`, {
        method: 'POST',
        body: formData
      })
      this.dadosRelatorioVendas = await response.json()
      this.loading = false
    },

    async processarContagemEstoque() {
      this.loading = true
      const response = await fetch(`${process.env.VUE_APP_BASE_URL}/api/processarcontagemestoque`)
      store.dadosContagemEstoque = await response.json()
      this.loading = false
    },

    async exportarParaExcel() {
      this.loadingExportarContagemEstoque = true
      await fetch(`${process.env.VUE_APP_BASE_URL}/api/contagemestoqueparaexcel`)      
      this.loadingExportarContagemEstoque = false
      window.location = `${process.env.VUE_APP_BASE_URL}/resultado.xlsx`
    },

    obterCor(diferencial, vendas) {
      return Math.abs(diferencial) === Math.abs(vendas) ? 'green' : 'red'
    }
  },

  computed: {
    habilitarContagemEstoque() {
      return true
      // if (this.dadosEstoqueInicial.data && 
      //       this.dadosEstoqueFinal.data && 
      //       this.dadosRelatorioVendas.data)
      //   return true
      // else
      //   return false
    }
  },

  watch: {
    dadosEstoqueInicial() {
      store.dadosContagemEstoque = {}
    },

    dadosEstoqueFinal() {
      store.dadosContagemEstoque = {}
    },

    dadosRelatorioVendas() {
      store.dadosContagemEstoque = {}
    }
  }
}
</script>