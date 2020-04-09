import Vue from 'vue'
import Vuex from 'vuex'
import router from '@/router'
import api from '@/api'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    Auth: {
      token: "",
      secret: "",
    },
    PastRecordings: [
      {
        date: "April 2, 2020, 18:34",
        score: 20,
      },
      {
        date: "April 1, 2020, 09:34",
        score: 30,
      }
    ]
  },
  getters: {
    isLoggedIn: (state) => state.Auth.token !== "" && state.Auth.secret !== "",
  },
  mutations: {
    // User
    saveAuth: (state, {token, secret}) => {
      console.log(token)
      console.log(secret)
      state.Auth = {token: token, secret: secret}
    },
    deleteAuth:  (state) => {
      state.Auth = {token: "", state: ""}
    },
  },
  actions: {
    confirmUser({commit}, {token}) {
      return new Promise((resolve, reject) => {
        api.confirmUser(token).then(res => {
          let token = res.data.token
          let secret = res.data.secret
          commit('saveAuth', {token, secret})
          localStorage.setItem('token', token)
          localStorage.setItem('secret', secret)
          router.replace({name: 'dashboard'})
        }).catch(err => {
          reject(err)
        })
      })
    },
    logoutUser({commit}) {
      commit('deleteAuthToken')
      localStorage.clear()
      router.push('signup')
    }
  }
})
