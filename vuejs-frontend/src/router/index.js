import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/produtos',
    name: 'Produto',
    component: () => import('../views/Produto.vue')
  },
  {
    path: '/insumos',
    name: 'Insumo',
    component: () => import('../views/Insumo.vue')
  },
  {
    path: '/controleestoque',
    name: 'ControleEstoque',
    component: () => import('../views/ControleEstoque.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
