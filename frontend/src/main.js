import Vue from 'vue'
import App from '@/App.vue'
import router from '@/router'
import store from '@/store'

Vue.config.productionTip = false

function loadStorage() {
  let token = localStorage.getItem('token')
  let secret = localStorage.getItem('secret')
  if (token !== null && secret !== null) {
    store.commit('saveAuth', {token, secret})
  }
}
loadStorage()

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
