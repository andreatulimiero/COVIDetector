<template>
  <div id="signup">
    <h1>Signup</h1>
    <input type="text" email="email" v-model="input.email" placeholder="e-mail">
    <button type="button" v-on:click="signup()">Sign up</button>
  </div>
</template>

<script>
  export default {
    name: "Signup",
    data() {
      return {
        input: {
          email: "",
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
#signup {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
