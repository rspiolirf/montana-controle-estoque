<template>
  <v-container
    fill-height>
    <v-row>
      <v-col
        class="ml-12 text-center">
        <h1 class="titulo_home primary--text pr-12">CONTROLE DE ESTOQUE</h1>
        <v-img
          contain
          max-height="300"
          src="../assets/undraw_Data_trends_re_2cdy.svg"
        ></v-img>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'Home',

  components: {
  }
}
</script>

<style lang="scss">
.titulo_home {
  font-family: 'Bebas Neue', cursive;
  letter-spacing: 1.5px;
}
</style>
