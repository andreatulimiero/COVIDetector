<template>
  <div id="app">
    <navbar v-if="showNavbar"></navbar>
    <main class="container">
      <router-view/>
    </main>
    <AppFooter></AppFooter>
  </div>
</template>

<script>
// @ is an alias to /src
import Navbar from '@/components/Navbar.vue'
import AppFooter from '@/components/AppFooter.vue'
export default {
  name: 'App',
  components: {
    Navbar,
    AppFooter
  },
  computed: {
    showNavbar() { return this.$store.getters.isLoggedIn },
  }
}
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  min-height: 100vh;
  position: relative;
  margin: 0;
  padding-bottom: 60px;
}
</style>
