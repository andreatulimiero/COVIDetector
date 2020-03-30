import React from 'react'
import VoiceRecorder from '../components/VoiceRecorder'
import TextForm from '../components/TextForm'
import PatientInfoForm from '../components/PatientInfoForm'


//var URL = "http://18.156.30.58:8000/";
var URL = "http://localhost:8000/";

export default class MainContainer extends React.Component {

  state = {
    successMsg: '',
    errorMsg: ''
  }

  sendRecording = (input) => {
    var reader = new FileReader();
    var patient_token = localStorage.getItem('patient_token');
    var patient_secret = localStorage.getItem('patient_secret');
    var ptr = this;
    reader.onload = function () {
      var b64_audio = reader.result.replace(/^data:.+;base64,/, '');
      fetch(URL + "api/samples/", {
        method: "POST",
        headers: {
          'Content-Type': "application/json",
          'X-PATIENT-TOKEN': patient_token,
          'X-PATIENT-SECRET': patient_secret
        },
        body: JSON.stringify({
          patient: patient_token,
          audio: b64_audio
        })
      })
      .then((resp) => {
        if (resp.ok) {
          ptr.setState({successMsg: 'Successfully sent the voice recording'});
          ptr.setState({errorMsg: ''});
        } else {
          ptr.setState({successMsg: ''});
          ptr.setState({errorMsg: resp.statusText});
        }
        console.log(resp);
      })
      .catch((error) => {
        ptr.setState({successMsg: ''});
        ptr.setState({errorMsg: error});
        console.error('Error:', error);
      });
    }
    reader.readAsDataURL(input.blob);
  }

  regUser = (emailstr) => {
    fetch(URL + "api/register/", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email: emailstr
      })
    })
    .then((resp) => {
      if (resp.ok) {
        this.setState({successMsg: 'Successfully registered'});
        this.setState({errorMsg: ''});
      } else {
        this.setState({successMsg: ''});
        this.setState({errorMsg: resp.statusText});
      }
      console.log(resp);
    })
    .catch((error) => {
      this.setState({successMsg: ''});
      this.setState({errorMsg: error});
      console.error('Error:', error);
    });
  }

  regUserConfirm = (tokenstr) => {
    fetch(URL + "api/register/confirm/", {
      method: "POST",
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        token: tokenstr,
      })
    })
    .then((resp) => {
      if (resp.ok) {
        this.setState({errorMsg: ''});
        this.setState({successMsg: 'Successfully processed token'});
      } else {
        this.setState({successMsg: ''});
        this.setState({errorMsg: resp.statusText});
      }
      console.log(resp);
      resp.json().then(function(data) {
        if ('token' in data) {
          localStorage.setItem('patient_token', data.token);
          localStorage.setItem('patient_secret', data.secret);
        }
      });
    })
    .catch((error) => {
      this.setState({successMsg: ''});
      this.setState({errorMsg: error});
      console.error('Error:', error);
    });
  }

  updatePatientInfo = (state) => {
    var patient_token = localStorage.getItem('patient_token');
    var patient_secret = localStorage.getItem('patient_secret');
    fetch(URL + "api/patients/" + patient_token + "/", {
      method: "PUT",
      headers: {
        'Content-Type': 'application/json',
         'X-PATIENT-TOKEN': patient_token,
         'X-PATIENT-SECRET': patient_secret
      },
      body: JSON.stringify({
        age_range: state.ageRange,
        gender: state.gender
      })
    })
    .then((resp) => {
      if (resp.ok) {
        this.setState({successMsg: 'Successfully saved your information'});
        this.setState({errorMsg: ''});
      } else {
        this.setState({successMsg: ''});
        this.setState({errorMsg: resp.statusText});
      }
      console.log(resp);
    })
    .catch((error) => {
      this.setState({successMsg: ''});
      this.setState({errorMsg: error});
      console.error('Error:', error);
    });
  }

  render(){
    return (
      <div className="main-container">
        <h2>Registration and Information</h2>
        <div style={{"margin-bottom": "5px"}}>
          <div style={{width: "50%", float: "left"}}>
            <TextForm label="1. E-mail" callback={this.regUser}/>
          </div>
          <div style={{width: "50%", float: "right"}}>
            <TextForm label="2. Token" callback={this.regUserConfirm}/>
          </div>
        </div>
        <PatientInfoForm label="3. Information" callback={this.updatePatientInfo}/>
        <h2>Voice Recording</h2>
        <p>Please say this sentence when recording: <i>"I am currently waiting for my package to be delivered"</i></p>
        <VoiceRecorder callback={this.sendRecording}/>
        { this.state.successMsg &&
          <h3 className="success"> {this.state.successMsg} </h3> }
        { this.state.errorMsg &&
          <h3 className="error"> {"ERROR: " + this.state.errorMsg} </h3> }
      </div>
    )
  }

}
