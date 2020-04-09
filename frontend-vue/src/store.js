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
      { "date": "2020-04-07T10:29:10Z", "score": 33 },
      { "date": "2020-03-28T00:18:04Z", "score": 10 },
      { "date": "2020-03-26T18:07:41Z", "score": 28 },
      { "date": "2020-03-23T23:10:35Z", "score": 39 },
      { "date": "2020-03-19T20:34:07Z", "score": 38 },
      { "date": "2020-03-15T21:40:10Z", "score": 21 },
      { "date": "2020-03-13T20:41:26Z", "score": 15 }
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
