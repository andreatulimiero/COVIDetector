<template>
  <div id="dashboard">
    <header>
      <h1>Dashboard</h1>
    </header>
    <div class="row">
      <div class="col-md-6">
        <article class="row justify-content-center">
          <div class="card col-12 col-md-11">
            <div id="audio" class="card-body">
              <h3>Record your audio!</h3>
              <p>Record an audio sample here!</p>
              <p>Simply state your condition here:</p>
              <p>Simply say this sentence into your microphone:</p>
              <h4>"The bird is flying back to its nest."</h4>
              <audio-recorder
                upload-url="YOUR_API_URL"
                :attempts="1"
                :time=".2"
                :headers="headers"
                :before-recording="callback"
                :pause-recording="callback"
                :after-recording="callback"
                :select-record="callback"
                :before-upload="callback"
                :successful-upload="callback"
                :failed-upload="callback"/>
          </div>
        </div>
        <div class="card col-12 col-md-11">
          <div class="card-body">
            <h3>Advice for recording</h3>
            <ul>
              <li>Make sure you are in a quiet room when you start the recording.</li>
              <li>Listen to your submission to confirm that the sample was taken.</li>
              <li>Speak clearly so the algorithm can process the data better.</li>
              <li>Take as many attempts as you need, but only one recording can be submitted every 12 hours.</li>
            </ul>
          </div>
        </div>
      </article>
      </div>
      <div class="col-md-6">
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
#audio {
  align-content: center;
}
</style>
