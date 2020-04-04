<template>
  <div id="confirm">
    <header>
      <img src="../assets/covid.jpg" id="covid">
      <h1>COVIDetector</h1>
      <p class="lead">Help the world's scientific community!</p> 
    </header>
    <div class="card container">
      <div class="card-body">
        <h4>Insert here the code you received via email</h4>
        <br/>
        <form class="form">
          <div class="form-row">
            <div class="form-group col-md-8">
              <input type="text"
                     class="form-control"
                     aria-describedby="emailHelp"
                     placeholder="Enter code"
                     v-model="token"> <small id="emailHelp" class="form-text text-muted"> Your email will be used only to check that you are a real person
              </small>
            </div>
            <div class="form-group col-md-4">
              <button type="submit" @click="confirm" class="btn btn-primary mb-2">Confirm</button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
  const axios = require('axios');
  export default {
    name: "Confirm",
    data() {
      return {
        token: "",
      }
    },
    methods: {
      confirm() {
        console.log('Token ', this.token)
        axios.post('http://localhost:8000/api/register/confirm/', {
          token: this.token
        }).then((res) => {
          console.log(res)
          localStorage.setItem('token', res.data.token)
          localStorage.setItem('secret', res.data.secret)
          this.$router.push({name: "submit"});
        }).catch((err) => {
          console.log(err)
        })
      }
    }
  }
</script>

<style>
#confirm > header {
  text-align: center;
}
#covid {
  width: 100px;
}
</style>
