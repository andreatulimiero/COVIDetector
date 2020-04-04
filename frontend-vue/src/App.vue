<template>
  <div id="app">
    <div id="nav">
      <router-link v-if="authenticated" to="/signup" v-on:click.native="replace()" replace>Replace Session</router-link>
    </div>
    <router-view @authenticated="setAuthenticated" />
  </div>
</template>

<script>
export default {
  name: 'App',
  data () {
    return {
      authenticated: false,
    }
  },
  mounted() {
    if (!this.authenticated){
      this.$router.replace({name: "signup"});
    }
  },
  methods: {
    setAuthenticated(status) {
      this.authenticated = status;
    },
    replace() {
      this.authenticated = false;
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
