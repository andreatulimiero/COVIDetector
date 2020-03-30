import React from 'react'
import { ReactMic } from '@cleandersonlobo/react-mic';

class VoiceRecorder extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      record: false
    }
  }

  startRecording = () => {
    this.setState({
      record: true
    });
  }

  stopRecording = () => {
    this.setState({
      record: false
    });
  }

  onData = (recordedBlob) => {
    console.log('This function does not return an object, but is called at a time interval of 10ms');
  }

  onStop = (recordedBlob) => {
    // console.log('recordedBlob is: ', recordedBlob);
    this.props.callback(recordedBlob);
  }

  render(){
    return (
      <div style={{"vertical-align": "middle"}}>
        <ReactMic
          record={this.state.record}
          className="sound-wave"
          onStop={this.onStop}
          onData={this.onData}
          strokeColor="#000000"
          backgroundColor="#FF4081" />
        <button onClick={this.startRecording} type="button">Start</button>
        <button onClick={this.stopRecording} type="button">Stop</button>
      </div>
    );
  }
}

export default VoiceRecorder;
