<template>
  <div id="app">
    <navbar v-if="showNavbar"></navbar>
    <main class="container">
      <router-view/>
    </main>
  </div>
</template>

<script>
// @ is an alias to /src
import Navbar from '@/components/Navbar.vue'
export default {
  name: 'App',
  components: {
    Navbar
  },
  computed: {
    showNavbar() { return this.$store.getters.isLoggedIn }
  }
}
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
