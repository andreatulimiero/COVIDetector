<template>
  <div id="signup">
    <header>
      <img src="../assets/covid.jpg" id="covid">
      <h1>COVIDetector</h1>
      <p class="lead">Help the world's scientific community!</p> 
    </header>
    <div class="card container">
      <div class="card-body">
        <h4>Help early disease detection by sharing anonymized voice samples!</h4>
        <br/>
        <form class="form">
          <div class="form-row">
            <div class="form-group col-md-8">
              <input type="email"
                     class="form-control"
                     aria-describedby="emailHelp"
                     placeholder="Enter email"
                     v-model="email"> <small id="emailHelp" class="form-text text-muted"> Your email will be used only to check that you are a real person
              </small>
            </div>
            <div class="form-group col-md-4">
              <button type="submit" @click="signup" class="btn btn-primary mb-2">Signup</button>
            </div>
          </div>
        </form>
        <p>Already have a confirmation token? Click <router-link to="confirm">here</router-link></p>
      </div>
    </div>
  </div>
</template>

<script>
  const axios = require('axios');
  export default {
    name: "Signup",
    data() {
      return {
        /*age_options: [
          {value: null, text: "Prefer not to say"},
          {value: '1', text: "0-9"},
          {value: '2', text: "10-19"},
          {value: '3', text: "20-29"},
          {value: '4', text: "30-39"},
          {value: '5', text: "40-49"},
          {value: '6', text: "50-59"},
          {value: '7', text: "60-69"},
          {value: '8', text: "70-79"},
          {value: '9', text: "80-89"},
          {value: '10', text: "90-99"},
          {value: '11', text: "100+"}
        ],
        gender_options: [
          {value: null, text: "Prefer not to say"},
          {value: 'M', text: "Male"},
          {value: 'F', text: "Female"},
        ],*/
        email: "",
      }
    },
    methods: {
      signup() {
        //this.$emit("authenticated", true); ?
        console.log('Registering ', this.email)
        axios.post('http://localhost:8000/api/register/', {
          email: this.email
        }).then((res) => {
          console.log(res)
          this.$router.push({name: "confirm"});
        }).catch((err) => {
          console.log(err)
        })
      }
    }
  }
</script>

<style>
#signup > header {
  text-align: center;
}
#covid {
  width: 100px;
}
</style>
