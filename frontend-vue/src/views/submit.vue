<template>
  <div id="submit">
    <h1>Secure Area</h1>
    <p>
      This is a secure area
    </p>
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
</template>

<script>
  export default {
    name: 'Submit',
    data() {
      return {};
    }
}
</script>

<style>
/* Not a thing
audio-recorder {
}*/
</style>
