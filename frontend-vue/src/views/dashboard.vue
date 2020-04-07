<template>
  <div id="dashboard">
    <header>
      <h1 id="title">Dashboard</h1>
    </header>
    <div class="row">
      <div class="col-md-6">
        <h3>Record your audio</h3>
        <article class="row justify-content-center">
          <div class="card col-12 col-md-11">
            <div id="audio" class="card-body">
              <p>State your condition:</p>
              <select v-model="selected">
                <option disabled value="">Please select one</option>
                <option>Sick</option>
                <option>Not Sick</option>
                <option>Not Sure</option>
              </select>
              <p>Speak this sentence into your microphone:</p>
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
        <div id="advice" class="card-body">
          <h3>Advice for recording</h3>
          <ul>
            <li>Make sure you are in a quiet room when you start the recording.</li>
            <li>Listen to your submission to confirm that the sample was taken.</li>
            <li>Speak clearly so the algorithm can process the data better.</li>
            <li>Take as many attempts as you need, but only one recording can be submitted every 12 hours.</li>
          </ul>
        </div>
      </article>
      </div>
      <div class="col-md-6">
        <h3>Past Recordings</h3>
        <div v-for="item in this.$store.state.PastRecordings" :key="item.date">
          <div class="card col-12 col-md-12">
            <div id="recording" class="row">
              <div class="col-9">
                {{ item.date }}
              </div>
              <div class="col">
                <button type="button" @click="remove" class="btn btn-danger">Delete</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'Dashboard',
    data() {
      return {
        selected: "",
      }
    },
    methods: {
      remove() {
        console.log("Deleted");
      }
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
#title {
  font-size: 3rem;
  font-weight: 300;
  line-height: 1.2;
  padding-top: 20px;
}
#advice {
  text-align: left;
}
#recording {
  text-align: left;
  font-weight: 100;
  vertical-align: middle;
}
</style>
