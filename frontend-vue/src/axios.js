import axios from 'axios'
import store from '@/store'

const HTTP_FORBIDDEN = 403
const HTTP_UNAUTHORIZED = 401

const mAxios = axios.create({
  baseURL: process.env.VUE_APP_API_URL + "/api"
});

mAxios.interceptors.request.use(function (config) {
  // Add authorization tokens
  // config.headers['Authorization'] = 'Token ' + authToken
  return config
}, function (error) { return Promise.reject(error); });

mAxios.interceptors.response.use(function (res) {
  return res
}, function (err) {
  console.error(err)
  if (err.response.status === HTTP_FORBIDDEN || err.response.status === HTTP_UNAUTHORIZED) {
    store.dispatch('logoutUser')
  }
  return Promise.reject(err);
});

export default mAxios
