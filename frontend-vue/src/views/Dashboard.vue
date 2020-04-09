<template>
  <div id="dashboard">
    <header>
      <h1 class="display-4">Dashboard</h1>
      <hr/>
    </header>
    <div class="row">
      <div class="col-12 col-lg-6">
        <article id="record">
          <h2>New recording</h2>
          <div class="alert alert-success alert-dismissible" role="alert">
            <h4 class="alert-heading">Recording advices</h4>
            <ul>
              <li>Make sure you are in a quiet room when you start the recording.</li>
              <li>Listen to your submission to confirm that the sample was taken.</li>
              <li>Speak clearly so the algorithm can process the data better.</li>
              <li>Take as many attempts as you need, but only one recording can be submitted every 12 hours.</li>
            </ul>
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <section id="recorder">
            <h6><strong>Read this sentence:</strong></h6>
            <p class="lead">"The bird is flying back to its nest."</p>
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
          </section>
          <footer class="d-flex justify-content-between">
            <div id="condition" class="select">
              <select v-model="selected">
                <option disabled value="">State your condition</option>
                <option>Sick</option>
                <option>Not Sick</option>
                <option>Not Sure</option>
              </select>
            </div>
            <button class="btn btn-primary">Submit recording</button>
          </footer>
        </article>
      </div>
      <div class="col-12 col-lg-6">
        <article>
          <h2>Past Recordings</h2>
          <div v-for="item in this.$store.state.PastRecordings" :key="item.date">
            <div class="card recording">
              <div class="card-body">
                <div>
                  <svg class="bi bi-mic" width="1em" height="1em" viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                    <path fill-rule="evenodd" d="M3.5 6.5A.5.5 0 014 7v1a4 4 0 008 0V7a.5.5 0 011 0v1a5 5 0 01-4.5 4.975V15h3a.5.5 0 010 1h-7a.5.5 0 010-1h3v-2.025A5 5 0 013 8V7a.5.5 0 01.5-.5z" clip-rule="evenodd"/>
                    <path fill-rule="evenodd" d="M10 8V3a2 2 0 10-4 0v5a2 2 0 104 0zM8 0a3 3 0 00-3 3v5a3 3 0 006 0V3a3 3 0 00-3-3z" clip-rule="evenodd"/>
                  </svg>
                  {{ item.date }}
                </div>
                <button type="button" @click="remove" class="btn btn-danger">
                  <svg class="bi bi-trash" width="1em" height="1em" viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                    <path d="M5.5 5.5A.5.5 0 016 6v6a.5.5 0 01-1 0V6a.5.5 0 01.5-.5zm2.5 0a.5.5 0 01.5.5v6a.5.5 0 01-1 0V6a.5.5 0 01.5-.5zm3 .5a.5.5 0 00-1 0v6a.5.5 0 001 0V6z"/>
                    <path fill-rule="evenodd" d="M14.5 3a1 1 0 01-1 1H13v9a2 2 0 01-2 2H5a2 2 0 01-2-2V4h-.5a1 1 0 01-1-1V2a1 1 0 011-1H6a1 1 0 011-1h2a1 1 0 011 1h3.5a1 1 0 011 1v1zM4.118 4L4 4.059V13a1 1 0 001 1h6a1 1 0 001-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z" clip-rule="evenodd"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </article>
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

<style lang="scss">
#dashboard {
  #record{
    margin-bottom: 32px;
    section, footer { 
      margin-top: 32px;
    }
    #recorder {
      & > .ar {
        width: 100%;
      }
    }
    .select {
      position: relative;
      display: flex;
      width: 15em;
      height: 3em;
      line-height: 3;
      background: #2c3e50;
      overflow: hidden;
      border-radius: .25em;
      select {
        appearance: none;
        border: 0;
        background: var(--info);
        flex: 1;
        padding: 0 .5em;
        color: #fff;
        cursor: pointer;
      }
      /* Arrow */
      &::after {
        content: '\25BC';
        color: white;
        position: absolute;
        top: 0;
        right: 0;
        padding: 0 1em;
        cursor: pointer;
        pointer-events: none;
        transition: .25s all ease;
      }
    }

  }
  .recording {
    margin-top: 16px;
    .card-body {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
  }
}
</style>
