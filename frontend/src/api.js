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
function submitRecording(patient_token, base64_audio, sickness_status) {
  let req = {
    "patient": patient_token,
    "audio": base64_audio,
    "sick": sickness_status
  }
  return axios.post('/samples/', req)
}

export default {
  signupUser,
  confirmUser,
  submitRecording
}
