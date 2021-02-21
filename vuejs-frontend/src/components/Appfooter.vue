<template>
  <v-footer>
    <div><span class="text-body-2">Versão 1.2</span></div>
    <v-spacer></v-spacer>
    <div>José Elias &amp; Priscila &copy; {{ new Date().getFullYear() }}</div>
  </v-footer>
</template>

<script>
export default {
  computed: {
    dataCompilacao() {
      return `${process.env.VUE_APP_BUILD_DATE}`
    }
  }
}
</script>