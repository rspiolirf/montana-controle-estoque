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
                <span class="page-title primary--text">INSUMOS</span>
              </v-col>
              <v-col class="text-right">
                <v-btn
                  dark
                  color="primary"
                  @click="abrirDialogoInsumo({}, true)"
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
          disable-pagination
          locale="pt"
          hide-default-footer
          :headers="headers"
          :items="store.insumos"
          item-key="codigo_insumo"
        >
          <template v-slot:[`item.actions`]="{ item }">
            <v-icon
              color="primary"
              @click="abrirDialogoInsumo(item, false)"
            >
              mdi-pencil
            </v-icon>
            <v-icon
              color="primary"
              @click="confimarDelecaoInsumo(item)"
            >
              mdi-delete
            </v-icon>
          </template>
        </v-data-table>
      </v-col>
    </v-row>

    <v-row justify="center">
      <v-dialog v-model="insumoDialogo" persistent max-width="600px">
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
                    v-model="insumo.codigo_insumo"
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
                    v-model="insumo.descricao"
                  ></v-text-field>
                </v-col>
              </v-row>

              <v-row class="mt-4">
                <v-col cols="6">
                  <v-text-field
                    label="Unidades por Pacote"
                    placeholder=" "
                    outlined
                    dense
                    hide-details="auto"
                    v-model="insumo.unidades_pacote"
                  ></v-text-field>
                </v-col>
              </v-row>

            </v-container>
          </v-card-text>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary dark" text @click="cancelarDialogoInsumo">Cancelar</v-btn>
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
        <v-card-title class="headline">Excluir Insumo</v-card-title>
        <v-card-text>Você tem certeza que deseja excluir o insumo {{ this.insumo.descricao }} (Código: {{ this.insumo.codigo_insumo }})? Esta ação não pode ser desfeita.</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="yellow darken-1" text @click="confirmaExclusaoDialogo = false">Cancelar</v-btn>
          <v-btn class="mr-5" color="red darken-1" text @click="deletarInsumo">Excluir</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </v-container>
</template>

<script>
import store from '@/store/store'

export default {
  name: 'Insumo',

  data: () => ({
    store,
    insumos: [],
    insumo: {},
    insumoDialogo: false,
    desabilitarBotaoSalvar: false,
    ehNovoInsumo: false,
    exibirSnackbar: false,
    snackbarMensagem: '',
    confirmaExclusaoDialogo: false,
    headers: [
      { text: 'Codigo', align: 'center', value: 'codigo_insumo', sortable: true },
      { text: 'Descrição', align: 'start', sortable: true, value: 'descricao' },
      { text: 'Unidades por Pacote', align: 'start', sortable: false, value: 'unidades_pacote' },
      { text: 'Ações', align: 'center', value: 'actions', sortable: false }
    ]
  }),

  methods: {
    abrirDialogoInsumo(item, ehNovoInsumo) {
      this.ehNovoInsumo = ehNovoInsumo
      if (ehNovoInsumo === false)
        this.insumo = {...item}
      this.insumoDialogo = true
    },

    cancelarDialogoInsumo() {
      this.insumo = {}
      this.insumoDialogo = false
    },

    salvar() {
      if (this.ehNovoInsumo) {
        // verifica se já existem um insumo com o mesmo código
        const insumo = store.insumos.find(i => i.codigo_insumo === this.insumo.codigo_insumo)

        if (insumo === undefined) {
          store.insumos.push(this.insumo)
          store.insumos.sort((a, b) => (Number(a.codigo_insumo) > Number(b.codigo_insumo)) ? 1 : ((Number(b.codigo_insumo) > Number(a.codigo_insumo)) ? -1 : 0))
          this.persistirAlteracoes()
        }
        else {
          this.snackbarMensagem = `Já existe um insumo com o código ${this.insumo.codigo_insumo}. Não é possível adicionar dois insumos com o mesmo código.`
          this.exibirSnackbar = true
        }
      }
      else {
        const insumo = store.insumos.find(i => i.codigo_insumo === this.insumo.codigo_insumo)
        insumo.descricao = this.insumo.descricao
        insumo.unidades_pacote = this.insumo.unidades_pacote
        this.persistirAlteracoes()
      }
    },

    async persistirAlteracoes() {
      await fetch(`${process.env.VUE_APP_BASE_URL}/api/insumos`, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(store.insumos)
      })
      this.insumo = {}
      this.insumoDialogo = false
    },

    confimarDelecaoInsumo(item) {
      this.insumo = item
      this.confirmaExclusaoDialogo = true
    },

    deletarInsumo() {
      store.insumos = store.insumos.filter(i => i.codigo_insumo !== this.insumo.codigo_insumo)
      this.insumo = {}
      this.confirmaExclusaoDialogo = false
      this.persistirAlteracoes()
    }
  }
}
</script>
