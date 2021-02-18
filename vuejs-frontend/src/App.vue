<template>
  <v-app>
    <appbar/>

    <v-main>
      <router-view/>
    </v-main>

    <appfooter/>
  </v-app>
</template>

<script>
import Appbar from '@/components/Appbar'
import Appfooter from '@/components/Appfooter'
import store from '@/store/store'

export default {
  name: 'App',

  components: {
    Appbar,
    Appfooter
  },

  data: () => ({
    store
  }),

  async created() {
    let response = await fetch(`${process.env.VUE_APP_BASE_URL}/api/insumos`)
    store.insumos = await response.json()

    response = await fetch(`${process.env.VUE_APP_BASE_URL}/api/produtos`)
    store.produtos = await response.json()
  }
}
</script>

<style lang="scss">
.v-toolbar__title {
  font-family: 'Bebas Neue', cursive;
  font-size: 1.75rem !important;
  letter-spacing: 1px;
  padding-top: 1px;
}
.page-title {
  font-family: 'Bebas Neue', cursive;
  font-size: 1.5rem;
  letter-spacing: 1px;
}
table thead.v-data-table-header th, .v-data-table > .v-data-table__wrapper > table > thead > tr > th {
  font-size: 1rem !important;
  color: '#cd2c16' !important;
}
.v-data-table>.v-data-table__wrapper>table>tbody>tr>td {
  font-size: 1rem !important;
}
.v-data-table > .v-data-table__wrapper tbody tr.v-data-table__expanded__content {
    box-shadow: none !important;
}
</style>
