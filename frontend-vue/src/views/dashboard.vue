<template>
  <div id="dashboard">
    <header>
      <h1>Dashboard</h1>
    </header>
    <div class="d-flex justify-content-between">
      <div>
        <audio-recorder
          upload-url="YOUR_API_URL"
          :attempts="3"
          :time="2"
          :headers="headers"
          :before-recording="callback"
          :pause-recording="callback"
          :after-recording="callback"
          :select-record="callback"
          :before-upload="callback"
          :successful-upload="callback"
          :failed-upload="callback"/>
      </div>
      <div>
        <h3>Past Recordings</h3>
        <p>Check out past recordings here! Feel free to delete any one of them that you like.</p>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'Dashboard',
    data() {
      return {};
    }
}
</script>

<style>
#dashboard {
  text-align: center;
}
</style>
