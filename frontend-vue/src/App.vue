<template>
  <div id="app">
    <navbar v-if="showNavbar"></navbar>
    <main class="container">
      <router-view/>
    </main>
    <myfooter></myfooter>
  </div>
</template>

<script>
// @ is an alias to /src
import Navbar from '@/components/Navbar.vue'
import MyFooter from '@/components/Footer.vue'
export default {
  name: 'App',
  components: {
    Navbar,
    MyFooter
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
  color: #2c3e50;
}
</style>
