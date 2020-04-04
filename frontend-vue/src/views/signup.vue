<template>
  <div id="signup">
    <h1>COVIDetector</h1>
    <div class="inner">
    <img src="../assets/covid.jpg" id="covid">
    <p>Help the world's scientific community! Simply sign up to start giving anonymized voice samples to help in early disease detection!</p>
    </div>
    <div class="inner">
    <input type="text" email="email" v-model="input.email" placeholder="e-mail">
    </div>
    <div class="inner">
    <p>Age Range:</p>
    <b-form-select v-model="input.age" :options="age_options"></b-form-select>
    </div>
    <div class="inner">
    <p>Gender:</p>
    <b-form-select v-model="input.gender" :options="gender_options"></b-form-select>
    </div>
    <div class="inner">
    <button type="button" v-on:click="signup()">Sign up</button>
    </div>
    <div class="inner">
    <h1>Download Anonymous Data for Further Research</h1>
    <p>Anonymous data of consenting users can be downloaded <a href="not working rn">here</a></p>
    </div>
  </div>
</template>

<script>
  export default {
    name: "Signup",
    data() {
      return {
        age_options: [
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
        ],
        input: {
          email: "",
          age: null,
          gender: null,
        }
      }
    },
    methods: {
      signup() {
        this.$emit("authenticated", true);
        this.$router.replace({name: "submit"});
      }
    }
  }
</script>

<style>
#covid {
  width: 10%;
  height: auto;
}
</style>
