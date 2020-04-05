<template>
  <div id="signup">
    <header>
      <img src="../assets/covid.jpg" id="covid">
      <h1>COVIDetector</h1>
      <p class="lead">Help the world's scientific community!</p>
    </header>
    <article class="row justify-content-center">
      <div class="card col-10 col-md-8">
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
      <div class="card col-10 col-md-8">
        <div class="card-body">
          <h4>What does our service provide?</h4>
          <br/>
          Our aim is to provide the scientific community with a collection of <em>anonymized</em> voice data samples that will help further research efforts. In addition, this service aims to provide a mean to test users whether or not they will become sick in the upcoming days. This means, with COVIDetector, in the future, one can:
          <br/>
          <ul>
            <li>Check the probability, using one of our machine learning models, the likelyhood they will become sick in the upcoming days</li>
            <li>Provide a completely <em>anonymized</em> dataset that can be downloaded by anyone to further research studies</li>
            <li>Open source all aspects of this project, including the website, backend, and the machine learning algorithms, so that the community can further improve on our work. <a href="https://github.com/andreatulimiero/COVIDetector">Link to the project on Github.</a></li>
          </ul>
          <p>However, to make this project come to light, we need voice samples collected from the public. We encourage you to sign up and upload a voice sample, and then once we have enough, we can properly train the model to start detection.</p>
        </div>
      </div>
      <div class="card col-10 col-md-8">
        <div class="card-body">
          <h4>Medical Advice</h4>
          <p>We hope that this service can be of the most use to the public. We envision that our product will work well and will correctly detect diseases early. However, this service should only serve to inform the user on whether or not they will be contagious in the upcoming days, and should not be used as a replacement for a doctor.</p>
        </div>
      </div>
    </article>
  </div>
</template>

<script>
  import api from '@/api.js'
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
        api.signupUser(this.email).then((res) => {
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
