<template>
  <v-app-bar
    app
    color="primary"
    dense
    dark
  >
    <v-img
      style="cursor: pointer"
      @click="irParaHome"
      contain
      src="../assets/logotipo.png"
      height="32"
      max-width="140"
    ></v-img>
    <v-spacer></v-spacer>
    <v-btn depressed color="primary" to="/insumos">Insumos</v-btn>
    <v-btn depressed color="primary" to="/produtos">Produtos</v-btn>
    <v-btn depressed color="primary" to="/controleestoque">Controle de Estoque</v-btn>
  </v-app-bar>    
</template>

<script>
export default {
  methods: {
    irParaHome() {
      if (this.$route.name !== 'Home')
        this.$router.push('/')
    }
  }
}
</script>

// #fede20 amarelo
// vermelho #cd2c16