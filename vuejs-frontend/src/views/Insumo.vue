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
          sort-by="ordem"
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

              <v-row class="mt-4">
                <v-col cols="6">
                  <v-text-field
                    label="Ordem de Apresentação"
                    placeholder=" "
                    outlined
                    dense
                    hide-details="auto"
                    v-model="insumo.ordem"
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
          <v-btn class="mr-5" color="red darken-1" text @click="excluirInsumo">Excluir</v-btn>
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
    insumo: {},
    insumoDialogo: false,
    ehNovoInsumo: false,
    exibirSnackbar: false,
    snackbarMensagem: '',
    confirmaExclusaoDialogo: false,
    headers: [
      { text: 'Ordem', align: 'center', value: 'ordem', sortable: true },
      { text: 'Codigo', align: 'center', value: 'codigo_insumo', sortable: true },
      { text: 'Descrição', align: 'start', sortable: true, value: 'descricao' },
      { text: 'Unidades por Pacote', align: 'center', sortable: false, value: 'unidades_pacote' },
      { text: 'Ações', align: 'center', value: 'actions', sortable: false }
    ]
  }),

  async created() {
    if (store.insumos.length === 0) {
      let response = await fetch(`${process.env.VUE_APP_BASE_URL}/api/insumos`)
      store.insumos = await response.json()
    }
  },

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
        this.salvarNovoInsumo()
      }
      else {
        this.salvarInsumoExistente()
      }
    },

    insumoJaExiste() {
      const insumo = store.insumos.find(i => i.codigo_insumo === this.insumo.codigo_insumo)
      if (insumo === undefined)
        return false
      else
        this.snackbarMensagem = `O insumo ${insumo.descricao} já está cadastrado com o código ${this.insumo.codigo_insumo}. Não é possível adicionar dois insumos com o mesmo código.`
        this.exibirSnackbar = true
        return true
    },

    async salvarNovoInsumo() {
      if (this.insumoJaExiste()) return

      store.insumos.push(this.insumo)
      store.insumos.sort((a, b) => (Number(a.ordem) > Number(b.ordem)) ? 1 : ((Number(b.ordem) > Number(a.ordem)) ? -1 : 0))
          
      await fetch(`${process.env.VUE_APP_BASE_URL}/api/insumos`, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(this.insumo)
      })
      this.insumo = {}
      this.insumoDialogo = false
    },

    async salvarInsumoExistente() {
      const insumo = store.insumos.find(i => i.codigo_insumo === this.insumo.codigo_insumo)
      insumo.descricao = this.insumo.descricao
      insumo.unidades_pacote = this.insumo.unidades_pacote
      insumo.ordem = this.insumo.ordem

      await fetch(`${process.env.VUE_APP_BASE_URL}/api/insumos/${this.insumo.codigo_insumo}`, {
        method: 'PUT',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(this.insumo)
      })

      this.insumo = {}
      this.insumoDialogo = false
    },

    confimarDelecaoInsumo(item) {
      this.insumo = item
      this.confirmaExclusaoDialogo = true
    },

    async excluirInsumo() {
      try {
        await fetch(`${process.env.VUE_APP_BASE_URL}/api/insumos/${this.insumo.codigo_insumo}`, {
          method: 'DELETE'
        })

        store.insumos = store.insumos.filter(i => i.codigo_insumo !== this.insumo.codigo_insumo)
        this.insumo = {}
        this.confirmaExclusaoDialogo = false
      }
      catch {
        console.log('erro ao excluir um insumo')
      }
    }
  },

  computed: {
    desabilitarBotaoSalvar() {
      if (this.insumo && 
          this.insumo.codigo_insumo && 
          this.insumo.descricao &&
          this.insumo.unidades_pacote &&
          this.insumo.ordem)
          return false
      else
        return true
    }
  }
}
</script>
