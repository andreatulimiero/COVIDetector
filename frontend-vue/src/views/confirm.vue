<template>
  <div id="confirm">
    <header>
      <img src="../assets/covid.jpg" id="covid">
      <h1>COVIDetector</h1>
      <p class="lead">Help the world's scientific community!</p> 
    </header>
    <article class="row justify-content-center">
      <div class="card col-10 col-md-8">
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
    </article>
  </div>
</template>

<script>
  export default {
    name: "Confirm",
    data() {
      return {
        token: "",
      }
    },
    methods: {
      confirm() {
        this.$store.dispatch('confirmUser', {token: this.token})
      }
    },
    created() {
      let token_query = this.$route.query.token 
      if (token_query !== undefined) this.token = token_query
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
