import axios from '@/axios'

// User
function signupUser(email) {
  let req = {email}
  return axios.post('/register/', req)
}
function confirmUser(token) {
  let req = {token}
  return axios.post('/register/confirm/', req)
}

export default {
  signupUser,
  confirmUser
}
