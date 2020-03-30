import React from 'react'

class PatientInfoForm extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      ageRange: 1,
      gender: ""
    }
  }

  handleAgeRangeChange = (event) => {
    this.setState({ageRange: event.target.value});
  }

  handleGenderChange = (event) => {
    this.setState({gender: event.target.value});
  }

  handleSubmit = (event) => {
    event.preventDefault();
    var st_res = {ageRange: this.state.ageRange};
    if (this.state.gender.length != 0) {
      st_res.gender = this.state.gender;
    }
    this.props.callback(st_res);
  }

  render(){
    return (
      <form onSubmit={this.handleSubmit} className='input-form'>
        <div style={{width: "200px", "margin-bottom": "5px"}}>
          <div style={{width: "50%", float: "left"}}>
            <label>
              <h4>Age:</h4>
              <select value={this.state.ageRange} onChange={this.handleAgeRangeChange}>
                <option value="1">0-9</option>
                <option value="2">10-19</option>
                <option value="3">20-29</option>
                <option value="4">30-39</option>
                <option value="5">40-49</option>
                <option value="6">50-59</option>
                <option value="7">60-69</option>
                <option value="8">70-79</option>
                <option value="9">80-89</option>
                <option value="10">90-99</option>
                <option value="11">100+</option>
              </select>
            </label>
          </div>
          <div style={{width: "50%", float: "right"}}>
            <label>
              <h4>Gender:</h4>
              <select value={this.state.gender} onChange={this.handleGenderChange}>
                <option value="M">Male</option>
                <option value="F">Female</option>
                <option value="">Rather not to say</option>
              </select>
            </label>
          </div>
        </div>
        <input type="submit" value="Submit" />
      </form>
    );
  }
}

export default PatientInfoForm;
